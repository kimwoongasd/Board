from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Blog,Comment
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
    blog.user = request.user
    blog.title = request.POST['title']
    blog.body = request.POST['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()

    if not request.FILES:
        blog.images = ""
        blog.save()
    else:
        blog.images = request.FILES['images']
        blog.save()

    return redirect('/detail/'+str(blog.id))

def update(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)

    if request.method == "POST":
        form = BlogUpdate(request.POST)
        if form.is_valid():
            blog.title = request.POST['title']
            blog.body = request.POST['body']
            blog.images = request.FILES['images']
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

def search(request):
    blogs = Blog.objects.all().order_by('-id')

    q = request.POST.get('q', "")

    if q:
        blogs = blogs.filter(title__icontains=q)
        return render(request, 'search.html', {'blogs': blogs, 'q': q})

    else:
        return render(request, 'search.html')

def newreply(request, blog_id):
    if request.method == 'POST':
        comment = Comment()
        comment.comment_body = request.POST['comment_body']
        comment.blog = Blog.objects.get(pk=blog_id)  # id로 객체 가져오기
        comment.save()
        return redirect('/detail/' + str(comment.blog.id))

def likes(request, blog_id):
    like_b = get_object_or_404(Blog, id=blog_id)
    if request.user in like_b.like.all():
        like_b.like.remove(request.user)
        like_b.like_count -= 1
        like_b.save()
    else:
        like_b.like.add(request.user)
        like_b.like_count += 1
        like_b.save()
    return redirect('/detail/' + str(blog_id))
