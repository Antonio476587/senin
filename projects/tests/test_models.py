from unicodedata import name
from django.test import TestCase

from projects.models import Project, Owner, Technologies, Languages

class OwnerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Owner.objects.create(full_name='Biggie Small', nickname='Big Poppa')

    def test_full_name_label(self):
        owner = Owner.objects.get(id=1)
        field_label = owner._meta.get_field('full_name').verbose_name
        self.assertEqual(field_label, 'full name')

    def test_full_name_max_length(self):
        owner = Owner.objects.get(id=1)
        max_length = owner._meta.get_field('full_name').max_length
        self.assertEqual(max_length, 100)

    def test_nickname_max_length(self):
        owner = Owner.objects.get(id=1)
        max_length = owner._meta.get_field('nickname').max_length
        self.assertEqual(max_length, 50)

    def test_object_name_is_full_name_comma_nickname(self):
        owner = Owner.objects.get(id=1)
        expected_object_name = f'{owner.full_name}, {owner.nickname}'
        self.assertEqual(str(owner), expected_object_name)

    def test_get_absolute_url(self):
        owner = Owner.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(owner.get_absolute_url(), '/projects/owner/1')

class ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Owner.objects.create(full_name='Biggie Small', nickname='Big Poppa')
        Languages.objects.create(name='JavaScript')
        Technologies.objects.create(name='React')
        Project.objects.create(name='Album', owner=Owner.objects.get(id=1), description='Illuminati, for all those hommies, I love you niggas, I am on.')
        project=Project.objects.get(id=1)
        project.technologies.add(Technologies.objects.get(name='React'))
        project.languages.add(Languages.objects.get(name='JavaScript'))
        project.save()

    def test_owner_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('owner').verbose_name
        self.assertEqual(field_label, 'owner')

    def test_delete_owner(self):
        project = Project.objects.get(id=1)
        Owner.objects.delete(full_name=project.owner.full_name)
        owner = Owner.objects.get(full_name=project.owner.full_name)
        project._meta.get_field('owner')
        self.assertFalse(owner)

    def test_name_max_length(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_description_max_length(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('description').max_length
        self.assertEqual(max_length, 1000)

    def test_get_absolute_url(self):
        project = Project.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(project.display_technologies(), ', '.join(technologies.name for technologies in project.technologies.all()[:3]))

    def test_object_name_is_name(self):
        project = Project.objects.get(id=1)
        expected_object_name = str(project.name)
        self.assertEqual(str(project), expected_object_name)

    def test_get_absolute_url(self):
        project = Project.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(project.get_absolute_url(), '/projects/project/1')

class LanguageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Languages.objects.create(name='JavaScript')

    def test_name_label(self):
        language = Languages.objects.get(id=1)
        field_label = language._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_full_name_max_length(self):
        language = Languages.objects.get(id=1)
        max_lenght = language._meta.get_field('name').max_length
        self.assertEqual(max_lenght, 50)

    def test_object_name_is_name(self):
        language = Languages.objects.get(id=1)
        expected_object_name = str(language.name)
        self.assertEqual(str(language), expected_object_name)

class TechnologiesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Technologies.objects.create(name='React')

    def test_name_label(self):
        technology = Technologies.objects.get(id=1)
        field_label = technology._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_full_name_max_length(self):
        technology = Technologies.objects.get(id=1)
        max_lenght = technology._meta.get_field('name').max_length
        self.assertEqual(max_lenght, 200)

    def test_object_name_is_name(self):
        technology = Technologies.objects.get(id=1)
        expected_object_name = str(technology.name)
        self.assertEqual(str(technology), expected_object_name)
