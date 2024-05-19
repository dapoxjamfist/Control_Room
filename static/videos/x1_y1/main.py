import cv2
import cvzone
import math
from ultralytics import YOLO

cap = cv2.VideoCapture('static/videos/x1_y1/video1.mp4')

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('static/videos/x1_y1/output.mp4', fourcc, 30.0, (980, 740))

model = YOLO("static/videos/x1_y1/best.pt")


classnames = []
with open("static/videos/x1_y1/coco.txt.txt", 'r') as f:
    classnames = f.read().splitlines()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (980, 740))

    results = model(frame,conf=0.5)

    for info in results:
        parameters = info.boxes
        for box in parameters:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            confidence = box.conf[0]
            class_detect = box.cls[0]
            class_detect = int(class_detect)
            class_name = model.names[class_detect]  # Get class name using the class ID

            class_detect = classnames[class_detect]
            conf = math.ceil(confidence * 100)

            # implement fall detection using the coordinates x1,y1,x2
            height = y2 - y1
            width = x2 - x1
            threshold = height - width
            print(threshold)

            if conf > 50 and class_name == 'tree':
                cvzone.cornerRect(frame, [x1, y1, x2, y2], l=30, rt=6)
                cvzone.putTextRect(frame, f'{class_detect}', [x1 + 8, y1 - 12], thickness=2, scale=2)

                if threshold < 150:
                    cvzone.putTextRect(frame, 'Fall Detected', [20, 20], thickness=2, scale=2)

    out.write(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('t'):
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
