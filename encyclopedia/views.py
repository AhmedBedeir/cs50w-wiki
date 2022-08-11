from ast import arg
from django.urls import reverse
from django.shortcuts import redirect, render
import markdown2
import random
from . import util
from .forms import newEntry,editEntry

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
#-----------------------------------------------------------
def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, 'encyclopedia/404.html')
    else:
        return render(request, 'encyclopedia/entry.html',{
            'content': markdown2.markdown(content),
            'title': title,
        })
#------------------------------------------------------------
def search(request):
    word = request.GET.get('q')
    allEntries = util.list_entries()
    result = []
    for entry in allEntries:
        if entry.lower() == word.lower():
            return redirect(reverse('entry', args=[word]))
        elif word.lower() in entry.lower():
            result.append(entry)
    if len(result) == 0:
        return render(request, 'encyclopedia/404.html')
    return render(request, 'encyclopedia/search.html',{
        "results": result,
    })
# -----------------------------------------------------------
def new(request):
    if request.method == 'POST':
        form = newEntry(request.POST)
        if form.is_valid():
            allData = form.cleaned_data
            newTitle = allData['title'].lower()
            for entry in util.list_entries():
                if entry.lower() == newTitle:
                    return render(request, 'encyclopedia/newEntry.html', {
                        'founded': True,
                        'entry': newTitle,
                    })
            util.save_entry(allData['title'], allData['content'])
            return redirect(reverse('entry', args=[allData['title']]))
        
        return render(request, 'encyclopedia/newEntry.html', {
            'founded': False,
            "form": form,
        })
    return render(request, 'encyclopedia/newEntry.html', {
            'founded': False,
            "form": newEntry(),
        })
#----------------------------------------------------------------
def edit(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, 'encyclopedia/404.html')
    if request.method == 'POST':
        form = editEntry(request.POST)
        if form.is_valid():
            dataForm = form.cleaned_data
            util.save_entry(title, dataForm['content'].encode())
            return redirect(reverse('entry', args=[title]))
    
    return render(request, 'encyclopedia/editEntry.html', {
        'title': title,
        'form': editEntry({"content": content})
    })
#-----------------------------------------------------------------
def randomEntry(request):
    allEntries = util.list_entries()
    index = random.randint(0, len(allEntries) - 1)
    choseEntry = allEntries[index]
    return redirect(reverse('entry', args=[choseEntry]))