from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.

def index(request):
    job_list = Job.objects.all()
    context={"job_list":job_list}
    return render(request,'job/inxex.html',context)