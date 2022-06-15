from django.db import models
# Used to generate URLs by reversing the URL patterns
from django.urls import reverse

# Create your models here.


class Technologies(models.Model):
    """Model representing a technology."""
    name = models.CharField(
        max_length=200, help_text='Enter a technology, framework, library... (e.g. React)')

    def __str__(self):
        return self.name


class Owner(models.Model):
    """Model representing an owner."""
    full_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=50)
    date_of_registry = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['full_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular owner instance."""
        return reverse('owner-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.full_name}, {self.nickname}'


class Languages(models.Model):
    """Model representing a Language (e.g. Python, Lisp, Java, etc.)"""
    name = models.CharField(max_length=50,
                            help_text="Enter the project's languages")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Project(models.Model):
    """Model representing a project."""
    name = models.CharField(max_length=200)

    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)

    description = models.TextField(
        max_length=1000, help_text='Enter a description about the project')

    technologies = models.ManyToManyField(
        Technologies, help_text='Select a technology.')

    languages = models.ManyToManyField(
        Languages, help_text='Select a language')

    def display_technologies(self):
        """Create a string for the Technologies. This is required to display technology in Admin."""
        return ', '.join(technologies.name for technologies in self.technologies.all()[:3])

    display_technologies.short_description = 'Technology'

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('project-detail', args=[str(self.id)])
