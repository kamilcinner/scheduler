from django.contrib.auth.models import User
from django.test import TestCase, SimpleTestCase
from django.urls import reverse


class IndexViewTest(TestCase):
    # TODO: add this at the end
    # def setUp(self):
    #     # Create user.
    #     test_user = User.objects.create_user(
    #         username='test_user',
    #         password='pluralism'
    #     )
    #
    #     test_user.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class InactiveYetViewTest(SimpleTestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/inactive/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('inactive-yet'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('inactive-yet'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inactive.html')


class AboutViewTest(SimpleTestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')


class OtherProjectsViewTest(SimpleTestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/other/projects/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('other-projects'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('other-projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'other_projects.html')
