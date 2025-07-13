import uuid

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Note(models.Model):
    
    id = models.UUIDField(
        _("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Unique identifier for the note.")
    )
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notes",
        help_text=_("The user who owns this note."),
    )

    title = models.CharField(
        _("Title"),
        max_length=255,
        help_text=_("Enter a short, descriptive title for the note.")
    )

    description = models.TextField(
        _("Description"),
        blank=True,
        help_text=_("Enter the detailed content of the note.")
    )

    is_favourite = models.BooleanField(
        _("Is Favourite"),
        default=False,
        help_text=_("Mark this note as a favourite.")
    )

    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True,
        help_text=_("The date and time when the note was created.")
    )

    updated_at = models.DateTimeField(
        _("Last Updated"),
        auto_now=True,
        help_text=_("The date and time when the note was last modified.")
    )

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("notes:detail", kwargs={"pk": self.pk})