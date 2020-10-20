from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'text')

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-control', 'placeholder':'Title...'})
        self.fields['text'].widget.attrs.update({'class':'form-control', 'placeholder':'Note..'})

