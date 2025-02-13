import logging
import requests
import time
from models.reddit import SubredditData, RedditPost, Comment


def fetch_top_posts(subreddit: str, limit: int = 20) -> SubredditData:
    try:
        url = f"https://www.reddit.com/r/{subreddit}/top.json?t=day&limit={limit}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        data = response.json()
        
        logging.info(f"fetch_top_posts(): successfully fetched {url}")
        logging.info(
            f"rate_limit_used: {response.headers["x-ratelimit-used"]}. "
            f"rate_limit_remaining: {response.headers["x-ratelimit-remaining"]}. "
            f"rate_limit_reset: {response.headers["x-ratelimit-reset"]}. "
        )

        posts = []
        for post in data["data"]["children"]:
            post_id = post["data"].get("id")
            post_title = post["data"].get("title")
            post_score = post["data"].get("score")
            post_url = f"https://www.reddit.com{post['data']['permalink']}"

            top_comments = _fetch_comments(post_id, subreddit)
            posts.append(RedditPost(
                title=post_title,
                url=post_url,
                score=post_score,
                comments=top_comments
            ))

            time.sleep(1)

        return SubredditData(subreddit=subreddit, posts=posts)
    
    except Exception as e:
        logging.error(f"fetch_top_posts() error: subreddit: {subreddit}: error: {e}")


def _fetch_comments(post_id: dict, subreddit: str):
    try:
        comments_url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json?limit=10"
        comments_response = requests.get(comments_url, headers={"User-Agent": "Mozilla/5.0"})
        comments_data = comments_response.json()

        if not comments_data or len(comments_data) < 1:
            return []

        top_comments = []
        for comment in comments_data[1]["data"]["children"]:
            if not comment["data"].get("body"): 
                continue

            _comment = _process_comments(comment)
            top_comments.append(_comment)
        
        logging.info(
            f"fetch_comments(): "
            f"url: {comments_url} "
            f"success."
        )
        return top_comments
    
    except Exception as e:
        logging.error(
            f"fetch_comments() error: "
            f"url: {comments_url}. "
            f"error: {e}.",
            exc_info=True
        )
        return []
        
def _process_comments(comment: dict) -> Comment:
    _comments = []
    _replies = comment["data"].get("replies")
    if _replies:
        for reply in _replies["data"]["children"]:
            _comments.append(_process_comments(reply))

    return Comment(
        author=comment["data"].get("author"),
        body=comment["data"].get("body"),
        score=comment["data"].get("score"),
        replies=_comments
    )