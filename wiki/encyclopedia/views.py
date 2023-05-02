from django.shortcuts import render, redirect
import markdown
import random

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

# Search functionality.
# Fixes needed: Make search case insensitive. Make so that 'CSS' and 'css' and 'Css' are the same queries

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

# Create a new page
# Fixes needed: Case insensitivity. Make so that 'css' and 'CSS' and 'Css' are all counted as the same title.

def new(request):
    # open new page
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")

    # if submitting the content
    else:
        title = request.POST['title']
        content = request.POST['content']

        #check if the title already exists on the wiki
        check_title = util.get_entry(title)
        if check_title is not None:
            return render(request,"encyclopedia/error.html",{
                "message":"Page with this title already exsists"
            })
        #if page does not exists
        else:
            util.save_entry(title,content)
            html_content = convert_markdown(title)
            return render(request, "encyclopedia/entry.html",{
                "title":title,
                "content": html_content
            })
        
def edit(request,title):
    #open edit page
    if request.method == "GET":
        return render(request,"encyclopedia/edit.html",{
            "content": util.get_entry(title),
            "title": title
        })
    # save changes
    else:
        content = request.POST['content']
        util.save_entry(title,content)
        html_content = convert_markdown(title)
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "content":html_content
        })


def random_page(request):
    #populate list with all entries
    pages = util.list_entries()
    #randomize an index number
    index = random.randrange(len(pages))
    #select the page with the randomized index
    random_page = pages[index]

    #render the page
    html_content = convert_markdown(random_page)
    if html_content == None:
        return render(request,"encyclopedia/error.html",{
             "message":"The requested page was not found."
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "title":random_page,
            "content":html_content
         })


    
        

            





