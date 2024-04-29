# myproject/celery.py

import os
import sys
from celery import Celery

# 设置默认的 Django 设置模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

app = Celery("myproject")

# 从 Django 的设置文件中加载配置模块
app.config_from_object("django.conf:settings", namespace="CELERY")

# 自动发现和加载任务
app.autodiscover_tasks()

if "test" in sys.argv:
    app.conf.update(
        {
            "task_always_eager": True,
            "task_eager_propagates": True,  # Exceptions are propagated rather than stored
            "broker_url": "memory://",  # Use memory broker to avoid I/O operations
            "result_backend": "cache+memory://",  # Store results in memory
        }
    )
