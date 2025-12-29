# blog/views.py
from django.shortcuts import render
from .models import Post

def home(request):
    latest_posts = Post.objects.all().order_by("-created_at")[:5]

    # notes 앱이 있을 때만 가져오기 (없으면 터지니까 안전하게)
    try:
        from notes.models import Note
        latest_notes = Note.objects.all().order_by("-created_at")[:5]
        note_count = Note.objects.count()
    except Exception:
        latest_notes = []
        note_count = 0

    post_count = Post.objects.count()

    return render(request, "blog/home.html", {
        "latest_posts": latest_posts,
        "latest_notes": latest_notes,
        "post_count": post_count,
        "note_count": note_count,
    })


def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "blog/post_list.html", {"posts": posts})


from django.shortcuts import render
from aggregator.models import FeedEntry

def home(request):
    recommended = FeedEntry.objects.select_related("source").all()[:9]  # 최신 9개
    return render(request, "blog/home.html", {"recommended": recommended})
