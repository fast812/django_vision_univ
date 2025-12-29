# notes/models.py
from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=200)
    course = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ✅ 추가: AI 요약 저장
    ai_summary = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title
