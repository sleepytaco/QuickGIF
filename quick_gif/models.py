from django.db import models
from myapp import settings
import os
import datetime
import pytz
import shutil


# Create your models here.
class QuickGIFs(models.Model):
    key = models.CharField(max_length=36, unique=True)
    made_on = models.DateTimeField(auto_now_add=True)
    gif_file = models.ImageField(upload_to='quick_gifs/')
    sharable = models.BooleanField(default=False)

    def delete_gif(self):
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'quick_gifs', f'{self.id}.gif'))
        QuickGIFs.objects.get(key=self.key).delete()  # delete the related object in the model

    def delete_if_expired(self):
        now = datetime.datetime.now(pytz.utc)  # make a timezone "aware" datetime object so that it can be added to the made_on attribute
        if self.made_on + datetime.timedelta(minutes=10) < now:  # if the event date has past
            self.delete_gif()
            return True
        return False

    def expires_in(self):
        now = datetime.datetime.now(pytz.utc)
        if self.made_on + datetime.timedelta(minutes=10) > now:  # if the event date has not past
            s = ((self.made_on + datetime.timedelta(minutes=10)) - now).seconds
            hours, remainder = divmod(s, 3600)
            minutes, seconds = divmod(remainder, 60)
            # return '{:02} hours {:02} minutes and {:02} seconds'.format(int(hours), int(minutes), int(seconds))
            if hours > 0:
                return '{:02} hours'.format(int(hours))
            if minutes > 0:
                return '{:02} minutes'.format(int(minutes))
            if seconds > 0:
                return '{:02} seconds'.format(int(seconds))
        return 'EXPIRED'
