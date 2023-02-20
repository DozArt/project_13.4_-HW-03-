from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilters
from .forms import PostForms


class PostList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news.html'
    context_object_name = 'all_news'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilters(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class ArticlesList(PostList):
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilters(self.request.GET, queryset)
        return self.filterset.qs.filter(essence='A')


class NewsList(PostList):
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilters(self.request.GET, queryset)
        return self.filterset.qs.filter(essence='N')


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


class PostCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForms
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.essence = 'A'
        print(post)
        return super().form_valid(form)


class NewsCreate(PostCreate):
    success_url = reverse_lazy('news_list')


class PostEdit(UpdateView):
    form_class = PostForms
    model = Post
    template_name = 'post_edit.html'


def News(request):
    return redirect('/news/')

# class NewsEdit(PostEdit):
#     success_url = reverse_lazy('one_news')
#
#
# class ArticlesEdit(PostEdit):
#     success_url = reverse_lazy('one_articles')


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
