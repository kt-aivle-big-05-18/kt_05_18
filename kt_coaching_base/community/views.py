# community/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponse, Http404
import urllib.parse
import mimetypes
import os
from .models import Notice, Survey
from .forms import NoticeForm

# Create your views here.
def notice_list(request):
    notices = Notice.objects.order_by('-created_at')
    reversed(notices)
    return render(request, 'community/notice_list.html', {'notices': notices})

@login_required
def notice_create(request):
    if request.method == "POST":
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.file = request.FILES["file"]
            notice.save()
            messages.success(request, "공지사항 작성 완료")
            return redirect("community:notice_list")
    elif request.method == "GET":
        if not request.user.is_superuser:
            error_message = "허가되지 않은 행동입니다."
            script = f'<script>alert("{error_message}"); window.location.href="{reverse("community:notice_list")}";</script>'
            return HttpResponseBadRequest(script)
        else:
            form = NoticeForm()

    return render(request, "community/notice_create.html", {"form": form})

def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)

    if request.method == "POST" and 'download' in request.POST:
        if notice.file:
            file_path = notice.file.path
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    file_name = os.path.basename(file_path)
                    file_name_encoded = urllib.parse.quote(file_name.encode('utf-8'))
                    content_type, _ = mimetypes.guess_type(file_path)
                    response = HttpResponse(file.read(), content_type=content_type)
                    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{file_name_encoded}'
                    return response
            else:
                message = "파일이 없습니다."
                return render(request, "community/notice_detail.html", {"notice": notice, "message": message})

    return render(request, "community/notice_detail.html", {"notice": notice})

def survey_list(request):
    surveys = Survey.objects.all()
    return render(request, 'community/survey_list.html', {'surveys': surveys})