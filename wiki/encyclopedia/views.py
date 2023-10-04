from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry_page(request, entry):
    return render(
        request,
        "encyclopedia/entry.html",
        {"entry_name": entry, "entry": util.get_entry(entry)},
    )


def search(request):
    entry = request.GET.get("q").upper()
    entries = util.list_entries()
    entries_upper = [en.upper() for en in entries]
    if entry in entries_upper:
        return HttpResponseRedirect(reverse("encyclopedia:entry", args=[entry]))
    else:
        if entry:
            result = [en for en_up, en in zip(entries_upper, entries) if entry in en_up]
        else:
            result = None
        return render(request, "encyclopedia/search.html", {"entry": result})


