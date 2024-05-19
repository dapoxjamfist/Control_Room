import cv2
import numpy as np
import time

# Global variables for ROI selection
points = []
roi_selected = False

# Mouse callback function for polygon ROI selection
def select_roi(event, x, y, flags, param):
    global points, roi_selected

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        roi_selected = False

    elif event == cv2.EVENT_RBUTTONDOWN:
        roi_selected = True

# Create a window and set mouse callback for ROI selection
cv2.namedWindow("Select ROI")
cv2.setMouseCallback("Select ROI", select_roi)

# Capture the video
cap = cv2.VideoCapture(r"C:/Users/91735/Desktop/model/encroachment/encroachment.mp4")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame (optional)
    frame = cv2.resize(frame, (800, 600))
    time.sleep(0.1)  # Adjust the delay time as needed


    # Draw selected points
    for point in points:
        cv2.circle(frame, point, 5, (0, 255, 0), -1)

    # Draw lines between selected points
    if len(points) > 1:
        for i in range(len(points) - 1):
            cv2.line(frame, points[i], points[i + 1], (0, 255, 0), 2)

    # Display the frame with ROI selection
    cv2.imshow("Select ROI", frame)

    # Break the loop if ROI is selected and 'q' is pressed
    if roi_selected:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Convert points to a numpy array
points = np.array(points)

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()

# Print ROI points
print("Selected ROI Points:")
print(points)

# Re-capture the video
cap = cv2.VideoCapture(r"C:/Users/91735/Desktop/model/encroachment/encroachment.mp4")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame (optional)
    frame = cv2.resize(frame, (800, 600))

    # Slow down the video by adding a delay
    time.sleep(0.1)  # Adjust the delay time as needed

    # Display the frame with ROI selection
    cv2.imshow("Slow Video", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
