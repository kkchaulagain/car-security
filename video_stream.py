import cv2
from flask import Flask, Response

app = Flask(__name__)

# Placeholder value for FOV (replace with the actual FOV of your camera module)
FOV_DEGREES = 120.0

def generate_frames():
    camera = cv2.VideoCapture(0)  # Open the camera

    # Print camera properties
    print("Camera Properties:")
    print("Resolution:", camera.get(cv2.CAP_PROP_FRAME_WIDTH), "x", camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("FOV (degrees):", FOV_DEGREES)
    print("Framerate (fps):", camera.get(cv2.CAP_PROP_FPS))

    while True:
        success, frame = camera.read()  # Read a frame from the camera

        if not success:
            break

        # Resize the frame to fit the display
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Convert the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)

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
