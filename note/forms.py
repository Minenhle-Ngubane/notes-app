from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Note


class NoteForm(forms.ModelForm):
    
    class Meta:
        model = Note
        fields = ["title", "description", "is_favourite"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update({
            "class": "form-control",
            "placeholder": _("e.g., Grocery List"),
        })

        self.fields["description"].widget.attrs.update({
            "class": "form-control",
            "rows": 5,
            "placeholder": _("Write your note here..."),
        })

        self.fields["is_favourite"].widget.attrs.update({
            "class": "form-check-input",
        })
        
        # Add error classes to fields with errors
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                # Remove existing form-control and add is-invalid
                current_classes = field.widget.attrs.get("class", "")
                new_classes = current_classes.replace("form-control", "form-control is-invalid")
                field.widget.attrs["class"] = new_classes
        