from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry_page(request, entry:str):
    entries = [en.upper() for en in util.list_entries()]
    if entry.upper() in entries:
        return render(
            request,
            "encyclopedia/entry.html",
            {"entry_name": entry, "entry": util.get_entry(entry)},
        )
    else:
        return render(
            request,
            "encyclopedia/error.html",
            {"error": 404, "error_message": f"The title '{entry}' does not exist."},
        )


def search(request):
    entry = request.GET.get("q")
    entries = util.list_entries()
    result = []
    if entry:
        for en in entries:
            if entry.upper() == en.upper():
                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[entry]))
            if entry.upper() in en.upper():
                result.append(en)
    if not result:
        return render(
            request,
            "encyclopedia/error.html",
            {"error": 404, "error_message": f"The title '{entry}' wasn't found."},
        )
    return render(request, "encyclopedia/search.html", {"entry": result})


def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        text = request.POST.get("textarea").encode("utf-8")
        entries = util.list_entries()
        exists = [en for en in entries if title.upper() == en.upper()]
        if not exists:
            if title and text:
                util.save_entry(title, text)
                return HttpResponseRedirect(reverse("encyclopedia:index"))
            else:
                return render(
                    request,
                    "encyclopedia/error.html",
                    {
                        "error": 400,
                        "error_message": "Must provide title and Markdown text.",
                    },
                )
        else:
            return render(
                request,
                "encyclopedia/error.html",
                {
                    "error": 400,
                    "error_message": f"The title '{exists[0]}' already exists",
                },
            )
    return render(request, "encyclopedia/create.html")


def edit(request, entry:str):
    entry_content = util.get_entry(entry)
    if request.method == "POST":
        new_content = request.POST.get("textMarkdown").encode("utf-8")
        if new_content:
            util.save_entry(entry, new_content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[entry]))
        else:
            return render(request, "encyclopedia/error.html", {
                "error": 400,
                "error_message": "Markdown text can't be blank"
            })
    return render(request, "encyclopedia/edit.html", {"entry": entry, "entry_content": entry_content})
