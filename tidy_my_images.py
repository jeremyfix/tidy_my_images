#!/usr/bin/python

# tidy_my_images.py is a python script for 
# classifying images into subdirectories by YYYY/MM/
# Copyright (C) 2014  Jeremy Fix

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# python tidy_my_images.py -h for help

import os.path, time
import sys
import os
import fnmatch
import argparse
import shutil

# For extracting the Exif info of the images
# We use https://github.com/ianare/exif-py
# apt-get install python-exif
import exifread

# PIL does not support all the image types (e.g. CR2)
#from PIL import Image
#from PIL.ExifTags import TAGS

parser = argparse.ArgumentParser(description='Sort out images and put them in directories YYYY/MM/ and filenames YYYY_MM_DD_hh:mm:ss according to their exif DateTimeOriginal tag value')
parser.add_argument('src_dir', type=str, help="The source directory from which the images will be recursively considered")
parser.add_argument('dst_dir', type=str, help="The root target directory in which subdirectories will be created and images copied")
parser.add_argument('--verbosity', help="increase output verbosity (0, 1, 2) , default:0", type=int)
args = parser.parse_args()

src_root_dir = args.src_dir
dst_root_dir = args.dst_dir
verbosity_mode = args.verbosity
if not args.verbosity:
    verbosity_mode = 0 # The default
else:
    verbosity_mode = args.verbosity


def get_exif_datetime(path_name):
    # Open image file for reading (binary mode)
    f = open(path_name, 'rb')
    
    # Extract the DateTimeOriginal exif tag
    tags = exifread.process_file(f, details=False, stop_tag='DateTimeOriginal',strict=True )
    f.close()

    if(tags.has_key('EXIF DateTimeOriginal')):
        return str(tags['EXIF DateTimeOriginal'])
    else:
        raise KeyError('The file {} does not have the DataTimeOriginal EXIF information'.format(path_name))


if(verbosity_mode >= 1):
    start_time = time.time()
    nb_processed_files = 0

for root, dirnames, filenames in os.walk(src_root_dir):
    for filename in filenames:
        if(verbosity_mode >= 1):
            nb_processed_files+=1
        _, ext = os.path.splitext(filename)
        full_filename = os.path.join(root, filename)

        try:
            if(verbosity_mode >= 1):
                print("Reading datetime of %s" % full_filename)
            exif_datetime = get_exif_datetime(full_filename)
        except KeyError:
            # The file is ignored but we copy it in
            # dst_root_dir/ignored_files/ ...
            # The ... is the prefix path excluding src_root_dir
            p = os.path.relpath(full_filename, src_root_dir)
            full_target_filename = os.path.join(dst_root_dir,"ignored_files", p)
            target_dir = os.path.dirname(full_target_filename)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            if(verbosity_mode >= 1):
                print("Ignored file {} copied to {}".format(full_filename, full_target_filename))
            shutil.copy2(full_filename, full_target_filename)
            continue

        ltime = time.strptime(exif_datetime,"%Y:%m:%d %H:%M:%S")
        target_dir = os.path.join(dst_root_dir, \
                                  time.strftime("%Y",ltime), \
                                  time.strftime("%m",ltime))
        target_filename = time.strftime("%Y_%m_%d_%H:%M:%S", ltime) + ext
        full_target_filename = os.path.join(target_dir, target_filename)
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        # We check if the file already exists
        if os.path.isfile(full_target_filename):
            target_filename_new = "_" + target_filename
            full_target_filename_new = os.path.join(target_dir, target_filename_new)
            while(os.path.isfile(full_target_filename_new)):
                target_filename_new =  "_" + target_filename_new
                full_target_filename_new = os.path.join(target_dir, target_filename_new)
            if(verbosity_mode >= 2):
                print("Warning, {} already exists, using {} instead".format(full_target_filename, full_target_filename_new))
            full_target_filename = full_target_filename_new
        if(verbosity_mode >= 2): 
            print("Copying {} to {}".format(full_filename, full_target_filename))
        shutil.copy2(full_filename, full_target_filename)

if(verbosity_mode >= 1):
    elapsed_time = time.time() - start_time
    print("Processed {} files in {} s.".format(nb_processed_files, elapsed_time))
    nb_src_files = 0
    for root, dirnames, filenames in os.walk(src_root_dir):
        nb_src_files += len(filenames)
    nb_dst_files = 0
    for root, dirnames, filenames in os.walk(dst_root_dir):
        nb_dst_files += len(filenames)
    print("Get {} in {} from {} in {}".format(nb_dst_files, dst_root_dir, nb_src_files, src_root_dir))
