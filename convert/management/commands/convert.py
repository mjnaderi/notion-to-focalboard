import os
import shutil
import subprocess
import time
from datetime import timedelta
from tempfile import TemporaryDirectory

from django.core.management.base import BaseCommand
from django.utils import timezone

from convert.models import ConvertTask


class Command(BaseCommand):
    help = "Handle convert tasks"

    SLEEP = 2  # seconds

    def add_arguments(self, parser):
        parser.add_argument("focalboard_repo", nargs=1, type=str)

    def convert(self, task: ConvertTask):
        with TemporaryDirectory() as tmpdir:
            self.stdout.write(tmpdir)
            notion_unpacked_path = os.path.join(tmpdir, "notion")
            os.mkdir(notion_unpacked_path)
            shutil.unpack_archive(task.notion_export.path, notion_unpacked_path)
            res = subprocess.run(
                [
                    "npx",
                    "ts-node",
                    "importNotion.ts",
                    "-i",
                    notion_unpacked_path,
                    "-o",
                    task.get_result_path(),
                ],
                capture_output=True,
                text=True,
            )
            if res.returncode != 0:
                task.state = ConvertTask.State.FAILED
                task.error_msg = (
                    f"Return Code: {res.returncode}\n{res.stderr}\n{res.stdout}"[:400]
                )
                task.save()
                self.stdout.write(f"Failed to convert {task.id}: {res.stdout}")
            else:
                task.state = ConvertTask.State.COMPLETED
                task.save()
                self.stdout.write(f"Converted {task.id}")

    def handle(self, *args, **options):
        os.chdir(os.path.join(options["focalboard_repo"][0], "import", "notion"))

        i = 0
        while True:

            i = (i + 1) % 100
            if i == 0:
                self.stdout.write(f"Deleting old task files")
                tasks = list(
                    ConvertTask.objects.filter(
                        created_at__lt=timezone.now() - timedelta(days=1)
                    )
                )
                for task in tasks:
                    try:
                        task.notion_export.delete()
                        os.remove(task.get_result_path())
                    except FileNotFoundError:
                        pass
                self.stdout.write(f"Deleted files for {len(tasks)} old tasks")

            for task in ConvertTask.objects.filter(state=ConvertTask.State.PENDING):
                task.state = ConvertTask.State.RUNNING
                task.save()
                self.stdout.write(f"Converting {task.id}")
                try:
                    self.convert(task)
                except:
                    task.state = ConvertTask.State.FAILED
                    task.save()
                    self.stdout.write(f"Failed to convert {task.id}")

            time.sleep(self.SLEEP)
