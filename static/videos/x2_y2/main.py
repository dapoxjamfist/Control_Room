import cv2
from ultralytics import YOLO
import cvzone
import numpy as np
import math

# Load the model
model = YOLO("static/videos/x2_y2/yolov8n.pt")
with open("static/videos/x2_y2/classes.txt", 'r') as f:
    classnames = f.read().splitlines()

# Define the selected ROI points
a = np.array([
    [250, 309],
    [343, 304],
    [339, 488],
    [509, 482],
    [471, 342],
    [523, 314],
    [703, 554],
    [169, 583],
    [248, 310]
])

# Read the video
cap = cv2.VideoCapture("static/videos/x2_y2/video1.mp4")
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('static/videos/x2_y2/output.mp4', fourcc, 30.0, (800, 600))
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame
    frame = cv2.resize(frame, (800, 600))

    # Draw selected ROI points region
    cv2.polylines(frame, [a], isClosed=True, color=(0, 0, 255), thickness=2)

    # Filter out detections outside the selected ROI
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, [a], (255, 255, 255))
    masked_frame = cv2.bitwise_and(frame, mask)

    # Perform object detection on the masked frame
    results = model(masked_frame)
    
    vehicle_count = 0  # Initialize vehicle count

    for info in results:
        parameters = info.boxes
        for box in parameters:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            confidence = box.conf[0]
            class_detect = box.cls[0]
            class_detect = int(class_detect)
            class_detect = classnames[class_detect]
            conf = math.ceil(confidence * 100)
            cvzone.putTextRect(frame, f'{class_detect}', [x1 + 8, y1 - 12], thickness=2, scale=1)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Increment the vehicle count if the detected object is a vehicle
            if class_detect in ['car', 'truck', 'bus']:  # Add more classes if needed
                vehicle_count += 1

    # Display the vehicle count on the frame
    cvzone.putTextRect(frame, f'Vehicles identified: {vehicle_count}', [20, 40], scale=1, thickness=1, offset=10)
    if vehicle_count>10:
        cvzone.putTextRect(frame, f'encroachment identified', [30, 40], scale=2, thickness=2, offset=10)

        
    out.write(frame)
    cv2.imshow("vid", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
