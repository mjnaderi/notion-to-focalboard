import os
import uuid

from django.conf import settings
from django.db import models


class ConvertTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notion_export = models.FileField(upload_to="notion_export")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class State(models.TextChoices):
        PENDING = "pending", "Pending"
        RUNNING = "running", "Running"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    state = models.CharField(
        max_length=10,
        choices=State.choices,
        default=State.PENDING,
    )

    def __str__(self):
        return f"{self.id}: {self.state}"

    def get_archive_name(self):
        return os.path.splitext(os.path.basename(self.notion_export.path))[0]

    def get_result_path(self):
        return settings.MEDIA_ROOT / "result" / f"{self.id}.boardarchive"
