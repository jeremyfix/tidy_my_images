Tidy My Images
==============

Python script to classify images from their EXIF datetime

Motivation
----------

I have a bunch of directories where I usually copy my images. But at some point, they all become 'to_classify', 'to_classify_2' , and so on. I like to get the images properly ordered in subdirectories root/YYYY/MM/filename with a filename being YYYY_MM_DD_hh:mm:ss.xxx where xxx is the original extension. The script tidy_my_images helps in doing the job by using the EXIF datetime tag of the images. 

Installation
------------

The script relies on [exif-py](https://github.com/ianare/exif-py)

Usage
-----

To know how to use the script, use
>     python tidy_my_images.py -h

The basic way to use the script is:
>     python tidy_my_images.py Photos/  PhotosDst/

If you want to know what the script is doing, you can set up the verbosity (0, 1 or 2)
>     python tidy_my_images.py Photos/  PhotosDst/ --verbosity 2

The script processes all the files, order and rename the images and copy the other files into PhotosDst/ignored_files

