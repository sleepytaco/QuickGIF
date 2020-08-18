import os
from myapp.settings import MEDIA_ROOT
from PIL import Image, ImageDraw, ImageFont


def make_gif(files, gif_name, speed, width, height, key):

    os.mkdir(os.path.join(MEDIA_ROOT, 'quick_gifs', key))

    ok_files = []
    bad_files = []
    errors = False

    count = 1
    for filename in files:
        if filename.name.endswith(('.jpg', '.jpeg', '.png')):
            try:
                img = Image.open(filename)  # open the file as image object
                img.verify()  # verify, it is infact an image
                # ok_files.append(filename)
                ok_files.append(filename)
                """img = Image.open(filename)
                print(os.path.join(MEDIA_ROOT, 'quick_gifs', key, '-' + str(count) + os.path.splitext(filename.name)[-1]))
                img.save(os.path.join(MEDIA_ROOT, 'quick_gifs', key, '-' + str(count) + os.path.splitext(filename.name)[-1]))
                ok_files.append(os.path.join(MEDIA_ROOT, 'quick_gifs', key, '-' + str(count) + os.path.splitext(filename.name)[-1]))"""
            except (IOError, SyntaxError) as e:  # if the image is corrupt, ignore
                bad_files.append(filename)
                print(e)

        else:  # if an image of someother extenstion is uploaded, delete it as well
            bad_files.append(filename)
            errors = True
            return {'errors': errors}
        count += 1

    MAXWIDTH = width

    # sort images files according to max height when a given width is set
    sorted_files = sorted(ok_files, key=lambda x: int((float(Image.open(x).size[1]) * float((MAXWIDTH / float(Image.open(x).size[0]))))), reverse=True)

    if height == 0:
        im = Image.open(sorted_files[0])
        wpercent = (MAXWIDTH / float(im.size[0]))
        hsize = int((float(im.size[1]) * float(wpercent)))
        max_gif_height = hsize  # initial
    else:
        max_gif_height = height

    images = []
    counter = 1
    for file in ok_files:

        im = Image.open(file)

        basewidth = MAXWIDTH
        wpercent = (basewidth / float(im.size[0]))
        hsize = int((float(im.size[1]) * float(wpercent)))
        img = im.resize((basewidth, hsize), Image.ANTIALIAS)

        """draw = ImageDraw.Draw(img)
        VCRFont = ImageFont.truetype(os.path.join(MEDIA_ROOT, 'fonts', 'VCR_OSD_MONO.ttf'), 40)
        draw.text((0, 0), str(counter), fill='black', font=VCRFont)"""

        if height == 0:
            if hsize >= max_gif_height:
                max_gif_height = hsize

        whitebg = Image.new('RGB', (MAXWIDTH, max_gif_height), 'white')
        whitebgcopy = whitebg.copy()
        whitebgcopy.paste(img)

        images.append(whitebgcopy)
        counter += 1

    images[0].save(os.path.join(MEDIA_ROOT, 'quick_gifs', key, gif_name + '.gif'), save_all=True, append_images=images[1:], optimize=False, duration=speed * 1000, loop=0)

    return {'gif_height': max_gif_height, 'images_used': len(ok_files), 'image_files': images, 'errors': errors}
