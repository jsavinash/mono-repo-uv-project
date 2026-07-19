class TimestampMixin:
    """Mixin that provides created_at and updated_at fields."""

    @classmethod
    def setup_timestamp_fields(cls, model_class):
        from django.db import models

        if not hasattr(model_class, "created_at"):
            model_class.add_to_class(
                "created_at",
                models.DateTimeField(auto_now_add=True),
            )
        if not hasattr(model_class, "updated_at"):
            model_class.add_to_class(
                "updated_at",
                models.DateTimeField(auto_now=True),
            )
