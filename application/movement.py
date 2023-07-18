import cv2

# Load video file
cap = cv2.VideoCapture("1.mp4")

while True:
    # Read first frame
    ret, frame1 = cap.read()

    # Check if frame was successfully read
    if not ret:
        print("Unable to read frame")
        break

    # Read second frame
    ret, frame2 = cap.read()

    # Check if frame was successfully read
    if not ret:
        print("Unable to read frame")
        break

    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Compute absolute difference between frames
    diff = cv2.absdiff(gray1, gray2)

    # Threshold difference image to create binary image
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    # Find contours
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        # Find bounding rectangle for contour
        x,y,w,h = cv2.boundingRect(c)
        prev_x, prev_y = x, y
        # Check if fire has moved
        if abs(x - prev_x) > 10 or abs(y - prev_y) > 10:
            fire_movement = True
        else:
            fire_movement = False



    # Update frame1
    frame1 = frame2

# Release video capture
cap.release()
cv2.destroyAllWindows()
