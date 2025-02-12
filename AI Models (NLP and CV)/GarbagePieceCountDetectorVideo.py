import cv2
import math
import cvzone
from ultralytics import YOLO

# Initialize video capture
video_path = "medias/garbage.mp4"
cap = cv2.VideoCapture(video_path)

# Load YOLO model with custom weights
model = YOLO("weight/best.pt")

# Define class names
classNames = ['0', 'c', 'garbage', 'garbage_bag', 'sampah-detection', 'trash']

# Initialize total garbage count
total_garbage_count = 0

while True:
    success, img = cap.read()
    if not success:
        break  # End of video

    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Correctly unpack bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            w, h = x2 - x1, y2 - y1
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])

            if conf > 0.5 and classNames[cls] in ['garbage', 'garbage_bag', 'trash']:
                # Crop the region of interest (ROI) for garbage detection
                roi = img[y1:y2, x1:x2]

                # Convert the ROI to grayscale and apply thresholding
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray_roi, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # Find contours in the thresholded image
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Count distinct pieces of garbage in this bounding box
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
                cvzone.putTextRect(img, f'{classNames[cls]}: {garbage_count_in_box}', (max(0, x1), max(35, y1)),
                                   scale=1, thickness=1, colorR=(255, 0, 0))

    # Annotate the image with the total garbage count in yellow
    cv2.putText(img, f"Total Garbage Pieces: {total_garbage_count}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 255), 2)

    # Display the image with detections and counts
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close the window
cap.release()
cv2.destroyAllWindows()
