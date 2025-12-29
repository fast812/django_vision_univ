from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_datetime

import feedparser

from aggregator.models import FeedSource, FeedEntry


def _to_dt(entry) -> timezone.datetime | None:
    # feedparser는 published_parsed를 time.struct_time로 주는 경우가 많음
    if getattr(entry, "published_parsed", None):
        return timezone.make_aware(
            timezone.datetime(*entry.published_parsed[:6]),
            timezone=timezone.get_current_timezone(),
        )
    # 혹시 ISO 형태면 파싱 시도
    if getattr(entry, "published", None):
        dt = parse_datetime(entry.published)
        if dt:
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt, timezone.get_current_timezone())
            return dt
    return None


class Command(BaseCommand):
    help = "RSS/Atom 피드를 가져와서 FeedEntry에 저장합니다."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=10, help="소스별로 최대 몇 개 항목 저장할지")

    def handle(self, *args, **options):
        limit = options["limit"]

        sources = FeedSource.objects.filter(is_active=True)
        if not sources.exists():
            self.stdout.write(self.style.WARNING("활성화된 FeedSource가 없습니다. 먼저 소스를 추가하세요."))
            return

        total_new = 0

        for src in sources:
            self.stdout.write(f"Fetching: {src.name} ({src.feed_url})")
            feed = feedparser.parse(src.feed_url)

            # feedparser는 bozo(깨진 피드)라도 entries는 주는 경우가 있어 그냥 진행
            entries = feed.entries[:limit]

            for e in entries:
                url = getattr(e, "link", "").strip()
                title = getattr(e, "title", "").strip()
                summary = getattr(e, "summary", "") or getattr(e, "description", "")
                uid = (getattr(e, "id", "") or url or f"{src.id}:{title}").strip()

                if not (title and url and uid):
                    continue

                published_at = _to_dt(e)

                obj, created = FeedEntry.objects.get_or_create(
                    uid=uid,
                    defaults={
                        "source": src,
                        "title": title[:300],
                        "url": url,
                        "summary": summary[:5000],
                        "published_at": published_at,
                    },
                )
                if created:
                    total_new += 1

        self.stdout.write(self.style.SUCCESS(f"Done. New entries: {total_new}"))
