# notes/urls.py
from django.urls import path
from .views import (
    NoteListView, NoteDetailView, NoteCreateView, NoteUpdateView, NoteDeleteView
)
from .views import note_ai_summarize  # ✅ 추가

urlpatterns = [
    path("", NoteListView.as_view(), name="note_list"),
    path("new/", NoteCreateView.as_view(), name="note_create"),
    path("<int:pk>/", NoteDetailView.as_view(), name="note_detail"),
    path("<int:pk>/edit/", NoteUpdateView.as_view(), name="note_update"),
    path("<int:pk>/delete/", NoteDeleteView.as_view(), name="note_delete"),

    # ✅ AI 요약 버튼 POST 엔드포인트
    path("<int:pk>/ai-summarize/", note_ai_summarize, name="note_ai_summarize"),
]
