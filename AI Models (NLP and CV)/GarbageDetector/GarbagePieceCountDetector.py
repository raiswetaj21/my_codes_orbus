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

# Initialize total garbage count
total_garbage_count = 0

# Loop through the detections and process each bounding box
for r in results:
    boxes = r.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        w, h = x2 - x1, y2 - y1
        conf = math.ceil((box.conf[0] * 100)) / 100
        cls = int(box.cls[0])

        # Process only relevant garbage classes
        if conf > 0.3 and class_labels[cls] in ['garbage', 'garbage_bag', 'trash']:
            # Crop the region of interest (ROI)
            roi = img[y1:y2, x1:x2]

            # Convert to grayscale and apply thresholding
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray_roi, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Find contours in the thresholded image
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Count distinct pieces of garbage
            garbage_count_in_box = 0
            for contour in contours:
                # Filter out small contours (noise)
                if cv2.contourArea(contour) > 100:  # Adjust this threshold as needed
                    garbage_count_in_box += 1
                    # Optionally, draw contours for visualization
                    cv2.drawContours(roi, [contour], -1, (0, 255, 0), 2)

            # Update the total garbage count
            total_garbage_count += garbage_count_in_box

            # Draw bounding box and count on the original image
            cvzone.cornerRect(img, (x1, y1, w, h), t=2)
            cvzone.putTextRect(img, f'{class_labels[cls]}: {garbage_count_in_box}', (x1, y1 - 10),
                               scale=0.8, thickness=1, colorR=(255, 0, 0))

# Annotate the image with the total garbage count
cv2.putText(img, f"Total Garbage Pieces: {total_garbage_count}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Display the image with detections and counts
cv2.imshow("Image", img)

# Close window when 'q' button is pressed
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cv2.waitKey(1)
