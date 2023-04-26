from config.wsgi import *
from Core.solicitud.models import *
import random


letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
           'u', 'v', 'w', 'x', 'y', 'z']

for i in range(1, 6000):
    nombre = ''.join(random.choices(letters, k=5))
    while Category.objects.filter(nombre=nombre).exists():
        nombre = ''.join(random.choices(letters, k=5))
    Categorias(nombre=nombre).save()
    print('Guardado registro {}'.format(i))