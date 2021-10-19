import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.db import models

from task.models.base import BaseEntity


class GenerateQR(BaseEntity):
    name = models.CharField(max_length=100)
    qr_image = models.ImageField(upload_to='qr_code', blank=True, null=True)

    def __str__(self):
        return self.name

    # save method
    def save(self, *args, **kwargs):
        qr_image = qrcode.make(self.name)
        qr_offset = Image.new('RGB', (310, 310), 'white')
        draw_img = ImageDraw.Draw(qr_offset)
        qr_offset.paste(qr_image)
        file_name = f'{self.name}-{self.id}qr.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.qr_field.save(file_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)
