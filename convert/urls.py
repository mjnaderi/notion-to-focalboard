from django.urls import path

from .views import convert, download_archive, view_convert_result

app_name = "convert"
urlpatterns = [
    path("", convert, name="convert"),
    path("result/<uuid:task_id>", view_convert_result, name="view-convert-result"),
    path("download/<uuid:task_id>", download_archive, name="download-archive"),
]
