from django.urls import path
from .views import notes_list_index, NoteDeleteView, update_note

app_name = 'notesapp'

urlpatterns = [
    path('', notes_list_index, name="list_index"),
    path('<pk>/delete', NoteDeleteView.as_view(), name='delete'),
    path('<pk>/update', update_note, name='update'),
]
