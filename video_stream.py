import cv2
from flask import Flask, Response

app = Flask(__name__)

def generate_frames():
    camera = cv2.VideoCapture(0)  # Open the camera

    # Set camera resolution to ultra wide
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 3000)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Set camera frame rate to 24 fps
    camera.set(cv2.CAP_PROP_FPS, 24)

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
