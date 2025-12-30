#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# ✅ 1) 피드 소스(FeedSource) 넣기: 이미 있으면 실패할 수 있으니 || true
python manage.py loaddata aggregator/fixtures/feeds.json || true

# ✅ 2) 피드 수집: 네트워크/RSS 문제로 실패할 수 있으니 || true
python manage.py fetch_feeds --limit 10 || true