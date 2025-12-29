# notes/forms.py
from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "course", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "제목"}),
            "course": forms.TextInput(attrs={"class": "form-control", "placeholder": "과목/주제 (선택)"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10, "placeholder": "내용"}),
        }
