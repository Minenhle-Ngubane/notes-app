from django.urls import path

from .views import (
    NoteListView,
    NoteDetailView,
    NoteCreateView,
    NoteUpdateView,
    NoteDeleteView,
    NoteSearchView,
    NoteFavoriteToggleView,
    FavouriteNoteListView,
)

app_name = "note"


urlpatterns = [
    path("", NoteListView.as_view(), name="note_list"),
    path("create/", NoteCreateView.as_view(), name="note_create"),
    path("<uuid:pk>/", NoteDetailView.as_view(), name="note_detail"),
    path("<uuid:pk>/edit/", NoteUpdateView.as_view(), name="note_edit"),
    path("<uuid:pk>/delete/", NoteDeleteView.as_view(), name="note_delete"),
    path("search/", NoteSearchView.as_view(), name="note_search"),
    
    path("<uuid:pk>/favorite/", NoteFavoriteToggleView.as_view(), name="note_favorite_toggle"),
    path("favourite/<int:is_favourite>", FavouriteNoteListView.as_view(), name="note_favorite_list"),
]