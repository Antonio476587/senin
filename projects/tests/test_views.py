from django.test import TestCase
from django.urls import reverse

from projects.models import Owner, Languages, Technologies, Project
from django.contrib.auth.models import User

class OwnerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 owners for pagination tests
        number_of_owners = 13

        for owner_id in range(number_of_owners):
            Owner.objects.create(
                full_name=f'Christian {owner_id}',
                nickname=f'Surname {owner_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/project/owners/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('owners'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('owners'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/owner_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('owners'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['owner_list']), 10)

    def test_lists_all_owners(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('owners')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['owner_list']), 3)

import uuid

from django.contrib.auth.models import Permission # Required to grant the permission needed to set a book as returned.

class RenewBookInstancesViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')

        test_user1.save()

        # Create a book
        self.test_author = Owner.objects.create(full_name='John', nickname='Smith')
        test_technology = Technologies.objects.create(name='Hadoop')
        test_language = Languages.objects.create(name='Swift')
        test_project = Project.objects.create(
            name='Project Title',
            description='My project summary',
            owner=self.test_author,
        )

        # Create technologies as a post-step
        technologies_objects_for_projects = Technologies.objects.all()
        test_project.technologies.set(technologies_objects_for_projects) # Direct assignment of many-to-many types not allowed.
        test_project.save()

        # Create languages as a post-step
        languages_objects_for_projects = Languages.objects.all()
        test_project.languages.set(languages_objects_for_projects) # Direct assignment of many-to-many types not allowed.
        test_project.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('edit-owner-nickname', kwargs={'pk': self.test_author.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in_get_the_page(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('edit-owner-nickname', kwargs={'pk': self.test_author.pk}))

        # Check that it lets us login - and get the page
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        # unlikely UID to match our bookinstance!
        test_uid = uuid.uuid4()
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('edit-owner-nickname', kwargs={'pk':test_uid}))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('edit-owner-nickname', kwargs={'pk': self.test_author.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'project/owner_edit_nickname.html')

    def test_redirects_to_owner_detail_on_success(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        valid_nickname = 'fanstasma'
        response = self.client.post(reverse('edit-owner-nickname', kwargs={'pk':self.test_author.pk,}), {'nickname':valid_nickname})
        self.assertRedirects(response, reverse('owner-detail', args=[str(self.test_author.pk)]))

    def test_form_invalid_nickname_is_digit(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        nickname_in_digits = '222'
        response = self.client.post(reverse('edit-owner-nickname', kwargs={'pk': self.test_author.pk}), {'nickname': nickname_in_digits})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'nickname', 'Add some characters, it is not R2D2')

    def test_form_no_printable_nickname(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        no_printable_nickname = '\n'
        response = self.client.post(reverse('edit-owner-nickname', kwargs={'pk': self.test_author.pk}), {'nickname': no_printable_nickname})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'nickname', 'Your nickname is not printable')

