# project-4
Build a Twitter-like social network app

**Design Decisions**
- Since this will be a twitter-like app, we will keep the twitter 280 max char limit for posts.
- On the landing page, a user that is not logged-in will see all posts (the All Posts feed) however they will not be able to add, edit, or navigate to an poser's profile page. 
- On the landing page, a user that is not logged-in will see both the Follow and Like buttons but they will be taken login page if they opt to click on either of them
- A logged-in user will have access to the All Posts feed, a user-specific feed through the profile, and a feed that limits to posts to only those posters they are following.
- A logged-in is able to add a post from any view with a post feed

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
