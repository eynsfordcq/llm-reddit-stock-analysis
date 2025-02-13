from pydantic import BaseModel
from typing import List, Optional


class Comment(BaseModel):
    author: Optional[str]
    body: Optional[str]
    score: Optional[int]
    replies: Optional[List['Comment']] 

    class Config:
        from_attributes = True

class RedditPost(BaseModel):
    title: Optional[str]
    url: Optional[str]
    score: Optional[int]
    comments: Optional[List[Comment]]

class SubredditData(BaseModel):
    subreddit: str
    posts: Optional[List[RedditPost]]