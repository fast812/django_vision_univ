# mysite/urls.py
from django.contrib import admin
from django.urls import path, include
from blog import views as blog_views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", blog_views.home, name="home"),     # ✅ 홈 대시보드
    path("blog/", include("blog.urls")),        # ✅ 글 목록은 /blog/ 로
    path("", include("pages.urls")),
    path("notes/", include("notes.urls")),
]
