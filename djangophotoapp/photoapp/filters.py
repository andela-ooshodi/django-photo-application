import os

from photoapp.models import Images
from PIL import Image, ImageFilter


class ApplyFilter:

    """
    Defines methods to apply filter
    """

    def __init__(self, imageid, imagesrc, imagefilter):
        self.imagepath = Images.objects.get(pk=imageid).image.path
        self.imagesrc = imagesrc

        # get the ImageFilter method based of "imagefilter" string
        self.imgfilter = getattr(ImageFilter, imagefilter)

    def apply_filter(self):

        # apply filter
        img = Image.open(self.imagepath)
        img = img.filter(self.imgfilter)

        # split file path to create new file path for edited images
        filepath, ext = os.path.splitext(self.imagepath)
        new_filepath = filepath + "filtered" + ext
        img.save(new_filepath)

        # create new url for filtered image
        url, ext = os.path.splitext(self.imagesrc)
        new_url = url + "filtered" + ext
        # return path to filtered image
        return new_url
