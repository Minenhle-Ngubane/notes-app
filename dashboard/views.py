from django.views import View
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.core.serializers.json import DjangoJSONEncoder

from note.models import Note


class DashboardView(LoginRequiredMixin, View):
    
    def get(self, request):
        notes_qs = Note.objects.filter(owner=request.user)
        
        notes_by_day = (
            notes_qs
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(total=Count("id"))
            .order_by("day")
        )
        
        # Convert queryset into JSON-safe format
        notes_by_day_json = json.dumps(list(notes_by_day), cls=DjangoJSONEncoder)

        stats = {
            "total_notes": notes_qs.count(),
            "favourite_notes": notes_qs.filter(is_favourite=True).count(),
            "recent_notes": notes_qs.filter(updated_at__gte=timezone.now() - timedelta(days=7)).count(),
            "last_updated": notes_qs.first(),
        }

        return render(
            request, 
            "dashboard/index.html", 
            {
                "title": "Dashboard",
                "stats": stats,
                "notes_by_day": notes_by_day_json,
            }
        )