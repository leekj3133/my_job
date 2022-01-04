from django.http import HttpResponse, HttpResponseRedirect,FileResponse,StreamingHttpResponse
from django.shortcuts import render,redirect
from crawling_job import crwler_job,DBtoCSV
from django.urls import reverse
from django.db.models import Q
from jobapp.models import GetInfo
import os

def hello_job(request):
    job_list = GetInfo.objects.order_by("title")
    context={"job_list": job_list}
    return render(request,"jobapp/hello_job.html",context)

def result(request):
    job_lists = GetInfo.objects.all()
    search_key = request.GET.get("search_key")
    if search_key:

        job_filter_list = job_lists.filter(Q(word__icontains=search_key))
        job_filter_list = job_filter_list.reverse()
        DBtoCSV(search_key)
        if job_filter_list.last() in job_lists:
            return render(request,"jobapp/job_list.html", {"search_job_list":job_filter_list})
        else:
            crwler_job(search_key)
    else:
        raise ValueError("The Search Key is invalid")
    return render(request,"jobapp/job_list.html", {"search_job_list":job_filter_list})

def send_file(request):
    # response = StreamingHttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="job.csv"'
    # rows = ("title {},company {}\n".format(row, row) for row in range(0, 100))
    # response.streaming_content = rows
    # return response
    import mimetypes
    import os, tempfile, zipfile
    from wsgiref.util import FileWrapper

    filename = "jobs.csv"  # Select your file here.
    download_name = "job.csv"
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(filename,"rb"),chunk_size), content_type=mimetypes.guess_type(filename)[0])
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = "attachment; filename=%s" % download_name
    return response

