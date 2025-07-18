from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"
    login_url = "accounts:login"
    redirect_field_name = "next"