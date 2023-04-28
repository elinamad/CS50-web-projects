from django.shortcuts import render, redirect
import markdown

from . import util


# Convert markdown to HTML
def convert_markdown(title):
    content = util.get_entry(title)
    markdowner =  markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)
    

# List entry items in the index.html
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Render entry page if it exists
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

# Search functionality
def search(request):
    # if something was submitted in the search bar
    if request.method == "POST":
        query = request.POST['q']
        all_entries = util.list_entries()
        matching_entries = []

        #if any entries fully or partially match the query, add them to matching_entries list
        for entry in all_entries:
            if query.lower() in entry.lower():
                matching_entries.append(entry)

        # if there are matching entries
        if matching_entries:
            #if there is an exact match, redirect to the entry page 
            if query in matching_entries:
                return render(request, "encyclopedia/entry.html",{
                    "title":query,
                    "content":convert_markdown(query)
                })
            # if there are only partial matches, show a page with all results
            else:
                return render(request,"encyclopedia/search.html",{
                    "entries":matching_entries,
                    "query":query
                })
        # if there are no matches at all, show an error message
        else:
            return render(request,"encyclopedia/error.html",{
                "message":"No entries were found"
                
            })
        

            





