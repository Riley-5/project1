from django.shortcuts import render
from django.http import HttpResponse

from . import util
import markdown2
from django.http import Http404
from django.http import HttpResponseRedirect
from django import forms
import random
from django.urls import reverse

class NewSearchForm(forms.Form):
    search_item = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': "Search Encyclopedia"}), label = "") #TODO check if "search item" in original page

class CreateNewPage(forms.Form):
    title = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': "Title of Web Page"}), label = "")
    markdown_content = forms.CharField(widget = forms.Textarea(), label = "Enter Markdown Content for Page")

class EditPage(forms.Form):
    edit_contents = forms.CharField(widget = forms.Textarea(), label = "")

def index(request): 
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

def wiki(request, title):
    if title in util.list_entries(): #if title in list of entires show contents
        return render(request, "encyclopedia/wiki_page.html", {
            "title": title,
            "content": markdown2.markdown(util.get_entry(title)),
            "form": NewSearchForm()
        })
    else: # return error page indicating that page was not found
        raise Http404("Requested Page Not Found")

def search(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search_item = form.cleaned_data["search_item"]
            entry_exist = util.get_entry(search_item)

            if entry_exist:
                return render(request, "encyclopedia/wiki_page.html", {
                    "form": NewSearchForm(),
                    "title": search_item,
                    "content": markdown2.markdown(entry_exist)
                })
            else:
                related_search = []
                for name in util.list_entries():
                    if search_item.lower() in name.lower() or name.lower() in search_item.lower():
                        related_search.append(name)

                return render(request, "encyclopedia/search_results.html", {
                    "title": "Search Results",
                    "form": NewSearchForm,
                    "search_content": related_search
                })

    return render(request, "encyclopedia/wiki_page.html",{
        "form": NewSearchForm(),
        "content": "No Results",
        "title": "No Results"
    })

def create_new_page(request):
    return render(request, "encyclopedia/create_new_page.html", {
        "create_new_page": CreateNewPage(),
        "form": NewSearchForm()
    })

def new_page(request):
    if request.method == "POST":
        form = CreateNewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            markdown_content = form.cleaned_data["markdown_content"]
            if title in util.list_entries():
                raise Http404("Name Already Taken")
            else:
                util.save_entry(title, markdown_content)
                return render(request, "encyclopedia/new_page.html", {
                    "form": NewSearchForm(),
                    "title": title,
                    "content": markdown2.markdown(markdown_content)
                })
        else:
            return render(request, "encyclopedia/create_new_page.html", {
                "create_new_page": form
            })
    return render(request, "encyclopedia/create_new_page.html", {
        "create_new_page": CreateNewPage()
    })

def random_page(request):
    rpage = random.choice(util.list_entries())
    return render(request, "encyclopedia/wiki_page.html", {
        "title": rpage,
        "content": markdown2.markdown(util.get_entry(rpage)),
        "form": NewSearchForm()
    })

def edit_page(request, title):
    return render(request, "encyclopedia/edit_page.html", {
    "form": NewSearchForm(),
    "title": title,
    "edit": EditPage(initial = {"edit_contents": util.get_entry(title)})
    })

def save_edit(request, title):
    if request.method == "POST":
        form = EditPage(request.POST or None)
        if form.is_valid():
            edit_contents = form.cleaned_data["edit_contents"]
            util.save_entry(title, edit_contents)
            edited = util.get_entry(title)
            return render(request, "encyclopedia/save_edit.html", {
                "form": NewSearchForm,
                "title": title,
                "edited": markdown2.markdown(edited)
            })