import random
import uuid

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from task_manager.models import Task


class TaskListViewTest(TestCase):
    def setUp(self):
        # Create user.
        test_user = User.objects.create_user(
            username='test_user',
            password='pluralism'
        )

        test_user.save()

        # Create 10 tasks with different parameters for the user.
        status = True
        for i in range(10):
            status = not status

            # Generate pseudo random date for Task due date field.
            due_date = timezone.now()
            due_date + timezone.timedelta(days=random.randint(-10, 10))
            due_date = due_date.astimezone(timezone.get_default_timezone())

            # Generate random Task priority.
            # high, normal, low
            priorities = ['h', 'n', 'l']
            task_priority = random.choice(priorities)

            Task.objects.create(
                owner=test_user,
                name=f'Test Task {i}',
                due_date=due_date,
                status=status,
                priority=task_priority
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('task_manager:task-list'))
        self.assertRedirects(response, '/accounts/login/?next=/scheduler/tasks/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='test_user', password='pluralism')
        response = self.client.get(reverse('task_manager:task-list'))

        # Check our user is logged in.
        self.assertEqual(str(response.context['user']), 'test_user')
        # Check that we got a response "success".
        self.assertEqual(response.status_code, 200)

        # Check we used correct template.
        self.assertTemplateUsed(response, 'task_manager/task_list.html')

    def test_tasks_ordered_by_status_then_due_date_then_priority(self):
        login = self.client.login(username='test_user', password='pluralism')
        response = self.client.get(reverse('task_manager:task-list'))

        # Check our user is logged in.
        self.assertEqual(str(response.context['user']), 'test_user')
        # Check that we got a response "success".
        self.assertEqual(response.status_code, 200)

        # Get all Tasks from response context.
        tasks = response.context['task_list']

        # Check there are 10 Tasks created.
        self.assertEqual(len(tasks), 10)

        for i in range(1, len(tasks)):
            previous_task = tasks[i-1]
            current_task = tasks[i]

            # Check first ordering by status.
            self.assertTrue(previous_task.status <= current_task.status)

            # Check second ordering by due date only if status of the
            # current Task is the same as previous.
            if previous_task.status == current_task.status:
                self.assertTrue(previous_task.due_date <= current_task.due_date)

                # Check third ordering by priority only if due date of the
                # current Task is the same as previous.
                if previous_task.due_date == current_task.due_date:
                    self.assertTrue(previous_task.priority >= current_task.priority)


class MarkTaskDoneViewTest(TestCase):
    def setUp(self):
        # Create owner User.
        test_user1 = User.objects.create_user(
            username='test_user1',
            password='pluralism'
        )
        test_user1.save()
        # Create User with no Tasks.
        test_user2 = User.objects.create_user(
            username='test_user2',
            password='pluralism'
        )
        test_user2.save()

        # Create not done Task for the User.
        Task.objects.create(
            owner=test_user1,
            name='Test Task not done'
        )
        # Create done Task for the User.
        Task.objects.create(
            owner=test_user1,
            name='Test Task done',
            status=True
        )

    def test_redirect_if_not_logged_in(self):
        task = Task.objects.first()
        response = self.client.get(reverse('task_manager:task-mark', args=[str(task.pk)]))
        self.assertRedirects(response, f'/accounts/login/?next=/scheduler/task/{task.pk}/mark/')

    def test_logged_in_owner_can_mark_task_done(self):
        login = self.client.login(username='test_user1', password='pluralism')

        task = Task.objects.first()

        response = self.client.get(reverse('task_manager:task-mark', args=[str(task.pk)]))

        # Check that we got a response redirect.
        self.assertEqual(response.status_code, 302)

        # Check that the Task changed status to done (True).
        task = Task.objects.get(pk=task.pk)
        self.assertTrue(task.status)

    def test_logged_in_owner_can_mark_task_undone(self):
        login = self.client.login(username='test_user1', password='pluralism')

        task = Task.objects.last()

        response = self.client.get(reverse('task_manager:task-mark', args=[str(task.pk)]))

        # Check that we got a response redirect.
        self.assertEqual(response.status_code, 302)

        # Check that the Task has changed status to done (True).
        task = Task.objects.get(pk=task.pk)
        self.assertFalse(task.status)

    def test_logged_in_not_owner_can_mark_task(self):
        login = self.client.login(username='test_user2', password='pluralism')

        task = Task.objects.first()

        response = self.client.get(reverse('task_manager:task-mark', args=[str(task.pk)]))

        # Check that we got a response not found.
        self.assertEqual(response.status_code, 404)

        # Check that the Task hasn't changed status to done (True).
        task = Task.objects.get(pk=task.pk)
        self.assertFalse(task.status)

    def test_logged_in_get_404_when_try_to_mark_not_existing_task(self):
        login = self.client.login(username='test_user1', password='pluralism')

        dummy_uuid = uuid.uuid4()

        response = self.client.get(reverse('task_manager:task-mark', args=[str(dummy_uuid)]))

        # Check that we got a response redirect.
        self.assertEqual(response.status_code, 404)

    # Actually this is not related to view, but django.
    def test_logged_in_get_404_when_try_to_mark_task_by_invalid_uuid(self):
        login = self.client.login(username='test_user1', password='pluralism')

        bad_uuid = 'sdsd3e2ddd'

        response = self.client.get(f'/scheduler/task/{bad_uuid}/mark/')

        # Check that we got a response redirect.
        self.assertEqual(response.status_code, 404)


class ShareTaskViewTest(TestCase):
    def setUp(self):
        # Create owner User.
        test_user1 = User.objects.create_user(
            username='test_user1',
            password='pluralism'
        )
        test_user1.save()
        # Create User with no Tasks.
        test_user2 = User.objects.create_user(
            username='test_user2',
            password='pluralism'
        )
        test_user2.save()

        # Create not done Task for the User.
        Task.objects.create(
            owner=test_user1,
            name='Test Task not shared'
        )
        # Create done Task for the User.
        Task.objects.create(
            owner=test_user1,
            name='Test Task shared',
            is_shared=True,
            status=True # status True for easy ordering.
        )

    def test_redirect_if_not_logged_in(self):
        task = Task.objects.first()
        response = self.client.get(reverse('task_manager:task-share', args=[str(task.pk)]))
        self.assertRedirects(response, f'/accounts/login/?next=/scheduler/task/{task.pk}/share/')

    def test_logged_in_owner_can_share_task(self):
        login = self.client.login(username='test_user1', password='pluralism')

        task = Task.objects.first()

        response = self.client.get(reverse('task_manager:task-share', args=[str(task.pk)]))

        # Check that we got a response redirect.
        self.assertEqual(response.status_code, 302)

        # Check that the Task changed status to done (True).
        task = Task.objects.get(pk=task.pk)
        self.assertTrue(task.is_shared)

    def test_logged_in_owner_can_unshare_task(self):
        login = self.client.login(username='test_user1', password='pluralism')

        task = Task.objects.last()

        response = self.client.get(reverse('task_manager:task-share', args=[str(task.pk)]))

        # Check that we got a response redirect.
        self.assertEqual(response.status_code, 302)

        # Check that the Task has changed status to done (True).
        task = Task.objects.get(pk=task.pk)
        self.assertFalse(task.is_shared)

    def test_logged_in_not_owner_can_share_task(self):
        login = self.client.login(username='test_user2', password='pluralism')

        task = Task.objects.first()

        response = self.client.get(reverse('task_manager:task-share', args=[str(task.pk)]))

        # Check that we got a response not found.
        self.assertEqual(response.status_code, 404)

        # Check that the Task hasn't changed status to done (True).
        task = Task.objects.get(pk=task.pk)
        self.assertFalse(task.is_shared)

    def test_logged_in_get_404_when_try_to_share_not_existing_task(self):
        login = self.client.login(username='test_user1', password='pluralism')

        dummy_uuid = uuid.uuid4()

        response = self.client.get(reverse('task_manager:task-share', args=[str(dummy_uuid)]))

        # Check that we got a response redirect.
        self.assertEqual(response.status_code, 404)
