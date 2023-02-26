from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilters
from .forms import PostForms


class PostList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news.html'
    context_object_name = 'all_news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilters(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        # context['filterset'] = self.filterset
        context['essence'] = "новости и статьи"
        return context


class ArticlesList(PostList):
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilters(self.request.GET, queryset)
        return self.filterset.qs.filter(essence='A')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['essence'] = "статьи"
        return context


class NewsList(PostList):
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilters(self.request.GET, queryset)
        return self.filterset.qs.filter(essence='N')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['essence'] = "новости"
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'one_news.html'
    context_object_name = 'news'


class ArticlesDetail(PostDetail):
    def get_queryset(self):
        return Post.objects.filter(essence='A')


class NewsDetail(PostDetail):
    def get_queryset(self):
        return Post.objects.filter(essence='N')


class NewsSearch(ListView):
    model = Post
    ordering = '-date'
    template_name = 'search.html'
    context_object_name = 'search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilters(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = PostForms
    model = Post
    template_name = 'post_edit.html'


class NewsCreate(PostCreate):
    def form_valid(self, form):
        post = form.save(commit=False)
        post.essence = 'N'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('one_news', kwargs={'pk': self.object.id})


class ArticlesCreate(PostCreate):
    def form_valid(self, form):
        post = form.save(commit=False)
        post.essence = 'A'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('one_articles', kwargs={'pk': self.object.id})


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    raise_exception = True
    form_class = PostForms
    model = Post
    template_name = 'post_edit.html'


class NewsEdit(PostEdit):
    def get_success_url(self):
        return reverse('one_news', kwargs={'pk': self.kwargs['pk']})


class ArticlesEdit(PostEdit):
    def get_success_url(self):
        return reverse('one_articles', kwargs={'pk': self.kwargs['pk']})


def News(request):
    return redirect('/news/create/')


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
