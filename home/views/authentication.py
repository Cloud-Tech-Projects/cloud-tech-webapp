import logging
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.conf import settings
from django_tenants.utils import get_tenant
from django.core.exceptions import PermissionDenied

from web.models import UserProfile
from ..forms.authentication import LoginForm, SignUpForm
from ..tasks import admin_notification_email, user_notification_email

User = get_user_model()


class Login(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home:home')

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data()
        context['public_url'] = settings.PUBLIC_URL
        return context
      
    def authenticate_user(self, username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            return user
        raise PermissionDenied("Invalid credentials")

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        try:
            user = self.authenticate_user(username, password)

            if UserProfile.objects.filter(user=user).exists():
                tenant = get_tenant(self.request)
                if tenant not in user.profile.tenants.all():
                    raise PermissionDenied("Permission Denied")

            login(self.request, user)
            return super().form_valid(form)

        except PermissionDenied as e:
            form.add_error(None, str(e))

        return self.form_invalid(form)


class Register(FormView):
    template_name = 'accounts/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home:login')

    def form_valid(self, form):
        # Create the user object
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']

        # Create the User object
        user = User.objects.create_user(
            username=username, email=email, password=password)
        tenant = get_tenant(self.request)
        logging.info(type(tenant))
        user_profile = UserProfile.objects.create(user=user)
        user_profile.tenants.set([tenant])
        task1 = admin_notification_email.si(tenant.id,user.username).set(queue='queue1')
        task1.apply_async()
        task2 = user_notification_email.si(tenant.id,user.username).set(queue='queue2')
        task2.apply_async()
        return super().form_valid(form)
