from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Blog
from .forms import BlogUpdate
from django.core.paginator import Paginator

# Create your views here.

def home(request):
    blogs = Blog.objects.order_by('-id')
    blog_list = Blog.objects.all().order_by('-id')
    paginator = Paginator(blog_list, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'home.html', {'blogs': blogs, 'posts':posts})

def count(request):
    return render(request, 'count.html')

def word(request):
    full_text = request.GET['fulltext']
    word_list = full_text.split()
    word_dict = {}

    for word in word_list:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1

    return render(request, 'word.html', {'fulltext': full_text, 'total':len(word_list),
                                         'dictionary':word_dict.items()})

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'blog': blog_detail})

def create(request):
    return render(request, 'create.html')

def postcreate(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/detail/'+str(blog.id))

def update(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)

    if request.method == "POST":
        form = BlogUpdate(request.POST)
        if form.is_valid():
            blog.title = request.POST['title']
            blog.body = request.POST['body']
            blog.pub_date = timezone.datetime.now()
            blog.save()
            return redirect('/detail/' + str(blog_id))

    else:
        form = BlogUpdate(instance = blog)

        return render(request, 'update.html', {'form': form})

def delete(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    blog.delete()
    return redirect('/')