import cv2

# Capture video from webcam
cap = cv2.VideoCapture('1.mp4')

while True:
    # Read frame
    _, frame = cap.read()
    print(frame)

    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of fire color in HSV
    lower_fire = (0, 50, 50)
    upper_fire = (10, 255, 255)

    # Create mask
    mask = cv2.inRange(hsv, lower_fire, upper_fire)

    # Perform morphological transformations to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Find contours
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        # Find bounding rectangle for contour
        x,y,w,h = cv2.boundingRect(c)

        # Draw bounding rectangle on frame
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)

    # Display frame
    cv2.imshow("Fire Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture
cap.release()
cv2.destroyAllWindows()
