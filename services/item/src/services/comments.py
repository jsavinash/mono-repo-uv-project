from item.src.models.domain.comments import Comment
from item.src.models.domain.users import User


def check_user_can_modify_comment(comment: Comment, user: User) -> bool:
    return comment.author.username == user.username
