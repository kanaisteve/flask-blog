function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likedButton = document.getElementById(`like-button-${postId}`);

    fetch(`/like-post/${postId}`, { method: "POST" })
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = data["likes"];
            if(data["liked"] === true) {
                likedButton.className ="fa-solid fa-thumbs-up";
            } else {
                likedButton.className = "fa-regular fa-thumbs-up"
            }
        })
        .catch((e) => alert("Could not like post.")); 

    
    // console.log(likeCount.value)
}

function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST', 
        body: JSON.stringify({ noteId: noteId })
    }).then((res) => {
        window.location.href = "/";
    })
}