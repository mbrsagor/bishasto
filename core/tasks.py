from celery import shared_task
from core.models.item import Item


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_items():
    return Item.objects.count()

@shared_task
def mod(self, x, y):
    try:
        z = x % y
        print(f'{x} % {y} = {x%y}')
        return z
    except :
        mod.retry()
        print(f'Error with mod')


@shared_task
def rename_item(item_id, item_name):
    _item = Item.objects.get(id=item_id)
    _item.item_name = item_name
    _item.save()
