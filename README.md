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

**Design Decisions: App Design**
- Pages & APIs
- Layout & Visibility
- Event Driven Actions

**Notes on Specs**
* New Post:  logged in user

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
