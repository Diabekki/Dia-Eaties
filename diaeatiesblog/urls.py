from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ListPost.as_view(), name='home'),
    path('<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_detail'),
]
