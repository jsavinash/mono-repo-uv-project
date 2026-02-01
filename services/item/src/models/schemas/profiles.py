from pydantic import BaseModel

from item.src.models.domain.profiles import Profile


class ProfileInResponse(BaseModel):
    profile: Profile
