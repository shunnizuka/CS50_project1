from django.shortcuts import render, redirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entryPage(request, title):
    return render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(title),
        "title": title
    })

def search(request):
    
    if request.method == "GET":
        query = request.GET.get('q')
        if(util.get_entry(query) != None):
            return redirect('title', query)
        else:
            entries = util.list_entries()
            searchResults = []
            for entry in entries:
                if query in entry:
                    searchResults.append(entry)
            return render(request, "encyclopedia/searchResults.html", {
                "entries": searchResults
            })
    return redirect('index')

