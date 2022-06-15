from django.contrib import admin
from .models import Languages, Owner, Project, Technologies

# Register your models here.

class ProjectAdminInline(admin.TabularInline):
    model = Project

# admin.site.register(Project)
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'display_technologies', 'description')
    list_per_page = 10
    list_filter = (['owner'])
    fieldsets = (
        (None, {
            'fields': ('name', 'owner', 'description')
        }),
        ('Characteristics', {
            'fields': ('technologies', 'languages')
        }),
    )

# admin.site.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'nickname', 'date_of_registry')
    inlines = [ProjectAdminInline]

admin.site.register(Owner, OwnerAdmin)
admin.site.register(Technologies)
admin.site.register(Languages)
