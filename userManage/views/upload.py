import os
from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from userManage.utils.form import UploadForm, UploadModalForm
from userManage import models


def upload_form(request):
    title = "基于form上传文件"
    if request.method == 'GET':
        form = UploadForm()
        return render(request, 'upload_form.html', {"title": title, "form": form})
    form = UploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 读取用户上传的文件，写入到自定义的文件夹中，并获取文件的路径
        file_object = form.cleaned_data.get("file")

        db_file_path = os.path.join(settings.MEDIA_ROOT, file_object.name)
        f = open(db_file_path, mode="wb")
        for chunk in file_object.chunks():
            f.write(chunk)
        f.close()

        # 将文件路径写入到数据库
        models.UploadInfo_Form.objects.create(
            name=form.cleaned_data["name"],
            age=form.cleaned_data["age"],
            file=db_file_path,
        )
        # print(form.cleaned_data)
        return redirect("/upload/list/")
    return render(request, 'upload_form.html', {"title": title, "form": form})


def upload_modalform(request):
    title = "基于ModalForm上传文件"
    if request.method == 'GET':
        form = UploadModalForm()
        return render(request, "upload_form.html", {"title": title, "form": form})
    form = UploadModalForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/upload/list/")
    return render(request, "upload_form.html", {"title": title, "form": form})

def upload_list(request):
    upload_data = models.UploadInfo_ModalForm.objects.all()
    return render(request, "upload_list.html", {"upload_data": upload_data})

def upload_add(request):
    if request.method == "GET":
        upload_data = models.UploadInfo_ModalForm.objects.all()
        return render(request, "upload_list.html", {"upload_data": upload_data})
    return redirect("/upload/modalform/")
