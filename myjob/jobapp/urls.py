from django.urls import path

from . import views


app_name = "jobapp"

urlpatterns = [
    path('', views.hello_job, name="hello_job"),
    path('job_list/', views.result, name="job_list"),
]