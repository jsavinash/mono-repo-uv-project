from typing import List

from item.src.models.common import DateTimeModelMixin, IDModelMixin
from item.src.models.domain.profiles import Profile
from item.src.models.domain.rwmodel import RWModel


class Article(IDModelMixin, DateTimeModelMixin, RWModel):
    slug: str
    title: str
    description: str
    body: str
    tags: List[str]
    author: Profile
    favorited: bool
    favorites_count: int
