from django.shortcuts import render, get_object_or_404
from .models import Blog

# Create your views here.

def home(request):
    blogs = Blog.objects
    return render(request, 'home.html', {'blogs': blogs})

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