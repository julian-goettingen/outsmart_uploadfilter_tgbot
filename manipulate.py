import moviepy as mp
import moviepy.editor as mpe
from skimage import filters, io
import numpy as np
import numpy.random as npr
import random
import functools
import re

def _blur(im):
    """ Returns a blurred (radius=2 pixels) version of the image """
    return filters.gaussian(im.astype(float), sigma=2)

def _darken_by(im, by=0.95):

    return im.astype(float)*0.95


def manipulate_mp4(filename_in, filename_out):



    clip = mpe.VideoFileClip(filename_in)
    start_at = npr.uniform(0.01,0.06)
    end_at = -npr.uniform(0.01,0.06)
    clip = clip.subclip(start_at, end_at)

    
    darken = functools.partial(_darken_by,by=random.choice([0.93, 0.95, 1.05, 1.03]))

    res = clip.fl_image( darken )
    res.write_videofile(filename_out)



def manipulate_image(filename_in, filename_out):

    img_arr = io.imread(filename_in)

    io.imsave(filename_out, img_arr)



fileending2fun = {
        "mp4" : manipulate_mp4,
        "jpg" : manipulate_image,
        "jpeg" : manipulate_image,
        "png" : manipulate_image
}
uppercase_keys = {k.upper() : v for k,v in fileending2fun.items()}
fileending2fun.update(uppercase_keys)

supp_endings_msg = "Supported fileendings are currently :"+", ".join(fileending2fun.keys())


def manipulate(filename_in):

    m = re.match(r"([^.]+)\.([^.]+)", filename_in)
    
    if not m:
        return (False, filename_in + " ? failed to detect file type. "+supp_endings_msg)

    name, ftype = m.groups()

    filename_out = name + "_x." + ftype

    print(ftype)
    print(ftype not in fileending2fun)
    print(fileending2fun.keys())
    if ftype not in fileending2fun:
        return (False, filename_in + f" has unsupported file ending: {ftype}, "+supp_endings_msg)
    mani = fileending2fun[ftype]

    mani(filename_in, filename_out)

    return (True, filename_out)



