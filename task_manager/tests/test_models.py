import uuid

from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase

from task_manager.models import Task

class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods.

        # Create test User.
        User.objects.create(username='test_user')

        # Create test Tasks.

        # Task in the past.
        Task.objects.create(owner=User.objects.first(), name='Test Task in the past', due_date=timezone.datetime(year=2020, month=3, day=20, hour=13, minute=55).astimezone(timezone.get_default_timezone()), description='Test description.')

        # Task in the future.
        Task.objects.create(name='Test Task in the future', due_date=timezone.now() + timezone.timedelta(minutes=1.0), description='Test description.', status=True,)

    # Test fields attributes.

    # id

    def test_id_default_type_is_uuid(self):
        task = Task.objects.first()
        id = uuid.uuid4()
        self.assertEqual(type(task.id), type(id))

    def test_id_is_primary_key(self):
        task = Task.objects.first()
        is_primary_key = task._meta.get_field('id').primary_key
        self.assertTrue(is_primary_key)

    # owner

    def test_owner_is_not_null(self):
        task = Task.objects.first()
        self.assertIsNotNone(task.owner)

    def test_owner_on_delete_set_null(self):
        # Get Task owner and delete object.
        user = User.objects.first()
        User.delete(user)

        # Get Task object with no owner from this point.
        task = Task.objects.first()

        self.assertEqual(task.owner, None)

    def test_owner_allow_null(self):
        task = Task.objects.first()
        can_be_null = task._meta.get_field('owner').null
        self.assertTrue(can_be_null)

    # name

    def test_name_max_length(self):
        task = Task.objects.first()
        max_length = task._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_name_label(self):
        task = Task.objects.first()
        field_label = task._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Task name')

    # due_date

    # TODO: fails for first Task with manually set datetime.
    def test_due_date_timezone(self):
        task = Task.objects.last()
        default_timezone = timezone.now().astimezone(timezone.get_default_timezone()).tzinfo
        task_timezone = task.due_date.astimezone(timezone.get_default_timezone()).tzinfo
        self.assertEquals(task_timezone, default_timezone)

    # description

    def test_description_max_length(self):
        task = Task.objects.first()
        max_length = task._meta.get_field('description').max_length
        self.assertEqual(max_length, 5000)

    # status

    def test_status_label(self):
        task = Task.objects.first()
        field_label = task._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'Done')

    def test_status_default_is_false(self):
        task = Task.objects.first()
        self.assertFalse(task.status)

    # is_shared

    def test_is_shared_default_is_false(self):
        task = Task.objects.first()
        self.assertFalse(task.is_shared)

    # priority

    def test_priority_max_length(self):
        task = Task.objects.first()
        max_length = task._meta.get_field('priority').max_length
        self.assertEqual(max_length, 1)

    def test_priority_default_is_normal(self):
        task = Task.objects.first()
        self.assertEqual(task.priority, 'n')

    def test_priority_choices_are_high_normal_and_low(self):
        task = Task.objects.first()
        task_priorities = task._meta.get_field('priority').choices
        TASK_PRIORITIES = (
            ('h', 'High'),
            ('n', 'Normal'),
            ('l', 'Low')
        )
        self.assertEqual(task_priorities, TASK_PRIORITIES)

    # Test own methods.

    def test_object_name_is_name_bracket_day_month_year_hour_minute_bracket(self):
        task = Task.objects.first()
        expected_object_name = f'{task.name} (20 Mar 2020 13:55)'
        self.assertEqual(expected_object_name, str(task))

    def test_task_in_the_past_is_overdue(self):
        task_past = Task.objects.first()
        self.assertTrue(task_past.is_overdue)

    def test_task_in_the_future_is_overdue(self):
        task_future = Task.objects.last()
        self.assertFalse(task_future.is_overdue)

    def test_crispy_time(self):
        task = Task.objects.first()
        time_format = '13:55'
        self.assertEqual(task.crispy_time, time_format)

    def test_get_absolute_url(self):
        task = Task.objects.first()
        # This will also fail if the urlconf is not defined.
        self.assertEqual(task.get_absolute_url(), f'/scheduler/task/{task.id}/')
