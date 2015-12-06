from celery.task import task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@task
def save_pictures(request, form):
    picture = form.save(commit=False)
    picture.picture_file_name = form.files['picture'].name
    picture.owner = request.user
    picture.save()
    logger.info("Picture Saved!!")
    return True
