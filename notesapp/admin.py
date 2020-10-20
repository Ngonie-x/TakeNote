from django.contrib import admin
from .models import Note, Categories

# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created')
    list_filter = ('category', 'created')
    search_fields = ('title', 'text')

admin.site.register(Note, NoteAdmin)
admin.site.register(Categories)