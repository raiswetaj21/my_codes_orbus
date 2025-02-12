import cv2
import math
import cvzone
from ultralytics import YOLO

# Load YOLO model with custom weights
yolo_model = YOLO("Weights/best.pt")

# Define class names
class_labels = ['0', 'c', 'garbage', 'garbage_bag', 'sampah-detection', 'trash']

# Load the image
image_path = "Media/garbage_5.jpeg"
img = cv2.imread(image_path)

# Perform object detection
results = yolo_model(img)

# Initialize garbage count
garbage_count = 0

# Loop through the detections and draw bounding boxes
for r in results:
    boxes = r.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        w, h = x2 - x1, y2 - y1

        conf = math.ceil((box.conf[0] * 100)) / 100
        cls = int(box.cls[0])

        # Count garbage only for relevant classes
        if conf > 0.3 and class_labels[cls] in ['garbage', 'garbage_bag', 'trash']:
            garbage_count += 1  # Increment the count
            cvzone.cornerRect(img, (x1, y1, w, h), t=2)
            cvzone.putTextRect(img, f'{class_labels[cls]} {conf}', (x1, y1 - 10), scale=0.8, thickness=1,
                               colorR=(255, 0, 0))

# Annotate the image with the garbage count
cv2.putText(img, f"Garbage Count: {garbage_count}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Display the image with detections and count
cv2.imshow("Image", img)

# Close window when 'q' button is pressed
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cv2.waitKey(1)
