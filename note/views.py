import re
import json

from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from django.utils.timezone import now
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect

from .models import Note
from .forms import NoteForm


class NoteListView(LoginRequiredMixin, View):
    """
    Display a list of all notes belonging to the logged-in user.
    """
    def get(self, request):
        form = NoteForm()
        notes = Note.objects.filter(owner=request.user).order_by("-updated_at")
        return render(
            request, 
            "note/index.html", 
            {
                "notes": notes,
                "form": form,
                "title": "Notes"
            }
        )


class NoteDetailView(LoginRequiredMixin, View):
    """
    Display the details of a specific note.
    """
    def get(self, request, pk):
        note = get_object_or_404(Note, pk=pk, owner=request.user)
        return render(request, "note/note_detail.html", {"note": note})


class NoteCreateView(LoginRequiredMixin, View):
    """
    Handle creation of a new note.
    """
    def post(self, request):
        form = NoteForm(request.POST)
        
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.save()

            # Success message and updated list
            message = _("New note was created successfully.")
            notes = Note.objects.filter(owner=request.user).order_by("-updated_at")

            # Return new note partial (HTMX target)
            response = render(
                request,
                "note/partials/note_list.html",
                {
                    "notes": notes,
                }
            )
            
            response.status_code = 201  # HTTP 201 Created
            response["HX-Reswap"] = "innerHTML"
            response["HX-Retarget"] = f"#note-list"
            response["HX-Trigger"] = json.dumps({
                "noteCreated": {
                    "message": str(message)
                } 
            })

            return response

        # If form is invalid, return the form partial with errors
        response = render(
            request,
            "note/partials/create_note_form.html",
            {"form": form}
        )
        response.status_code = 400  # HTTP 400 Bad Request
        response["HX-Reswap"] = "outerHTML"
        response["HX-Retarget"] = f"#note-create-form"
        return response


class NoteUpdateView(LoginRequiredMixin, View):
    """
    Handle updating an existing note.
    """
    def get(self, request, pk):
        note = get_object_or_404(Note, pk=pk, owner=request.user)
        form = NoteForm(instance=note)
        
        return render (
            request,
            "note/partials/edit_note_form.html",
            {
                "form": form, 
                "note": note,
            }
        )
        
    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk, owner=request.user)
        form = NoteForm(request.POST, instance=note)
        
        if form.is_valid():
            note = form.save()
            message = _("Note updated successfully.")

            # Return new note partial (HTMX target)
            response = render(
                request,
                "note/partials/note_item.html",
                {"note": note}
            )
            
            response.status_code = 201  # HTTP 201 Updated
            response["HX-Reswap"] = "outerHTML"
            response["HX-Retarget"] = f"#note-{note.id}"
            response["HX-Trigger"] = json.dumps({
                "noteUpdated": {
                    "message": str(message), 
                    "noteId": str(note.id)
                } 
            })
            return response
          
        # If form is invalid, return the form partial with errors
        response = render(
            request,
            "note/partials/edit_note_form.html",
            {
                "form": form,
                "note": note
            }
        )
        response.status_code = 400  # HTTP 400 Bad Request
        response["HX-Reswap"] = "outerHTML"
        response["HX-Retarget"] = f"#edit-note-form-{note.id}"
        return response


class NoteDeleteView(LoginRequiredMixin, View):
    """
    Handle deletion of a note.
    """
    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk, owner=request.user)
        note.delete()
        notes = Note.objects.filter(owner=request.user).order_by("-updated_at")
        message = _("Note deleted successfully.")
        
        response = render(
            request,
            "note/partials/note_list.html",
            {
                "notes": notes
            }
        )
        
        response.status_code = 201  # HTTP 201 Deleted
        response["HX-Trigger"] = json.dumps({
            "noteDeleted": {
                "message": str(message), 
            } 
        })
        
        return response


class FavouriteNoteListView(LoginRequiredMixin, View):
    """
    Display a list of favourites notes belonging to the logged-in user.
    """
    def get(self, request, is_favourite):
        
        if bool(is_favourite):
            notes = Note.objects.filter(owner=request.user, is_favourite=True).order_by("-updated_at")
        else:
            notes = Note.objects.filter(owner=request.user).order_by("-updated_at")
               
        return render(
            request,
            "note/partials/note_list.html",
            {
                "notes": notes
            }
        )     
  
        
class NoteFavoriteToggleView(LoginRequiredMixin, View):
    """
    Handle toggling favorite status of a note.
    """
    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk, owner=request.user)
        
        # Toggle the favorite status
        note.is_favourite = not note.is_favourite
        note.save(update_fields=['is_favourite'])

        return render(
            request,
            "note/partials/note_item.html",
            {
                "note": get_object_or_404(Note, pk=pk)
            }
        )
        
 
class NoteSearchView(LoginRequiredMixin, View):
    
    @staticmethod
    def highlight_query(text, query):
        if not query:
            return text
        # Escape regex special chars in query
        pattern = re.escape(query)
        highlighted = re.sub(
            pattern,
            lambda m: f"<mark>{m.group(0)}</mark>",
            text,
            flags=re.IGNORECASE
        )
        return mark_safe(highlighted)


    def get(self, request, *args, **kwargs):
        query = request.GET.get("search", "")
        all_notes = Note.objects.filter(owner=request.user).order_by("-updated_at")
        
        if query:
            notes = all_notes.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
            ).distinct()
            
            # Highlight results
            for note in notes:
                note.title = self.highlight_query(note.title, query)
                note.description = self.highlight_query(note.description, query)

        else:
            notes = all_notes
            
            
        if query and not notes.exists():
            no_results_message = mark_safe(f'No notes found matching <mark>{query}</mark>.')
        else:
            no_results_message = None
            
        return render(
            request, 
            "note/partials/note_list.html",
            {
                "notes": notes, 
                "no_results_message": no_results_message
            }
        )       