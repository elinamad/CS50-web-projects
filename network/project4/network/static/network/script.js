

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

