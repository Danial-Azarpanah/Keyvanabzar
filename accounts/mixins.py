from django.shortcuts import redirect
from django.urls import reverse_lazy


class RequiredLoginMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(
                reverse_lazy("accounts:sign-in") + f"?return_to={request.GET.get('return_to')}"
            )
        return super().dispatch(request, *args, **kwargs)


class AuthenticatedMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)
