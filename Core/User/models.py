from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict

from crum import get_current_request

from Config.settings import MEDIA_URL, STATIC_URL


class User(AbstractUser):
    imagen = models.ImageField(upload_to='users1/%Y/%m/%d', null=True, blank=True)
    token = models.UUIDField(primary_key=False, null=True, editable=False, blank=True)

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/user.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['password','user_permissions','last_login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['imagen'] = self.get_image()
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass
    
    def __str__(self):
        return '{}'.format(self.username)

