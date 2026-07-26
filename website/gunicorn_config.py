import json
from pathlib import Path

with Path('website/prod-config.json').open() as json_file:
    data = json.load(json_file)

workers = int(data.get('GUNICORN_PROCESSES', '1'))
threads = int(data.get('GUNICORN_THREADS', '1'))
bind = data.get('GUNICORN_BIND', 'localhost:8098')
