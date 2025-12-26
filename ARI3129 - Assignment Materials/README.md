# Advanced Computer Vision for AI (ARI3129) Assignment  

## 1. Environment Setup
- Install Anaconda/Miniconda if you have not already.
- From the repo root run:
  ```bash
  conda env create -f Dependencies.yml
  conda activate ARI3129
  ```
- Launch Jupyter (`jupyter lab` or `jupyter notebook`) from this environment before opening `MemberMerger.ipynb` or `LS2COCO.ipynb`.

## 2. Prepare Label Studio
1. Start Label Studio locally and create a new project.
2. When prompted to configure the labeling interface, switch to the code (XML) editor and paste or upload the contents of `LabelingInterface.xml`.
3. Import your data.

### Labeling Rules (per `LabelingInterface.xml`)
- Draw a bounding box around every visible traffic sign.
- After drawing each box, pick the correct *Sign Type* (Stop, No Entry, Pedestrian Crossing, Roundabout Ahead, No Through Road, Blind-Spot Mirror).
- Set the required per-region sign attributes:
  - `Sign Shape Type`: Circular, Square, Triangular, Octagonal, or Damaged.
  - `Viewing Angle`: Front, Side, Back.
  - `Mounting Type`: Pole-mounted or Wall-mounted.
  - `Sign Condition`: Good, Weathered, Heavily Damaged.
- Optionally add task-level tags (`Sourced Online`, `No EXIF`) or free-text notes if they matter for your dataset.

## 3. Working With the Notebooks
- `MemberMerger.ipynb`: helps consolidate member exports or partial Label Studio results before conversion; run it after downloading team annotations to verify label consistency.
- `LS2COCO.ipynb`: loads the cleaned Label Studio JSON and exports COCO-style detection data; review the notebook cells and edit any paths that point to your local data directories.
- Always run these notebooks inside the `ARI3129` environment so the expected dependencies are available.

## 4. Deliverables Checklist
-  Environment created from `Dependencies.yml`.
-  Label Studio project configured with `LabelingInterface.xml`.
-  All images annotated following the required attributes.
-  Consolidated annotations converted through the notebooks into the format requested by your instructor.


## 5. Train Object Detector & Attribute Classifier

- **Detection Models**: Each member must train any detector (Ultralytics, TensorFlow, or PyTorch). Recommended options: YOLOv8/v11/v12, RF-DETR, RetinaNet, Faster R-CNN, EfficientDet. Groups with ≥3 members may mix YOLO versions within one project. Models trained via Roboflow or Ultralytics Hub will not be accepted.
- **Per-Member Requirements**: Train two separate detectors for traffic sign detection plus one additional model targeting a distinct attribute (viewing angle, mounting type, sign condition, or sign shape). Team members should choose different attributes.
- **Evaluation**: Use tools like TensorBoard or Ultralytics reports plus scripted metrics to compare runs. Document both qualitative observations and quantitative scores.
- **Analytics Output**: After detection, provide per-image analytics summarizing how many signs were found and which attribute category was predicted for each; motivate how this aids sign maintenance workflows.
