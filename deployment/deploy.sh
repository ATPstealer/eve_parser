#!/usr/bin/env bash
# Usage: deploy.sh <branch>
set -euo pipefail

BRANCH="${1:?branch required}"
APP_DIR=/root/eve_parser

cd "$APP_DIR"

git fetch origin "$BRANCH"
git checkout -B "$BRANCH" "origin/$BRANCH"
git reset --hard "origin/$BRANCH"

python3 -m pip install -r requirements.txt

python3 manage.py migrate --noinput

cp deployment/cron/eve-parser /etc/cron.d/eve-parser
chmod 644 /etc/cron.d/eve-parser

cp deployment/systemd/django.service /etc/systemd/system/django.service
systemctl daemon-reload
systemctl restart django

cp deployment/nginx/evelog.online.conf /etc/nginx/sites-available/evelog.online.conf
ln -sf /etc/nginx/sites-available/evelog.online.conf /etc/nginx/sites-enabled/evelog.online.conf
nginx -t
systemctl reload nginx

echo "Deployed $BRANCH @ $(git rev-parse --short HEAD)"
