from django.urls import path
from . import views

urlpatterns = {
    path('', views.ListPost.as_view(), name='home'),
}
