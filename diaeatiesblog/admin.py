from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Recipes, Comment


@admin.register(Recipes)
class RecipesAdmin(SummernoteModelAdmin):
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('recipe_title',)}
    summernote_fields = ('content')
    list_display = ('recipe_title', 'slug', 'status', 'created_on')
    search_fields = ['recipe_title', 'content']


@admin.register(Comment)
class CommentRecipes(admin.ModelAdmin):
    list_display = ('name', 'body', 'post_comment', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comment']

    def approve_comment(self, request, queryset):
        queryset.update(approved=True)
