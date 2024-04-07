import os
from multiprocessing import cpu_count

port = os.getenv("DJANGO_PORT", 8000)
bind = f'0.0.0.0:{port}'
workers = cpu_count() * 2 + 1
logconfig_json = 'log_conf.json'
timeout = 300
