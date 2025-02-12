import cv2
import numpy as np


# Function to detect lane width in a single frame
def detect_lane_width(frame):
    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find the contours of the edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables to hold the leftmost and rightmost points
    leftmost = None
    rightmost = None

    # Iterate through contours and find the extreme leftmost and rightmost points
    for contour in contours:
        # Get extreme points for each contour
        left_point = tuple(contour[contour[:, :, 0].argmin()][0])
        right_point = tuple(contour[contour[:, :, 0].argmax()][0])

        # Update the leftmost and rightmost points for the road boundary
        if leftmost is None or left_point[0] < leftmost[0]:
            leftmost = left_point
        if rightmost is None or right_point[0] > rightmost[0]:
            rightmost = right_point

    if leftmost and rightmost:
        # Calculate the road width in pixels (distance between the leftmost and rightmost points)
        road_width_pixels = np.linalg.norm(np.array(leftmost) - np.array(rightmost))

        # Conversion from Pixels to Meters using the black car's width (assuming 1.5 meters for a nearby black taxi)
        car_width_meters = 1.5  # Estimated width of the black car in meters
        car_width_pixels = 150  # Approximate car width in pixels (adjust as necessary)

        # Calculate the pixel-to-meter ratio
        pixels_per_meter = car_width_pixels / car_width_meters

        # Calculate the road width in meters
        road_width_meters = road_width_pixels / pixels_per_meter

        # Convert road width to feet
        road_width_feet = road_width_meters * 3.28084

        # Annotate the frame
        annotated_frame = frame.copy()
        cv2.circle(annotated_frame, leftmost, 10, (0, 255, 0), -1)  # Leftmost point
        cv2.circle(annotated_frame, rightmost, 10, (0, 255, 0), -1)  # Rightmost point
        cv2.line(annotated_frame, leftmost, rightmost, (255, 0, 0), 2)  # Line between points

        # Add text annotation
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = f"Lane Width: {road_width_feet:.2f} ft"
        cv2.putText(annotated_frame, text, (int((leftmost[0] + rightmost[0]) / 2), leftmost[1] - 10),
                    font, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

        return annotated_frame, road_width_feet

    # Return the original frame if no lane is detected
    return frame, None


# Path to the input video
input_video_path = 'E:/AI Models (NLP and CV)/GarbageDetector/medias/garbage.mp4'

# Open the video file
cap = cv2.VideoCapture(input_video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get video properties for output settings
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Output video writer (optional)
output_video_path = 'E:/AI Models (NLP and CV)/GarbageDetector/medias/output_video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("End of video or error reading frame.")
        break

    # Process the frame for lane width detection
    processed_frame, lane_width_feet = detect_lane_width(frame)

    # Display the frame
    cv2.imshow('Lane Width Detection', processed_frame)

    # Write the frame to the output video
    out.write(processed_frame)

    # Add a delay to slow down playback (e.g., 500 ms for 2 FPS)
    if cv2.waitKey(500) & 0xFF == ord('q'):  # Press 'q' to exit
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
