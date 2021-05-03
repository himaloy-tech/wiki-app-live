from django.shortcuts import render, HttpResponse, redirect
import markdown2
from django.contrib import messages
from . import util
from random import randint

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def details(request, title):
    """
    detail of an entry
    """
    detail = util.get_entry(title=title)
    if detail == None:
        return render(request, 'encyclopedia/results.html', {
            "results":[]
        })
    else:
        normal_text = markdown2.markdown(detail.rstrip())
        return render(request, 'encyclopedia/details.html', {
            "text":normal_text,
            "title":title
        })

def search(request):
    query = request.GET.get('q')
    result = util.get_entry(title=query)
    if result is not None:
        return redirect(f'/wiki/{query}')
    else:
        results = []
        for entry in util.list_entries():
            if query in entry:
                results.append(entry)
            else:
                continue
        return render(request, 'encyclopedia/results.html', {
            "results":results
        })
def create(request):
    """
    create a new page
    """
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if util.get_entry(title=title) is not None:
            messages.error(request, f"A entry with the name {title} already exists")
            return render(request, 'encyclopedia/add.html', {
                "title":title,
                "content":content
            })
        else:
            util.save_entry(title=title, content=content)
            return redirect(f'/wiki/{title}')
    return render(request, 'encyclopedia/add.html')

def edit(request, title):
    entry = util.get_entry(title=title)
    if entry is None:
        return render(request, 'encyclopedia/results.html', {
            "results":[]
        })
    else:
        return render(request, 'encyclopedia/edit.html', {
            "title":title, 
            "entry": entry 
        })
    
def save_edit(request):
    """
    save
    """
    title = request.GET.get('title')
    content = request.GET.get('content')
    util.save_entry(title=title, content=content)
    return redirect(f'wiki/{title}')

def random(request):
    entries = util.list_entries()
    choice = randint(0, len(entries))
    return redirect(f'/wiki/{entries[choice]}')