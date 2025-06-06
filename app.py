from flask import Flask, render_template, Response, request, send_file, jsonify
from picamera2 import Picamera2
import cv2
import numpy as np
import logging
import os
import sys
import time

# Set up logging to both file and console, with timestamp
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/smartcampro.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(_name_)

app = Flask(_name_, template_folder='templates')

# Global settings
current_resolution = (640, 480)
current_fps_str = "30"
current_color_mode = "Color"
current_rotation = 0
current_effect = "Normal"
current_sharpness_str = "Medium"
current_compression = "High"

# Mappings
SHARPNESS_LEVELS = {"Low": -50, "Medium": 0, "High": 50, "Very High": 100}
COMPRESSION_QUALITY = {"High": 95, "Medium": 75, "Low": 50}
FPS_MAPPING = {"30": 30.0, "60": 60.0}

# Initialize the camera with a delay to ensure hardware readiness
time.sleep(5)  # Wait 5 seconds for camera to stabilize on boot
try:
    camera = Picamera2()
    default_config = camera.create_video_configuration(main={"size": current_resolution, "format": "RGB888"})
    camera.configure(default_config)
    camera.start()
    logger.info("Camera initialized successfully at %s", time.strftime("%H:%M:%S %z on %Y-%m-%d"))
except Exception as e:
    logger.error("Failed to initialize camera: %s", e)
    sys.exit(1)

def gen_frames():
    while True:
        try:
            frame = camera.capture_array()
            if current_color_mode == "Gray":
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
            if current_effect == "Negative":
                frame = 255 - frame
            ret, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, COMPRESSION_QUALITY[current_compression]])
            if not ret:
                logger.warning("Failed to encode frame")
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        except Exception as e:
            logger.error("Error in gen_frames: %s", e)
            break

@app.route('/')
def index():
    logger.info("Rendering index page at %s", time.strftime("%H:%M:%S %z on %Y-%m-%d"))
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    logger.info("Streaming video feed at %s", time.strftime("%H:%M:%S %z on %Y-%m-%d"))
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/set_settings', methods=['POST'])
def set_settings():
    global current_resolution, current_fps_str, current_color_mode, current_rotation, current_effect, current_sharpness_str, current_compression

    try:
        monitor = request.form.get('monitor', 'No')
        if monitor == "No":
            logger.info("Monitoring turned off via settings at %s", time.strftime("%H:%M:%S %z on %Y-%m-%d"))
            return jsonify({"status": "success", "message": "Monitoring turned off"})

        new_resolution = request.form.get('resolution', '640x480')
        width, height = map(int, new_resolution.split('x'))
        new_fps_str = request.form.get('fps', '30')
        new_color_mode = request.form.get('colorMode', 'Color')
        new_rotation = int(request.form.get('rotation', 0))
        new_effect = request.form.get('effect', 'Normal')
        new_sharpness_str = request.form.get('sharpness', 'Medium')
        new_compression = request.form.get('compression', 'High')

        camera.stop()
        new_config = camera.create_video_configuration(main={"size": (width, height), "format": "RGB888"})
        if new_fps_str != "Auto":
            new_fps = FPS_MAPPING.get(new_fps_str, 30.0)
            new_config["controls"]["FrameRate"] = new_fps
        camera.configure(new_config)
        sharpness_value = SHARPNESS_LEVELS.get(new_sharpness_str, 0)
        camera.set_controls({"Sharpness": sharpness_value, "Rotation": new_rotation})
        camera.start()

        current_resolution = (width, height)
        current_fps_str = new_fps_str
        current_color_mode = new_color_mode
        current_rotation = new_rotation
        current_effect = new_effect
        current_sharpness_str = new_sharpness_str
        current_compression = new_compression

        logger.info("Settings applied: Resolution=%s, FPS=%s, ColorMode=%s, Rotation=%d, Effect=%s, Sharpness=%s, Compression=%s at %s",
                    new_resolution, new_fps_str, new_color_mode, new_rotation, new_effect, new_sharpness_str, new_compression, time.strftime("%H:%M:%S %z on %Y-%m-%d"))
        return jsonify({"status": "success", "message": "Settings applied"})
    except Exception as e:
        logger.error("Error applying settings: %s at %s", e, time.strftime("%H:%M:%S %z on %Y-%m-%d"))
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/capture_image', methods=['POST'])
def capture_image():
    try:
        camera.stop()
        camera_config = camera.create_still_configuration(main={"size": (1920, 1080)})
        camera.configure(camera_config)
        camera.start()
        camera.capture_file("captured_image.jpg")
        camera.stop()
        camera_config = camera.create_video_configuration(main={"size": current_resolution, "format": "RGB888"})
        camera.configure(camera_config)
        camera.start()
        logger.info("Image captured successfully at %s", time.strftime("%H:%M:%S %z on %Y-%m-%d"))
        return jsonify({"status": "success", "message": "Image captured"})
    except Exception as e:
        logger.error("Error capturing image: %s at %s", e, time.strftime("%H:%M:%S %z on %Y-%m-%d"))
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get_image')
def get_image():
    try:
        logger.info("Serving captured image at %s", time.strftime("%H:%M:%S %z on %Y-%m-%d"))
        return send_file('captured_image.jpg', mimetype='image/jpeg')
    except Exception as e:
        logger.error("Error sending image: %s at %s", e, time.strftime("%H:%M:%S %z on %Y-%m-%d"))
        return jsonify({"status": "error", "message": "Image not available"}), 404

if _name_ == '_main_':
    logger.info("Starting SmartCam Pro Flask application at %s", time.strftime("%H:%M:%S %z on %Y-%m-%d"))
    app.run(host='0.0.0.0', port=5000, threaded=True)
