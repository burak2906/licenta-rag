from ultralytics import YOLO

model = YOLO("runs/detect/train7/weights/last.pt")

model.train(
    data="data.yaml",
    epochs=100,
    imgsz=640,
    batch=8,
    workers=2,
    patience=20,
    resume=True
)