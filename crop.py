#!/usr/bin/env python3
import argparse
import csv

from PIL import Image
from tqdm import tqdm

# positions of information in bounding box annotation sheet:
IMG_NAME = 0
CLASS_ID = 2
XMIN = 4
XMAX = 5
YMIN = 6
YMAX = 7


def crop_image(dir_path, filename, xmin, xmax, ymin, ymax):
    try:
        img = Image.open(f"{dir_path}{filename}")
        if img is not None:
            w, h = img.width, img.height

            left = xmin * w
            right = xmax * w
            bottom = ymax * h
            top = ymin * h

            img = img.crop((left, top, right, bottom))
            img.save(f"{dir_path}output/{filename}")
    except FileNotFoundError:
        pass


parser = argparse.ArgumentParser()
parser.add_argument('--dir', required=True, help="Directory path")
parser.add_argument('--classname', required=True, help="Class to identify")
parser.add_argument('--bboxes_csv', required=True, help="Path to the csv files which contains the bounding boxes")

args = parser.parse_args()

cls_id = None
# map the class name to its unique id, if it exists - otherwise end program
with open('class-descriptions.csv') as id_mapping:
    id_mapping_reader = csv.reader(id_mapping, delimiter=',')

    img_class = args.classname

    for row in id_mapping_reader:
        if row[1].lower() == img_class.lower():
            cls_id = row[0]
            print(f"Image class {img_class} has id {cls_id}")
            break

    if cls_id is None:
        raise Exception("The class name seems to be invalid.")

# extract information from bounding boxes csv sheet and crop images
with open(args.bboxes_csv) as bboxes:
    bbox_reader = csv.reader(bboxes, delimiter=',')

    for row in tqdm(bbox_reader):
        img_name = row[IMG_NAME]

        # Ignore header
        if "ImageID" in img_name:
            continue

        if cls_id in row[CLASS_ID]:
            xmin = float(row[XMIN])
            xmax = float(row[XMAX])
            ymin = float(row[YMIN])
            ymax = float(row[YMAX])

            filename = f"{img_name}.jpg"
            crop_image(args.dir, filename, xmin, xmax, ymin, ymax)
