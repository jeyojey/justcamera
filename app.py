from flask import Flask, Response, render_template
import cv2
import signal
import sys
import os

app = Flask(__name__)

# Initialize the camera
camera = cv2.VideoCapture(0)  # 0 for default camera


def generate_frames():
    while True:
        success, frame = camera.read()  # Capture frame-by-frame
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML template


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def cleanup(*args):
    """Release the camera resource when the app stops."""
    print("Releasing camera...")
    camera.release()
    sys.exit(0)


# Handle signals for a clean exit
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

#if __name__ == "__main__":
#    app.run(debug=False, host="0.0.0.0")  # Allow connections from all IPs

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
