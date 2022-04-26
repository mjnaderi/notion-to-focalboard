from django import forms
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import ConvertTask


class ConvertForm(forms.ModelForm):
    class Meta:
        model = ConvertTask
        fields = ["notion_export"]


def convert(request):
    if request.method == "POST":
        form = ConvertForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("convert:view-convert-result", task_id=form.instance.id)
    else:
        form = ConvertForm()
    return render(request, "convert/convert.html", {"form": form})


def view_convert_result(request, task_id):
    task = get_object_or_404(ConvertTask, id=task_id)
    return render(request, "convert/result.html", {"task": task})


def download_archive(request, task_id):
    task = get_object_or_404(ConvertTask, id=task_id)
    try:
        archive = open(task.get_result_path(), "rb")
    except FileNotFoundError:
        return HttpResponse("File not found.", status=404)
    response = StreamingHttpResponse(archive)
    response[
        "Content-Disposition"
    ] = f"attachment; filename={task.get_archive_name()}.boardarchive"
    return response
