#!/usr/bin/env python3
import argparse
import csv

from PIL import Image


def crop_image(filename, xmin, xmax, ymin, ymax):
    try:
        im = Image.open(filename)
        if im is not None:
            w, h = im.width, im.height

            left = xmin * w
            right = xmax * w
            bottom = ymax * h
            top = ymin * h

            im = im.crop((left, top, right, bottom))
            im.save("output/" + filename)
    except FileNotFoundError:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--classname', required=True, help="Class to identify")
    parser.add_argument('--bboxes_csv', required=True, help="Path to the csv files which contains the bounding boxes")

    args = parser.parse_args()

    cls_id = None

    with open('class-descriptions.csv') as id_mapping:
        id_mapping_reader = csv.reader(id_mapping, delimiter=',')

        img_class = args.classname

        for row in id_mapping_reader:
            if row[1] == img_class:
                cls_id = row[0]

        if cls_id is None:
            raise Exception("The class name seems to be invalid.")

    with open(args.bboxes_csv) as bboxes:
        bbox_reader = csv.reader(bboxes, delimiter=',')

        for row in bbox_reader:
            img_name = row[0]

            # Ignore header
            if "ImageID" in img_name:
                continue

            if cls_id in row[2]:
                xmin = float(row[4])
                xmax = float(row[5])
                ymin = float(row[6])
                ymax = float(row[7])

                filename = f"{img_name}.jpg"
                print(f"DEBUG: filename={filename}")
                print(f"DEBUG: xmin={xmin}, xmax={xmax}, ymin={ymin}, ymax={ymax}")

                crop_image(filename, xmin, xmax, ymin, ymax)
