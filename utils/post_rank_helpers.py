import re
# local
from posts.api.serializers import PostBaseSerializer


CREDIBILITY_WORDS = [
    'documentation', 'source', 'reference', 'references', 'citation', 'citations',
]


def count_syllables(word):
    syllables = re.findall(r'[^aeiou]+[aeiou]*|[aeiou]+', word)
    return len(syllables)


def calculate_readability(text):
    sentences = text.split('.')
    words = text.split(' ')

    num_sentences = len(sentences)
    num_words = len(words)

    num_syllables = sum([count_syllables(word) for word in words])
    avg_syllables = num_syllables / num_words

    # calculate the readability score using the Flesch-Kincaid formula
    # https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests

    score = 206.835 - 1.015 * \
        (num_words / num_sentences) - 84.6 * avg_syllables

    return score


def calculate_quality(post):
    quality = 0

    length = len(post['content'])

    if length > 500:
        quality += 5
    elif length > 250:
        quality += 3

    for word in CREDIBILITY_WORDS:
        if word in post['content']:
            quality += 2

    readability = calculate_readability(post['content'])

    if readability > 60:
        quality += 5
    elif readability > 50:
        quality += 3

    return quality


def rank_posts(posts, start_date, end_date):
    """
    Ranks the posts according to freshness, relevance and quality. For freshness, we use the
    time since the post was created. For relevance, we use the number of votes, share and comments.
    For quality, we use the length of the post, the number of credibility and the readability.
    """

    filtered_posts = posts.filter(created_at__range=[start_date, end_date])

    # sorting the post by freshness
    sorted_posts = filtered_posts.order_by('-created_at')

    # convert to json serializable data
    sorted_posts = PostBaseSerializer(sorted_posts, many=True).data

    # assigning base score to each post based on the freshness
    for i in range(len(sorted_posts)):
        sorted_posts[i].score = len(sorted_posts) - i

    # adjusting the score based on engagements
    for post in sorted_posts:

        # calculating the engagement score
        score = post['upvote_count'] * 2
        score += post['downvote_count'] * -1.5
        score += post['comment_count'] * 1.5
        score += post['share_count'] * 0.5

        score += calculate_quality(post)

        # adjusting the score based on the engagement score
        post.score = post.score + score

    # sorting the posts based on the score
    sorted_posts = sorted(
        sorted_posts, key=lambda post: post.score, reverse=True
    )

    return sorted_posts
