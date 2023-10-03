from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entry):
    return render(request, "encyclopedia/entry.html", {
        "entry_name": entry,
        "entry": util.get_entry(entry)
    })
