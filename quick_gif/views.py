import uuid
from django.shortcuts import render
from .forms import QuickGIFsForm
from .models import QuickGIFs
from modules import make_gif
import os
from django.views.decorators.http import require_POST
import json
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def quick_gif(request):
    if request.method == 'POST':
        print(request.POST)
        form = QuickGIFsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            print(request.POST)
            files = request.FILES.getlist('gif_file')

            speed = int(float(request.POST['gif_speed'])) if request.POST['gif_speed'] != '' else 500 / 1000
            width = int(float(request.POST['gif_width'])) if request.POST['gif_width'] != '' else 500

            checked = True
            try:
                if request.POST['set_height_from_width'] == 'on':  # if checked, then the script decides the height
                    height = 0
            except:  # if unchecked, use the user given height
                height = int(float(request.POST['gif_height'])) if request.POST['gif_height'] != '' else 550
                checked = False

            if len(files) > 100:
                user_inputs = {'gif_speed': speed,
                               'gif_width': width,
                               'gif_height': 550 if height == 0 else height}
                form = QuickGIFsForm(request.POST, files=request.FILES.copy())
                return render(request, "quick_gif/quick_gif.html", {'form': form,
                                                                    'gif_speed': speed,
                                                                    'gif_width': width,
                                                                    'gif_height': 550 if height == 0 else height,
                                                                    'checked': checked,
                                                                    'img_upload_error': 'You exceeded the max file upload limit >:('})

            gif = QuickGIFs.objects.create()
            key = str(uuid.uuid5(uuid.NAMESPACE_DNS, f'[[meow]].com/gifs/quick_gif/ma.ximu.s/1.7.29/{gif.id}'))
            gif.key = key
            gif.save()

            gif_details = make_gif.make_gif(files, str(gif.id), speed=speed, width=width, height=height, key=key)

            if gif_details['errors']:
                user_inputs = {'gif_speed': speed,
                               'gif_width': width,
                               'gif_height': 550 if height == 0 else height}
                form = QuickGIFsForm(request.POST, files=request.FILES.copy())
                return render(request, "quick_gif/quick_gif.html", {'form': form, 'img_upload_error': 'Please upload images with acceptable file formats!'})

            gif.gif_file = os.path.join('quick_gifs', key, str(gif.id) + '.gif')
            gif.save()

            file_size = gif.gif_file.size / (10 ** 6)

            return render(request, "quick_gif/quick_gif.html", {'gif': gif,
                                                                'sharable_link': '#',
                                                                'form': form,
                                                                'file_size': round(file_size, 1),
                                                                'gif_speed': speed,
                                                                'gif_width': width,
                                                                'gif_height': gif_details['gif_height'],
                                                                'checked': checked,
                                                                'number_of_images': gif_details['images_used']})
    else:
        form = QuickGIFsForm()
        return render(request, "quick_gif/quick_gif.html", {'form': form, 'checked': True})


def view_quick_gif(request, key):

    try:
        gif = QuickGIFs.objects.get(key=key)
        if not gif.sharable:  
            return render(request, 'quick_gif/view_quick_gif.html', {'error': 'You sneaky bastard ;)'})
        elif gif.delete_if_expired():  # if gif is expired, the model class deletes it
            return render(request, 'quick_gif/view_quick_gif.html', {'error': 'Uh-oh! Looks like this GIF link expired :('})
        else:
            return render(request, 'quick_gif/view_quick_gif.html', {'gif': gif, 'expires_in': gif.expires_in()})
    except ObjectDoesNotExist:
        return render(request, 'quick_gif/view_quick_gif.html', {'error': 'Uh-oh! Looks like this GIF link expired >:('})


@require_POST
def generate_gif_link(request):
    if request.method == 'POST':
        maze = request.POST['maze']

        gif = QuickGIFs.objects.get(id=maze)
        gif.sharable = True
        gif.save()

        sharable_link = f'http://127.0.0.1:8000/permalink/{gif.key}'

    ctx = {'gif_link': sharable_link}

    return HttpResponse(json.dumps(ctx), content_type='application/json')
