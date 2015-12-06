from celery.task import task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@task
def save_images(image):
    
    logger.info("Image Saved!!")
    return True
