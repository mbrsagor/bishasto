from celery import shared_task


@shared_task
def add(x, y):
    return x + y


# https://dontrepeatyourself.org/post/asynchronous-tasks-in-django-with-celery-and-rabbitmq/