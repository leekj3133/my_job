from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse

from jobapp.models import Job

def hello_job(request):

    if request.method == "POST":

        temp = request.POST.get("JOB INPUT")

        new_hello_job = Job()
        new_hello_job.text = temp
        new_hello_job.save()

        hello_job_list = Job.objects.all()
        return HttpResponseRedirect(reverse('jpbapp:hello_job'))
    else:
        hello_job_list = Job.objects.all()
        return render(request,'jobapp/hello_job.html', context = {"job_list" : hello_job_list})