

function likehandler(id,likedposts){
    var liked
    likecounter = document.getElementById(`${id}-likes`)
    icon = document.getElementById(`${id}`);
    fetch('/getlikedposts')
    .then(response => response.json())
    .then(data => {
        likedposts = data.likedposts;
        if(likedposts.indexOf(id) >= 0){
            //if post is liked
            liked = true;
            icon.src = likeimage
            console.log(`liked:${liked}`)
    
        }else{
            //if post is not liked
            liked = false;
            icon.src = likedimage
            console.log(`liked:${liked}`)
     
        }
        console.log(`start like:${liked}`)
        if (liked == true){
            //unlike
            fetch(`/removelike/${id}`)
            .then(response => response.json())
            .then(result => {
                console.log(result.message)
                icon.src = likeimage
                liked = false
                fetch('/getlikedposts')
                .then(response => response.json())
                .then(data => {
                    likedposts = data.likedposts;
                    console.log(likedposts)
                    console.log(`liked:${liked}`)
                    console.log("unlike function done")
                })
                likecounter.innerHTML = parseInt(likecounter.innerHTML) - 1
            })
            
    
        }else{
            //like
            fetch(`/addlike/${id}`)
            .then(response => response.json())
            .then(result => {
                console.log(result.message)
                icon.src = likedimage
                liked = true
    
                fetch('/getlikedposts')
                .then(response => response.json())
                .then(data => {
                    likedposts = data.likedposts
                    console.log(likedposts)
                    console.log(`liked:${liked}`)
                    console.log("like function done")
                })
            })
            likecounter.innerHTML = parseInt(likecounter.innerHTML) + 1
            
        }
    })
  
}
function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
}

function edit(id){
    fetch(`edit/${id}`)
    .then(response => response.json())
    .then(result => {
        console.log(result)
        let content = document.getElementById(`content-${id}`);
        content.innerHTML = "";
        const input = document.createElement('form');
        input.className = "form-group";
        content.append(input);
        const textarea = document.createElement("textarea");
        textarea.className = "form-control";
        textarea.value = result.post;
        input.append(textarea);
        const apply = document.createElement("p");
        apply.classList.add("btn");
        apply.classList.add("btn-primary");
        apply.innerHTML ="Apply changes";
        input.append(apply);
        input.append(textarea);
        apply.addEventListener('click',function(){
            let newpost = textarea.value
            const csrftoken = getCookie('csrftoken')
            fetch(`edit/${id}`,{
                method:'PUT',
                headers: {"content-type":"application/json","X-CSRFToken":csrftoken},
                body: JSON.stringify({
                    post:newpost
                })
            })
            .then(response => response.json())
            .then(result =>{
                console.log(result)
            })
            content.innerHTML = "";
            const posttext = document.createElement("h4");
            posttext.innerHTML = newpost;
            content.append(posttext);
        })
    })

    


}


