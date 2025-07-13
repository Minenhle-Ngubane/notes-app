import json

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string


from .models import Note
from .forms import NoteForm


class NoteListView(LoginRequiredMixin, View):
    """
    Display a list of all notes belonging to the logged-in user.
    """
    def get(self, request):
        form = NoteForm()
        notes = Note.objects.filter(owner=request.user).order_by("-updated_at")
        return render(request, "note/index.html", {"notes": notes, "form": form})


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
            message = _("Your note was created successfully.")
            notes = Note.objects.filter(owner=request.user).order_by("-updated_at")

            # Return new note partial (HTMX target)
            response = render(
                request,
                "note/partials/note_list.html",
                {"notes": notes}
            )
            response.status_code = 201  # HTTP 201 Created
            response["HX-Trigger"] = json.dumps({"noteCreated": {"message": str(message)} })

            return response

        # If form is invalid, return the form partial with errors
        response = render(
            request,
            "note/partials/create_note_form.html",
            {"form": form}
        )
        response.status_code = 400  # HTTP 400 Bad Request
        return response


class NoteUpdateView(LoginRequiredMixin, View):
    """
    Handle updating an existing note.
    """
    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk, owner=request.user)
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            message = _("Note updated successfully.")

            # Return new note partial (HTMX target)
            response = render(
                request,
                "note/partials/note_item.html",
                {"note": note}
            )
            response.status_code = 201  # HTTP 201 Updated
            response["HX-Trigger"] = json.dumps({"noteUpdated": {"message": str(message), "noteId": str(note.id)} })
            return response
          
        # If form is invalid, return the form partial with errors
        response = render(
            request,
            "note/partials/edit_note_form.html",
            {"form": form}
        )
        response.status_code = 400  # HTTP 400 Bad Request
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
        
        return render(
            request,
            "note/partials/note_list.html",
            {"notes": notes, "message": message}
        )


class FavouriteNoteListView(LoginRequiredMixin, View):
    """
    Display a list of favourites notes belonging to the logged-in user.
    """
    def get(self, request, is_favourite = None):
        
        if is_favourite == "all":
            print(is_favourite)
            notes = Note.objects.filter(owner=request.user).order_by("-updated_at")
        else:
            notes = Note.objects.filter(owner=request.user, is_favourite=True).order_by("-updated_at")
            
        print(is_favourite)    
        return render(
            request,
            "note/partials/note_list.html",
            {"notes": notes}
        )     
  
        
class NoteFavoriteToggleView(LoginRequiredMixin, View):
    """
    Handle toggling favorite status of a note.
    Returns JSON response for HTMX/AJAX requests.
    """
    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk, owner=request.user)
        
        # Toggle the favorite status
        note.is_favourite = not note.is_favourite
        note.save(update_fields=['is_favourite'])
        
        response_data = {
            'success': True,
            'is_favourite': note.is_favourite,
        }
        
        response = JsonResponse(response_data)
        
        return response