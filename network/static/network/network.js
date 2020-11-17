// setting up some event listeners and some formatting to handle
// on the fly without fully reloading the page.

document.addEventListener('DOMContentLoaded', function() {

  // listen for a user submitting a post
  const postForm = document.querySelector('#submit_post');
  if (postForm) {
    postForm.addEventListener('click', () => {
      savePost(),
      document.querySelector('#new_post').value = ``,
      window.location.reload()
    });
  }


  // listen for a user to edit a post
  const editButtons = document.querySelectorAll(".edit");
  for(let button  of editButtons) {
    button.addEventListener("click", () => getPost(button.dataset.postid));
  }


  // listen for a click to toggle like/unlike for any post
  const likeBtn = document.querySelectorAll(".like");
  // console.log(`how many like buttons? ${likeBtn.length}`);
  for (let button of likeBtn) {
    button.addEventListener("click", () => toggleLike(button));
  }


  // listen for a click on the follow button on the profile page
  const followBtn = document.querySelector('.follow');
  if(followBtn) {
  //  console.log(`found follow buttons and links`);  // DEBUG statement
    followBtn.addEventListener("click", () => {
      // console.log(`data.follow is ${followBtn.dataset.follow}`), // DEBUG
      follow(
        /[0-9]+/.exec(window.location.pathname)[0],
        String(followBtn.dataset.follow).trim() === 'follow')
    });
  }

  displayLikes();
});


// savePost: saves a post from the post form to the server
// args: none
function savePost() {
  console.log(`entering the savePost fetch`);

  // retrieve the data from the form
  const postContent = document.querySelector('#new_post').value.trim();
  const postFeed = document.querySelector('.post_list').dataset.posts;
  console.log(`content: ${postContent}`);
  console.log(`feed: ${postFeed}`);
  console.log(`length = ${postContent.length}`);
  if (postContent.length > 280) {
    document.querySelector('.error_msg').innherHTML = ``;
    document.querySelector('.error_msg').innerHTML = `error: 280 chars max`;
  }

  // submit the POST request to the API via a fetch command
  fetch('/posts', {
    method: 'POST',
    body: JSON.stringify({
      text: postContent,
      feed: postFeed
    })
  })
  .then(response => {
    response.json()
    if (response.ok) {
      console.log(`response OK`);
    }
  })
  .then(result => {
    // print result
    console.log(result);
  });

  console.log(`=== exiting submit post ===`);
}


// -- first part of update post ---
// getPost: for a given post id, get a post from the server
// args: postId
// int postId - unique id of a post
function getPost(postId) {

 // put the text into the edit field
  selectorPath = `.text[data-postid="` + postId + `"]`;
  console.log(selectorPath);
  textObj = document.querySelector(selectorPath);
  console.log(textObj.innerHTML);
  editObj = document.querySelector('#new_post');
  editObj.innerHTML = textObj.innerHTML;
  editObj.focus();

  // open item -- send a put to the server to update the post.
  // current functionality -- update by adding a new post
}


// follow: for the given author, toggle between following and unfollowing
// args: author, isFollow
//   int author - the id of the member to follow
//   bool isFollow - true to follow and false to unfollow
function follow(authorID, isFollow) {

  // set the API path for this call
  const pathAPI = `/follow/${authorID}/${isFollow}/`;
  console.log(`path = ${pathAPI}`);

  // send the request to the server
  fetch(pathAPI)
  .then(response => {
    response.json()
    if (response.ok) {
      console.log(`response OK`);
    }
  })
  .then(result => {
    // print result
    console.log(result);
    // update the button realtime before page load
    const btn = document.querySelector('.follow');
    if (btn.dataset.follow === 'follow') {
      btn.setAttribute('data-follow', 'unfollow');
    } else {
      btn.setAttribute('data-follow', 'follow');
    }
  });
}


// toggleLike: for the given post, the button can toggle between "like" and
// "unlike".
// args: likeObj
//   html element - likeObj - the buton associated with post that will toggle
//   when the button has a value onclick "like", a like is associaed with
//   this post and the button is updated.  when the button has a value of
//   "unlike", this user does not have a like associated with the past.
function toggleLike(likeObj) {

  // let's find out if the user is liking or unliking with post then send
  // the correct params to the fetch
  var current_state;
  var next_state;

  if (likeObj.dataset.name.trim().toLowerCase() ==="like") {
    updateLike(likeObj.dataset.postid, 1);
    next_state = "unlike";
  } else {
    updateLike(likeObj.dataset.postid, 0);
    next_state = "like";
  }

  likeObj.dataset.name = next_state;
  likeObj.innerHTML = next_state.toUpperCase();
}


// updateLike updates like information serverside
// args postId, displayLike
// int postId = post id that will be liked
// int isLike = +1 indicates we add a like, 0 indicates we unlike
function updateLike(postId, isLike) {

  console.log(`entering -- updateLike -- function`)
  // from the boolean set the integer value for the fetch

  pathAPI = `posts/${parseInt(postId)}/${parseInt(isLike)}`;
  console.log(`pathAPI = ${pathAPI}`);

  fetch(pathAPI)
  .then(response => response.json())
  .then(result => {
    // update the like count for this like
    //print Likes
    console.log(result);
  });
}

// set the proper like / unlike display for this user. to do this, we need
// to get the postids for each post the user has "liked" and then toggle the
// like / unlike button if needed
function displayLikes() {
  var i;
  var likesArr;

  // reset everything all likes on the page to LIKE then go back and set the
  // UNLIKE
  const likeElements = document.querySelectorAll('.like');
  console.log(`length: ${likeElements.length}`)
  for (i = 0; i < likeElements.length; i++) {
      likeElements[i].dataset.name='like';
      likeElements[i].innerHTML=`like`;
  }

 // fetch the like of current likes for this user (this does not necessarily
 // scale. for larger sites, some sort of partition needs to be considered)
  console.log(`entering -- displayLikes -- function`);
  // get a list of post id's that are currently liked by the logged-in user
  pathAPI = `posts/likes`;
  console.log(`pathAPI = ${pathAPI}`);

  fetch(pathAPI)
  .then(response => response.json())
  .then(result => {
    console.log(result),
    likesArr = result.split(','),
    updateUnlike(likesArr)
  });
}

// helper function to update unlikes on the page
function updateUnlike(arrayOfElementIds) {
  var i;
  for (i = 0; i < arrayOfElementIds.length; i++) {
    selectorPath = ".like[data-postid='"+ arrayOfElementIds[i] + "']";
    console.log(`${selectorPath}`);
    if (document.querySelector(selectorPath)) {
      document.querySelector(selectorPath).dataset.name="unlike";
      document.querySelector(selectorPath).innerHTML=`unlike`;
    }
  }
}
