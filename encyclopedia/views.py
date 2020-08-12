from django.shortcuts import render, redirect
from django import forms

import random
import markdown2

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Body")

class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Body")

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
                if query in entry.lower():
                    searchResults.append(entry)
            return render(request, "encyclopedia/searchResults.html", {
                "entries": searchResults
            })
    return redirect('index')

def createEntry(request):
    if request.method == "POST":
        entryForm = NewEntryForm(request.POST)

        if entryForm.is_valid():
            title = entryForm.cleaned_data["title"]
            content = entryForm.cleaned_data["content"]
            
            if(util.get_entry(title) != None):
                return render(request, "encyclopedia/entryExistsErrorPage.html", {
                    "title": title
                })
            else :
                util.save_entry(title, content)
                return redirect('title', title)
    else:
        return render(request, "encyclopedia/createNewPage.html", {
        "form": NewEntryForm()
    })

def editEntry(request, title):
    entry = util.get_entry(title)

    if request.method == "POST":
        editForm = EditEntryForm(request.POST)
        if editForm.is_valid():
            content = editForm.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('title', title)
        else:
            return render(request, "encyclopedia/editPage.html", {
                "title": title,
                "form": EditEntryForm(initial={'content': entry})
            })

    else:
        return render(request, "encyclopedia/editPage.html", {
            "title": title,
            "form": EditEntryForm(initial={'content': entry})
        })

def randomPage(request):
    entries = util.list_entries()
    randomEntry = random.choice(entries)
    return redirect('title', randomEntry)
