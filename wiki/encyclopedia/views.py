from django.shortcuts import render, redirect
import markdown

from . import util

def convert_markdown(title):
    content = util.get_entry(title)
    markdowner =  markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)
    


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if title:
        html_content = convert_markdown(title)
        if html_content == None:
            return render(request,"encyclopedia/error.html",{
                "message":"The requested page was not found."
            })
        else:
            return render(request, "encyclopedia/entry.html",{
                "title":title,
                "content":html_content
            })
    else:
        return redirect('index')




