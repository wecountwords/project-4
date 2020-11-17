import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.decorators.csrf import csrf_exempt


from .models import User, Post, Follower, Like

# this renders the landing and All Post pages.  all users, logged-in or
# otherwsie can reach this page
def index(request):

    # get the full feed and then initialize the pagination
    full_feed = Post.objects.all().order_by('-timestamp')
    p = Paginator(full_feed, 10)

    # first all to the feed always goes to page 1
    if (request.GET.get('page') == None):
        page_number = 1
    else:
        page_number = request.GET.get('page')

    # define a page object, get the posts for the page
    page_obj = p.page(page_number)
    post_feed = p.page(page_number).object_list

    return render(request, "network/index.html", {
        "post_feed": post_feed,
        "page_title": "All Posts",
        "data_attr_posts": "all",
        "page_obj": page_obj
    })


# this renders the profile page for any given author who posts.  all users,
# logged-in or therwsie can reach their own profile page or other's profiles
def profile(request, author_id):
    # get the set of posts for this profile page along with the post author name
    # for the page title
    qset_posts = Post.objects.filter(author=author_id)
    qset_followers = Follower.objects.filter(author=author_id)
    qset_following = Follower.objects.filter(follower=author_id)
    profile_name = User.objects.get(id=author_id).username

    # if the request.user is following the  post author (profile), enable
    # the unfollow button
    try:
        Follower.objects.get(follower=request.user.id, author=author_id)
        data_attr_follow ='unfollow'
    except ObjectDoesNotExist:
        data_attr_follow = 'follow'

    # setup the paging mechanism
    full_feed = qset_posts.order_by('-timestamp')
    p = Paginator(full_feed, 10)

    # first all to the feed always goes to page 1
    if (request.GET.get('page') == None):
        page_number = 1
    else:
        page_number = request.GET.get('page')

    # define a page object, get the posts for the page
    page_obj = p.page(page_number)
    post_feed = p.page(page_number).object_list

    return render(request, "network/index.html", {
        "page_title": profile_name,
        "profile_name": profile_name,
        "post_feed": post_feed,
        "author_name": profile_name,
        "followers": qset_followers.count(),
        "following": qset_following.count(),
        "data_attr_follow": data_attr_follow,
        "data_attr_posts": profile_name
    })


# this renders the following page and is accessible only when the user
# is logged in. currently, users can only see their following page.
def following(request, username):

    # find the authors that the user is following and from that get the posts
    # for those authors

    # we'll use a list to hold the unique id for each post that will be
    # written to the following page
    post_list = []
    # now get the authors along with the author count
    followed_authors = Follower.objects.filter(follower=request.user)
    length_authors = followed_authors.count()

    # for each author, get the id's for their posts and store them in the
    # post_list
    for i in range(length_authors):
        followed_posts = Post.objects.filter(author=followed_authors[i].author)
        length_posts = followed_posts.count()
        for j in range(length_posts):
            post_list.append(followed_posts[j].id)

    # build the queryset
    posts = Post.objects.filter(id__in=post_list)

    # render the page
    return render(request, "network/index.html", {
        "post_feed": posts.order_by('-timestamp'),
        "page_title": "Following Posts",
        "data_attr_posts": "following",
        "count": posts.count(),
        "followed_posts": posts
    })



'''
api's
submit and retrieve information posts and users
'''
@csrf_exempt
@login_required
def submit_post(request):

    # check with Logan:  do I need to add additional security or will @login_required be sufficient
    # for this assigment.  Additional security can be found here:
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/

    # compose a new twitter-like post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # get the content, validate it, and format it as needed
    data = json.loads(request.body)
    text = data.get("text").strip()
    feed = data.get("feed").strip()

    # do we have a real user here? - not needed, we are posting based on the
    # authenticated user. and a user cannot be authenticated unless they are
    # first a user

    # get the user object, then save the post to the Post model
    author = request.user
    user = User.objects.get(username__iexact=author)
    try:
        p = Post(author=user, content=text)
        p.save()
        post_id = Post.objects.filter(author=user).latest('timestamp').values()
    except:
        return JsonResponse({
            "error": "post body cannot be empty or more than 280 chars."},
            status=400)

    return JsonResponse({
        "success": f"{post_id}"}, status = 200)


@csrf_exempt
@login_required
def get_post(request, post_id):

    # we will assume the id is coming in as a positive integer or
    try:
        qset = Post.objects.filter(pk=post_id)
        post = obj_to_posts(qset)
    except:
        return JsonResponse({
            "error": "no posts found."}, status=400)

    return JsonResponse(post, safe=False)


@login_required
def follow(request, authorid, isfollow):

    # a user cannot follow/unfollow themselves. exit with error if
    # author = follower
    if (int(authorid) == request.user.id):
        return JsonResponse({
            "error": "unable to follow self."}, status = 400)

    # initialize the user objects
    author_User = get_user_by_id(authorid)
    follower_User = get_user_by_id(request.user.id)

    # if isfollow is true, let's add a following relationship to the model
    if (isfollow == 'true'):
        try:
            f = Follower(follower=follower_User, author=author_User)
            f.save()
            return JsonResponse({
                "success": "add follower: everything looks good!"}, status = 200)
        except:
            return JsonResponse({
                "error": "add follower failed."}, status = 400)

    # if isfollow is false, remove the relationship from the model
    try:
        f = Follower.objects.get(author=author_User, follower=follower_User)
        f.delete()
        return JsonResponse({
            "success": "unfollow: everything looks good!"}, status = 200)
    except ObjectDoesNotExis:
        return JsonResponse({
            "error": "unfollow: unable to unfollow."}, status = 400)


# for the post with postid, if addlike is true, add the like relationship and
# increase the like count in the post model. otherwise, update the like
# relationship and decrease the like count unlike
def add_like(request, postid, addlike):

    # does the unique like-post relationship exist for this user?
    # first get validate the user and the post exist
    try:
        user_User = get_user_by_id(request.user.id)
        post_Post = Post.objects.get(pk=postid)
    except ObjectDoesNotExist:
        return JsonResponse({
                    "error": "unable to locate post -- line 238."}, status = 400)

    # is there a row in the Like model for this particular like?
    try:
        res = Like.objects.get(post_id=postid, user=user_User)
    except ObjectDoesNotExist:
        res = None
    except MultipleObjectsReturned:
        return JsonResponse({
            "error": "post-like row not unique -- line 247."}, status = 400)

    # add the new like relationship to the model if it's not there
    if (res == None):
        try:
            newlike = Like(post_id=postid, user=user_User, like=addlike)
            newlike.save()
        except:
            return JsonResponse({
                "error": f"unable to add like at this time -- line 256. user = {user_User} and post = {post_Post}"}, status = 400)

        # update the post like_count
        val = post_Post.like_count

        if (int(addlike) == 1):
            val = val + 1
        else:
            val = val - 1
        post_Post.like_count = val
        post_Post.save()

        # exit with success
        return JsonResponse(val, safe=False)

    # otherwise this like exists in the models and this must be an update
    res.like = int(addlike)
    res.save()

    # did we get a good save?
    if (Like.objects.get(post_id=postid, user=user_User).like != int(addlike)):
        return JsonResponse({
                "error": "database not updated successfully -- line 279."}, status = 400)

    # update the like_count on the post
    val = post_Post.like_count

    if (int(addlike) == 1):
        val = val + 1
    else:
        val = val -1

    post_Post.like_count = val
    post_Post.save()

    # exit with success
    return JsonResponse(val, safe=False)


# returns a comma delimited string of id's that are currently "liked"
def get_likes(request):
    currentLikes = ""
    # for the request user, get the post id's for likes / unlikes
    qset = Like.objects.filter(user_id=request.user.id)
    if (not qset):
        return JsonResponse(currentLikes, safe=False)

    # we have at least one like in the likes table for this user. next pull
    # the ids and get the posts

    for like in qset:

        currentLikes = currentLikes + "," + str(like.post_id)

    return JsonResponse(currentLikes[1:], safe=False)  #DEBUG

    qset_posts = Post.objects.filter(id__in=ids)
    return JsonResponse({
        "error": f"debug - qset_posts count = {qset_posts.values().count} -- line 311."}, status = 400)

    likes = obj_to_posts(qset)
    return JsonResponse(likes, safe=False)
    #return JsonResponse({"res": f"{likes}"}, status = 200)


'''
helper function for returning data to be processed in network.js
'''
def obj_to_posts(queryset):

    result = [['post_id', 'author', 'content', 'timestamp', 'likes']]
    for post in queryset:
        result.append([f'{post.id}', f'{post.author}', f'{post.content}', f'{post.timestamp}', f'{post.like_count}'])
    return result


'''
authentication: login, logout, & register
'''

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })

        # next add the author to the Follower table with a null
        #init_follower_model(user.id)

        # login and navigate to the landing page
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")



'''
Model helper functions
'''

def get_user_by_id(userid):
    uid = int(userid)
    try:
        return User.objects.get(pk=uid)
    except ObjectDoesNotExist:
        return None
