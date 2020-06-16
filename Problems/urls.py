"""MathProblems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include, re_path

from Problems.views import tasks_list, tasks_edit_task, tasks_create_task, tasks_delete_task, tasks_read_task, try_ajax, \
    tasks_list_edit_grid

urlpatterns = [
    # list
    path('list/', tasks_list, name='tasks_list'),
    path('list_edit_grid/', tasks_list_edit_grid, name='tasks_list_edit_grid'),
    # create
    path('create_task/', tasks_create_task, name='tasks_create_task'),
    # edit
    re_path(r'edit_task/(?P<task_id>\d+)/', tasks_edit_task, name='tasks_edit_task'),
    # delete
    re_path(r'delete_task/(?P<task_id>\d+)/', tasks_delete_task, name='tasks_delete_task'),
    # read
    re_path(r'read_task/(?P<task_id>\d+)/', tasks_read_task, name='tasks_read_task'),
    path('try_ajax', try_ajax, name='try_ajax'),
]
