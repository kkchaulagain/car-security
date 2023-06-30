import cv2
import numpy as np
from flask import Flask, Response

app = Flask(__name__)

def adjust_colors(frame):
    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Adjust the color values in the HSV image
    # Modify the values based on your specific color correction requirements
    hue_shift = 0  # Adjust the hue shift
    saturation_scale = 1.2  # Adjust the saturation scale
    value_scale = 1.0  # Adjust the value scale

    hsv[..., 0] += hue_shift
    hsv[..., 1] *= saturation_scale
    hsv[..., 2] *= value_scale

    # Convert the HSV image back to BGR color space
    adjusted_frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return adjusted_frame

def generate_frames():
    camera = cv2.VideoCapture(0)  # Open the camera

    # Print camera properties
    print("Camera Properties:")
    print("Resolution:", camera.get(cv2.CAP_PROP_FRAME_WIDTH), "x", camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Framerate (fps):", camera.get(cv2.CAP_PROP_FPS))

    while True:
        success, frame = camera.read()  # Read a frame from the camera

        if not success:
            break

        # Adjust colors in the frame
        adjusted_frame = adjust_colors(frame)

        # Convert the adjusted frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', adjusted_frame)

        if not ret:
            break

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()  # Release the camera

@app.route('/')
def index():
    return "Camera Streaming"

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
