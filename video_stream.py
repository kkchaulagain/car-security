import cv2

camera = cv2.VideoCapture(0)  # Open the camera

while True:
    ret, frame = camera.read()  # Read a frame from the camera
    cv2.imshow('Camera Stream', frame)  # Display the frame

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit when 'q' is pressed
        break

camera.release()  # Release the camera
cv2.destroyAllWindows()  # Close the window
