import cv2
import numpy as np
# Check OpenCV version
print("OpenCV version:", cv2.__version__)

# Load the image
image = cv2.imread('E:/AI Models (NLP and CV)/GarbageDetector/images/lane_image.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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

# Draw the detected leftmost and rightmost road boundaries
road_image = image.copy()
cv2.circle(road_image, leftmost, 10, (0, 255, 0), -1)  # Leftmost point
cv2.circle(road_image, rightmost, 10, (0, 255, 0), -1)  # Rightmost point

# Draw a line between the leftmost and rightmost points (representing road width)
cv2.line(road_image, leftmost, rightmost, (255, 0, 0), 2)

# Add text annotation showing the road width in feet
font = cv2.FONT_HERSHEY_SIMPLEX
text = f"Lane Width: {road_width_feet:.2f} ft"
cv2.putText(road_image, text, (int((leftmost[0] + rightmost[0]) / 2), leftmost[1] - 10),
            font, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

# Display the final image with the correct annotation
cv2.imshow("Lane Width in Feet", road_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print the calculated width for reference
print(f"Lane width in pixels: {road_width_pixels:.2f} pixels")
print(f"Lane width in meters: {road_width_meters:.2f} meters")
print(f"Lane width in feet: {road_width_feet:.2f} feet")
