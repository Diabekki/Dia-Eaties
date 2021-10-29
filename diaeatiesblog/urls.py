from . import views
from django.urls import path

urlpatterns = [
    path('create/', views.CreateRecipe.as_view(), name='create_recipe'),
    path('', views.ListPost.as_view(), name='home'),
    path('<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_detail'),
    path('like/<slug:slug>', views.RecipeLike.as_view(), name='recipe_like'),
]
