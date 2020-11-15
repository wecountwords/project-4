# project-4
Build a Twitter-like social network app

**Design Decisions: User Flow & Functionality**
- Since this will be a twitter-like app, let's set a char limit to mirror the Twitter 280 max char limit for posts.
- For users that are not yet logged in, the following funcionality is available:
  - On the landing page (index.html), the "All Posts" feed should be visible."follow" and "like" buttons should be visible but disabled on each post. 
  - Clicking on he author's name on any post will take the user to the "All Posts" feel for that specific author. "follow" and "like" buttons will be disabled on each post.
  - Login & Register are also available through links on the top nav-bar.
- Upon login, the following functionality is available:
  - After login, users are taken to the landing page (index.html) with the "All Posts" feed visible, all buttons enabled, and the "Add new post" form visible.
  - The logged-in user's name (the member) should be visible in the nav-bar. Clicking on it will take the member to their Profile page.
  - Clicking on an author name in the post will take the member to the profile page for that author.
  - Follow, Unfollow, and Like buttons are enabled on all pages.
- Profile pages are available only to logged-in members with the following functionality:
  - The author-specific "All-Posts" feed is visible along with the "followers" and "following" count for the author.
  - The "Add new post" form is available on this page.
- From the nav-bar on any page, the logged-in user can navigate the their "Following feed" which shows all posts from all post authors they are following.
- All views of posts are listed in reverse chronological order.
- A logged-in user should be able to add a post from any view with a post feed.
- For any post in the post feed, the member can like or unlike the post or follow a post author. An author can be un-followed only from their profile page. 

### Design Decisions: App Design
- Views
  
- Layout & Visibility
- Event Driven Actions

**Notes on Specs**
* **New Post** - logged in user should be able to write a new text-based post by filling in text into a textarea and then clicking a button to submit the post
  - **Implementation** 
  - Add New Post is a form that is visible for any logged in user on all pages with a "post feed" (i.e. list of posts).
  - The post is stored in the Post model where content is a CharField with max 280 char limit.
  - Post api takes the content and stores it in the model. Once stored it will show up in the feed when next th epage is reloaded.
  - Open item: reload on submit is not yet implemented.
* **All Posts** - the _All Posts_ link in the nav-bar should take the user to a page where they can see all posts from all users, with the most recent post first. Each post should include the Poster (author) username, the content itself, the date and time of the post, and the number of likes on the post.
  - **Implementation** 
  - The nav-bar contains a link to the _All Posts_ feed and the link is available to all users, logged-in or otherwise, from all non-login related views. 
  - The _All Posts_ feed is rendered on index.html. Rendering and formatting is handled via the Django template for index.html. 
  - Each post is a bootstrap card and contains the author name, follow link, and like link in the card header. 
  - The card body contains the post date and content along with the like count.
* **Profile Page** - clicking on a username from the nav-bar or from any of the posts will load that user's profile page. The page should display the number of followers the user has, the number of people the user is following, all posts by that user (reverse chronological order), along with the follow / unfollow button for everyone except the post author.
  - **Implementation** 
  - the Profile page uses the same template as _All Posts_. The posts delivered to the template are only those of the profile author. 
  - three stats are listed at the top of page after the author's name: total posts, followers, following.
  - this page is available for both users that are not logged-in and logged-in users.
  - the follow link is live on all posts for logged-in users other than that profile author.

**References**
* Course lectures, notes, previous assignments, and assigment solutions posted by Teaching Fellows
* Reference guides for Django & Python
  - Django documentation : https://docs.djangoproject.com/en/3.1/ 
  - Python documentation : https://www.python.org/doc/
* Reference guides for HTML, CSS, & JavaScript: 
  - W3Schools.org : https://www.w3schools.com
  - MDN Web Docs: https://developer.mozilla.org/en-US/
* Color Picker : https://www.w3schools.com/colors/colors_monochromatic.asp
* Twitter API Reference : https://developer.twitter.com/en/docs/twitter-api/api-reference-index
* API Design Guidance & Naming Conventions:
  - Google API Design Guide : https://cloud.google.com/apis/design
  - Microsoft Web API Design : https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design
* W3.org HTTP Status Code Reference : https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
* Updating a portion of a page without reloading entire page with Django & JavaScript:
  - https://forum.djangoproject.com/t/changing-template-without-reloading-entire-page/3538/2
