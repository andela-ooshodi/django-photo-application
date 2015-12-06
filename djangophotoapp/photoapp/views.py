from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.template import RequestContext
from photoapp.models import UserProfile, Pictures
from photoapp.tasks import save_pictures


class LoginView(TemplateView):
    template_name = 'photoapp/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            messages.add_message(
                request, messages.SUCCESS, 'Welcome back!')
            return redirect(
                '/',
                context_instance=RequestContext(request)
            )
        return super(LoginView, self).dispatch(request, *args, **kwargs)


class LoginRequiredMixin(object):
    # View mixin which requires that the user is authenticated.

    @method_decorator(login_required(login_url='/login'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'photoapp/home.html'
    form_class = Pictures

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['profilepic'] = UserProfile.objects.get(
            user_id=self.request.user.id)
        return context

    def post(self, request, **kwargs):
        form = self.form_class(request.Files)
        task = save_pictures.delay(request, form)

        if task:
            return redirect('/home')
        return render(request, 'photoapp/home.html')
