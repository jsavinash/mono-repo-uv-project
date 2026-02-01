from item.src.models.common import DateTimeModelMixin, IDModelMixin
from item.src.models.domain.profiles import Profile
from item.src.models.domain.rwmodel import RWModel


class Comment(IDModelMixin, DateTimeModelMixin, RWModel):
    body: str
    author: Profile
