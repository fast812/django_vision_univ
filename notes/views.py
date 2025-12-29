# notes/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Note
from .forms import NoteForm

class NoteListView(ListView):
    model = Note
    template_name = "notes/note_list.html"
    context_object_name = "notes"

class NoteDetailView(DetailView):
    model = Note
    template_name = "notes/note_detail.html"
    context_object_name = "note"

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"
    success_url = reverse_lazy("note_list")

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"
    success_url = reverse_lazy("note_list")

class NoteDeleteView(DeleteView):
    model = Note
    template_name = "notes/note_confirm_delete.html"
    success_url = reverse_lazy("note_list")

# notes/views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Note
from .services import summarize_korean


def note_ai_summarize(request, pk: int):
    """
    노트를 OpenAI로 요약해서 Note.ai_summary에 저장
    """
    note = get_object_or_404(Note, pk=pk)

    if request.method != "POST":
        return redirect("note_detail", pk=note.pk)

    try:
        summary = summarize_korean(note.content)
        note.ai_summary = summary
        note.save(update_fields=["ai_summary"])
        messages.success(request, "AI 요약이 생성됐어요.")
    except Exception as e:
        messages.error(request, f"AI 요약 생성 실패: {e}")

    return redirect("note_detail", pk=note.pk)
