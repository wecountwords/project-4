# project-4
Build a Twitter-like social network app

**Design Decisions**
- Since this will be a twitter-like app, let's set a char limit to mirror the Twitter 280 max char limit for posts.
- For users that are not yet logged in, the following funcionality is available:
  - On the landing page (index.html), the "All Posts" feed should be visible."follow" and "like" buttons should be visible but disabled on each post. 
  - Clicking on he author's name on any post will take the user to the "All Posts" feel for that specific author. "follow" and "like" buttons will be disabled on each post.
  - Login & Register are also available through links on the top nav-bar.
- Upon login, users are taken to the landing page (index.html) with the following functionality:
  - "All Posts" feed should be visible. "follow" and "like" buttons are enabled on each post. Add new post form is visible and enabled.
  - The member's name should be visible in the nav-bar and clicking on the name will take the member to their profile page.
On the landing page, a user that is not logged-in will see all posts (the All Posts feed) however they will not be able to add, edit, or navigate to an poster's profile page. 
- From the landing page, a user that is not
- On the landing page, a user that is not logged-in will see both the Follow and Like buttons on each post but they will be taken login page if they opt to click on either of them
- A logged-in user will have access to the All Posts feed, a user-specific feed through the profile, and a feed that limits to posts to only those posters they are following.
- A logged-in is able to add a post from any view with a post feed.
- For a given post, each user can either "like" the post of "unlike" the post. But a single user cannot add multiple likes to a single post.

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
