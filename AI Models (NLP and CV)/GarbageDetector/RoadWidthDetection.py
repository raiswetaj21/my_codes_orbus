import numpy as np
import cv2
# Check OpenCV version
print("OpenCV version:", cv2.__version__)

# Load the image
image = cv2.imread('E:/AI Models (NLP and CV)/GarbageDetector/images/road_image.jpg')

# Convert to HSV to detect black and yellow colors of the boundary
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the lower and upper bounds for yellow and black colors
lower_yellow = np.array([15, 100, 100])
upper_yellow = np.array([30, 255, 255])
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 50])

# Create masks for black and yellow colors
mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
mask_black = cv2.inRange(hsv, lower_black, upper_black)

# Combine the masks to get the black-yellow boundary
mask_boundary = cv2.bitwise_or(mask_yellow, mask_black)

# Apply the mask to the image to get the road boundaries
masked_image = cv2.bitwise_and(image, image, mask=mask_boundary)

# Find the contours of the road boundaries
contours, _ = cv2.findContours(mask_boundary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours by area to remove small noise and focus on large boundaries
boundary_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]

# Initialize variables to hold the leftmost and rightmost points for the road
leftmost = None
rightmost = None

# Iterate through contours and find the extreme leftmost and rightmost points
for contour in boundary_contours:
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

# Conversion from Pixels to Meters using the car's width
car_width_meters = 1.7  # Estimated width of the car in meters
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
text = f"Road Width: {road_width_feet:.2f} ft"
cv2.putText(road_image, text, (int((leftmost[0] + rightmost[0]) / 2), leftmost[1] - 10),
            font, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

# Display the final image with the correct annotation
cv2.imshow("Road Width in Feet", road_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print the calculated width for reference
print(f"Road width in pixels: {road_width_pixels:.2f} pixels")
print(f"Road width in meters: {road_width_meters:.2f} meters")
print(f"Road width in feet: {road_width_feet:.2f} feet")
