from typing import Iterable

from django.db import models


class GenericModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True

    def save(
        self,
        force_insert: bool = ...,
        force_update: bool = ...,
        using: str | None = ...,
        update_fields: Iterable[str] | None = ...,
    ) -> None:
        self.before_save()
        super().save(force_insert, force_update, using, update_fields)
        self.after_save()

    def after_save(self, *args, **kwargs) -> None:
        """Override this method in model to control after save"""
        pass

    def before_save(self, *args, **kwargs) -> None:
        """Override this method in model to control before save"""
        pass
