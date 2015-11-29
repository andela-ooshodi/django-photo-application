from photoapp.models import UserProfile


def get_profile_details(backend, user, response, *args, **kwargs):
    # Save Facebook profile photo into the user profile
    # import pdb; pdb.set_trace()
    if backend.name == "facebook":
        img_url = "http://graph.facebook.com/{0}/picture".format(
            response['id'])

    profile = UserProfile.objects.get_or_create(user=user)[0]
    profile.photo = img_url
    profile.save()
