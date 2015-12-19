from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed,\
    HttpResponseBadRequest
from django.views.generic import View, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from photoapp.models import UserProfile, Images
from photoapp.forms import ImageForm
from photoapp.filters import ApplyFilter
from djangophotoapp.settings.base import MAX_UPLOAD_SIZE

import json
import os


class LoginView(TemplateView):
    template_name = 'photoapp/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/home')
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
        form = self.form_class(request.POST, request.FILES)
        file_size = form.files['image'].size

        if file_size < MAX_UPLOAD_SIZE:
            try:
                image = form.save(commit=False)
                image.image_file_name = form.files['image'].name
                image.owner = request.user
                image.save()

                # returning the img src of the latest
                # upload to be used in mobile
                # view (less than 992px)
                newest_image = Images.objects.filter(
                    owner_id=self.request.user.id).order_by('-date_created')[0]

                # id of newest image
                newest_image_id = newest_image.id

                # url of the latest image uploaded
                newest_image_src = newest_image.image.url

                return HttpResponse(
                    json.dumps({
                        'newest_image_src': newest_image_src,
                        'newest_image_id': newest_image_id
                    }),
                    content_type='application/json'
                )
            except:
                return HttpResponseBadRequest('invalidfile')
        else:
            return HttpResponseNotAllowed('largefile')

    def delete(self, request, **kwargs):
        image_id = int(request.body.split('=')[1])

        image = Images.objects.get(pk=image_id)
        image_path = image.image.path

        # delete from database
        image.delete()

        # delete from file directory
        if os.path.exists(image_path):
            # split the image part
            filepath, ext = os.path.splitext(image_path)
            # create the filtered image path
            new_filepath = filepath + "filtered" + ext
            # delete image
            os.remove(image_path)
            # delete filtered image
            os.remove(new_filepath)

        return HttpResponse(
            json.dumps({'msg': 'success'}),
            content_type='application/json'
        )


class FilterView(View):

    """
    Calls logic to apply image filtering
    """

    def get(self, request, *args, **kwargs):
        imagesrc = str(request.GET['img_src'])
        imageid = int(request.GET['img_id'])
        imagefilter = str(request.GET['img_filter'])

        # apply filter and get the path to the filtered image
        filter_img = ApplyFilter(imageid, imagesrc, imagefilter)
        filtered_img_path = filter_img.apply_filter()

        return HttpResponse(
            json.dumps({
                'filtered_img_path': filtered_img_path
            }),
            content_type='application/json'
        )


def custom404(request):
    return render(request, 'photoapp/404.html')


def custom500(request):
    return render(request, 'photoapp/500.html')
