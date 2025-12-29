from django.db import models

class FeedSource(models.Model):
    name = models.CharField(max_length=120, unique=True)
    site_url = models.URLField(blank=True, default="")
    feed_url = models.URLField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class FeedEntry(models.Model):
    source = models.ForeignKey(FeedSource, on_delete=models.CASCADE, related_name="entries")
    title = models.CharField(max_length=300)
    url = models.URLField()
    summary = models.TextField(blank=True, default="")
    published_at = models.DateTimeField(null=True, blank=True)

    # 같은 글 중복 저장 방지용(피드에 보통 들어있는 고유 id/링크)
    uid = models.CharField(max_length=500, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self) -> str:
        return f"[{self.source.name}] {self.title}"
