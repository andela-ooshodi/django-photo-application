from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.template import RequestContext
from photoapp.models import UserProfile, Images
from photoapp.forms import ImageForm
from cloudinary import api

import json


class LoginView(TemplateView):
    template_name = 'photoapp/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            messages.add_message(
                request, messages.SUCCESS, 'Welcome back!')
            return redirect(
                '/home',
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
    form_class = ImageForm

    def get_context_data(self, **kwargs):
        # get all images belonging to logged in user
        images = Images.objects.filter(
            owner_id=self.request.user.id).order_by('-date_created')
        context = super(HomeView, self).get_context_data(**kwargs)
        context['profilepic'] = UserProfile.objects.get(
            user_id=self.request.user.id)
        context['images'] = images
        return context

    def post(self, request, **kwargs):
        try:
            form = self.form_class(request.POST, request.FILES)
            image = form.save(commit=False)
            image.image_file_name = form.files['image'].name
            image.owner = request.user
            image.save()

            return HttpResponse(
                json.dumps({'msg': 'success'}),
                content_type="application/json"
            )
        except:
            return HttpResponseNotAllowed(
                'invalidfile',
                content_type='text/plain')

    def delete(self, request, **kwargs):
        image_id = int(request.body.split('=')[1])
        image = Images.objects.get(pk=image_id)
        public_id = image.image.public_id

        # delete from cloudinary
        api.delete_resources([public_id])

        # delete from database
        image.delete()

        return HttpResponse(
            json.dumps({'msg': 'success'}),
            content_type="application/json"
        )
