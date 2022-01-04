from django.urls import path, re_path

from . import views


app_name = "jobapp"

urlpatterns = [
    path('', views.hello_job, name="hello_job"),
    path('job_list/', views.result, name="job_list"),
    re_path(r'^\D+/', views.send_file,name="send_file"),
]