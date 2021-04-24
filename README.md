# OIV6-BBoxes-Cropper
A simple python3 script for cropping images from the Open Images V6 image set along their bounding boxes, which is useful for creating creating custom datasets.
The bounding box annotation CSV sheet has the following format:

| ImageID          | Source | LabelName | Confidence | XMin   | XMax     | YMin     | YMax   | IsOccluded | IsTruncated | ... |
|------------------|--------|-----------|------------|--------|----------|----------|--------|------------|-------------|-----|
| 000002b66c9c498e | xclick | /m/01g317 | 1          | 0.0125 | 0.195312 | 0.148438 | 0.5875 | 0          | 1           | ... |

## Usage:
```
python3 crop.py --classname <Name of class> --bboxes_csv <Path to bounding box annotation CSV sheet>
```

## Example
```
python3 crop.py --classname chair --bboxes_csv ../path/to/sheet/
```
