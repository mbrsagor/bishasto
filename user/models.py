import random
from django.db import models
from datetime import date, datetime
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

from .manager import UserManager
from core.models.base import Timestamp
from utils.enum_utils import GENDER, ROLE


class User(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=True)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=14, unique=True)
    role = models.IntegerField(choices=ROLE.get_choices(), default=ROLE.CUSTOMER.value)
    gender = models.IntegerField(choices=GENDER.select_gender(), default=GENDER.MALE.value)
    otp = models.CharField(max_length=6, null=True, blank=True)
    address = models.TextField(blank=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'username']
    objects = UserManager()

    # Method to Put a Random OTP in the CustomerUser table.
    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items_for_otp = []
        for i in range(6):
            num = random.choice(number_list)
            code_items_for_otp.append(num)
        code_string = "".join(str(item)
                              for item in code_items_for_otp)
        # A six digit random number from the list will be saved in top field
        self.otp = code_string
        # print(f"OTP: {self.otp}")
        super().save(*args, **kwargs)


    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return str(self.email)


class Profile(Timestamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nick_name = models.CharField(max_length=60, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile/%y/%m', blank=True, null=True)
    date_of_birth = models.DateField(default=datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    @property
    def current_age(self):
        today = date.today()
        return (today - self.date_of_birth).days

    @property
    def get_photo_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        else:
            return "/static/images/avatar.jpg"


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Profile.objects.get_or_create(user=instance)
        return profile


post_save.connect(create_user_profile, sender=User)


class ResetPhoneOTP(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$',
                                 message="Phone number must be entered in the form of +919999999999.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of opt_sent')
    validated = models.BooleanField(default=False,
                                    help_text='if it is true, that means user have validate opt correctly in seconds')

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)


class Follow(Timestamp):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"
