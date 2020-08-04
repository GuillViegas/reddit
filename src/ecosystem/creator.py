from post.models import Post


def createEcosystem(post_id, max_interactions=None):
    seed = Post.objects.get(id=post_id)
    comments = []
    posts = [seed]
    users = [seed.author]
    interactions = 0

    while(True):


        instections += 1


    pass
