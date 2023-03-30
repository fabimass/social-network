
def addLikesInfo(posts, user):
    modifiedPosts = []
    for post in posts:
        modifiedPosts.append({
            "data": post,
            "liked": post.is_liked_by(user)
        })
    return modifiedPosts