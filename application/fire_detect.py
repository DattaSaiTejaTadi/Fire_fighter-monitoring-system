import cv2
import numpy as np
import time

# Load the video file
video = cv2.VideoCapture("1.mp4")
fp=0
 
while True:
    # Read each frame
    (grabbed, frame) = video.read()
    if not grabbed:
        break

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(frame, (21, 21), 0)

    # Convert to HSV color space
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
 
    # Define the lower and upper bounds of the fire color
    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    # Apply color thresholding
    mask = cv2.inRange(hsv, lower, upper)

    # Apply Sobel edge detection to the masked image
    sobelx = cv2.Sobel(mask,cv2.CV_64F,1,0,ksize=5)
    sobely = cv2.Sobel(mask,cv2.CV_64F,0,1,ksize=5)
    sobel = np.sqrt(np.square(sobelx) + np.square(sobely))
    sobel = np.uint8(sobel/np.max(sobel)*255)

    # Apply binary thresholding to the Sobel image
    _, sobel_thresh = cv2.threshold(sobel, 50, 255, cv2.THRESH_BINARY)

    # Apply morphological closing to fill small gaps in the fire region
    kernel = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(sobel_thresh, cv2.MORPH_CLOSE, kernel)

    # Find contours of the fire region
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on the original frame
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 20000:
            print('Fire detected')
            fp=fp+1
            if fp==1:
                frame1=frame
                cv2.imwrite('image1.png', frame)
            time.sleep(1)
            if fp==2:
                frame2=frame
                cv2.imwrite('image2.png', frame)
                break
            cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)

    # Display the output
    cv2.imshow("Output", frame)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cv2.destroyAllWindows()
video.release()
