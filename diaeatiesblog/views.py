from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from .models import Recipes
from .forms import CommentForm


class ListPost(generic.ListView):
    model = Recipes
    queryset = Recipes.objects.filter(status=1).order_by('-created_on')
    template_name = "index.html"
    paginate_by = 3


class RecipeDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Recipes.objects.filter(status=1)
        post_comment = get_object_or_404(queryset, slug=slug)
        recipe_comments = post_comment.comment.filter(approved=True).order_by('created_on')
        liked = False
        if post_comment.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "recipe_detail.html",
            {
                "post_comment": post_comment,
                "recipe_comments": recipe_comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post_comment(self, request, slug, *args, **kwargs):
        queryset = Recipes.objects.filter(status=1)
        post_comment = get_object_or_404(queryset, slug=slug)
        recipe_comments = post_comment.comment.filter(approved=True).order_by('created_on')
        liked = False
        if post_comment.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            recipe_comments = comment_form.save(commit=False)
            recipe_comments.post_comment = post_comment
            recipe_comments.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "recipe_detail.html",
            {
                "post_comment": post_comment,
                "recipe_comments": recipe_comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


class RecipeLike(View):
    def post_comment(self, request, slug):
        post_comment = get_object_or_404(Recipes, slug=slug)

        if post_comment.likes.filter(id=request.user.id).exists():
            post_comment.likes.remove(request.user)
        else:
            post_comment.likes.add(request.user)

        return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))


class CreateRecipe(CreateView):
    model = Recipes
    fields = ['recipe_title', 'author', 'featured_image', 'excerpt', 'content', 'status']
    template_name = 'recipe_user.html'

    def get_success_url(self):
        return reverse('recipe_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        print(form.cleaned_data)
        return super().form_valid(form)

