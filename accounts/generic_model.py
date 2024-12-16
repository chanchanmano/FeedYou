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
        return super().save(force_insert, force_update, using, update_fields)
