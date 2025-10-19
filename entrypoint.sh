# ...existing code...
#!/bin/sh
set -e

echo "Waiting for Postgres..."

python - <<PY
import os, time, socket
host = os.environ.get('POSTGRES_HOST', 'db')
port = int(os.environ.get('POSTGRES_PORT', 5432))
for _ in range(60):
    try:
        s = socket.create_connection((host, port), 2); s.close()
        print('Postgres is up')
        break
    except Exception:
        time.sleep(1)
else:
    print('Timed out waiting for Postgres')
    raise SystemExit(1)
PY

# Apply migrations
python manage.py migrate --noinput

# Create superuser if env vars provided (uses heredoc to avoid syntax errors)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
  python - <<PY
from django.contrib.auth import get_user_model
User = get_user_model()
username = "${DJANGO_SUPERUSER_USERNAME}"
email = "${DJANGO_SUPERUSER_EMAIL}"
password = "${DJANGO_SUPERUSER_PASSWORD}"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
PY
fi

exec "$@"
# ...existing code...