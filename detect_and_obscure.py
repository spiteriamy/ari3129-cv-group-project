import os
import cv2
from ultralytics.models import YOLO

# define input and output folders
img_folder = 'obscure_in/'
processed_folder = 'obscure_out/'

if not os.path.exists(processed_folder):
    os.makedirs(processed_folder)

# Load the YOLOv8 nano model
model = YOLO('yolov8n.pt')

# From COCO dataset 
# 0: person, 1: bicycle, 2: car, 3: motorcycle, 5: bus, 7: truck
target_classes = [0, 1, 2, 3, 5, 7]

img_paths = os.listdir(img_folder)

for img_name in img_paths:
    full_path = os.path.join(img_folder, img_name)

    # specific check for image extensions
    if not img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        continue

    # Read image
    img = cv2.imread(full_path)
    if img is None:
        print(f"Could not read {img_name}")
        continue

    # Run YOLO inference
    # verbose=False keeps the terminal clean
    results = model(img, verbose=False)

    # Iterate through detections
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Get class ID (what object is it?)
            cls_id = int(box.cls[0])

            if cls_id in target_classes:
                # Get coordinates (x1, y1, x2, y2)
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Draw a solid black rectangle
                # (0, 0, 0) is black color
                # -1 thickness means "fill the shape"
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), -1)

    # Save the result
    output_path = os.path.join(processed_folder, img_name)
    cv2.imwrite(output_path, img)
    print(f"Processed and saved: {img_name}")
