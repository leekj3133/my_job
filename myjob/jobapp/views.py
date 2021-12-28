from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect

from django.urls import reverse

from jobapp.models import Jobapp

def hello_job(request):

    if request.method == "POST":

        temp = request.POST.get("JOB INPUT")

        new_hello_job = Jobapp()
        new_hello_job.text = request.POST["text"]
        new_hello_job.save()
        return redirect("hello_job")
        # hello_job_list = Job.objects.all()
        # return HttpResponseRedirect(reverse('jopapp:hello_job'))
    else:
        hello_job_list = Jobapp.objects.all()
        return render(request,'jobapp/hello_job.html', {"job_list" : hello_job_list})

def result(request):
    if request.method == "GET":
        results = Jobapp.objects.all()
        data = {
            "result": results,
        }
        return render(request, "jobapp/job_list.html", data)
    elif request.method == "POST":
        results = Jobapp.objects.all()
        data = {
            "result": results,
        }
        return render(request, "jobapp/job_list.html", data)
    # db = {}
    # word = request.args.get("word")
    # if word:
    #     word = word.lower()
    #     existingJobs = db.get(word)
    #     searchingBy = word,
    #     resultNumber = len(jobs),
    #     jobs = jobs
    #     data = {
    #         "searchingBy" : searchingBy,
    #         "resultNumber" : resultNumber,
    #         "jobs" : jobs
    #     }
    #     if existingJobs:
    #         jobs = existingJobs
    #     else:
    #         so_jobs = get_so_jobs(word)
    #         wwr_jobs = get_wwr_jobs(word)
    #         remote_jobs = get_remote_jobs(word)
    #         jobs = so_jobs + wwr_jobs + remote_jobs
    #         db[word] = jobs
    # else:
    #     return redirect("/")
    # return render(request,
    #     "report.html",
    #     data)






