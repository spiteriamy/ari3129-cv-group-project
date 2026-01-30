# ARI3129 Advanced Computer Vision for AI - Group Project 

## Repository Structure

[**Dataset**](/Dataset/): Contains all images and annotations.

```css
Dataset/
│── COCO-Format Annotations/
│   ├── COCO.json
│   ├── COCO_condition.json
│   ├── COCO_mounting.json
│   ├── COCO_sign_shape.json
│   └── COCO_view_angle.json
|
│── Individuals/
|
│── Train-Test-Val Split/
│   ├── COCO-based
│   ├── YOLO
│   └── images.zip
│
│── merged_images.zip
└── merged_input.json
```

- [**COCO-Format Annotations**](Dataset/COCO-Format%20Annotations/): Contains all COCO annotation files.

- [**Individuals**](Dataset/Individuals/): Contains all original JSON and ZIP files for each member.

- [**Train-Test-Val Split**](Dataset/Train-Test-Val%20Split/): Dataset split into 70% train, 15% validation, and 15% test subsets, contains both YOLO and COCO-based formats.

- [**merged_images.zip**](Dataset/merged_images.zip): All images in dataset, combined from all members.

- [**merged_input.json**](Dataset/merged_input.json): All image annotations.

---

[**Annotation Process**](/Annotation%20Process/): This directory contains all of the dataset files that were uploaded during the annotation stage, before merging and creating the final dataset. It also contains scripts used to help blur the images.

