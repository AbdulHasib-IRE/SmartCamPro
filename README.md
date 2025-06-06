# RPi SmartCam Pro - Advanced Surveillance System 🌐

**Real-Time Video Streaming and Monitoring with Raspberry Pi**

SmartCam Pro is a surveillance camera application designed for the Raspberry Pi Zero 2 W with a compatible camera module (e.g., Camera Module v2 or v3). Built using [Flask](https://flask.palletsprojects.com), it provides a web-based interface for live video streaming, customizable camera settings, and high-resolution image capture. The interface features a responsive, dark-themed design powered by [Tailwind CSS](https://tailwindcss.com), ensuring compatibility with mobile and desktop devices. The application is configured to start automatically on Raspberry Pi boot using a systemd service, with detailed logging to `/var/log/smartcampro.log` for debugging. It is ideal for applications like home security, wildlife monitoring, and educational projects.

## Repository Structure
```
SmartCamPro/
├── app.py              # Main Flask application for backend logic
├── templates/
│   └── index.html      # Frontend HTML file with Tailwind CSS styling
├── requirements.txt    # Lists Python dependencies
├── .gitignore          # Excludes unnecessary files from version control
├── LICENSE             # MIT License file
└── README.md           # Comprehensive project documentation
```

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Applications](#applications)
- [System Requirements](#system-requirements)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Managing the Service](#managing-the-service)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Maintenance](#maintenance)
- [Security](#security)
- [Testing](#testing)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)
- [Revision History](#revision-history)

## Overview
SmartCam Pro leverages the Raspberry Pi Zero 2 W and a Pi Camera to deliver a robust surveillance solution. It provides live video streaming with customizable settings (resolution: 640x480, 1280x960, 1920x1440; FPS: Auto, 30, 60; color mode: Color, Grayscale; rotation: -90°, 0°, 90°, 180°; effect: Normal, Negative; sharpness: Low, Medium, High, Very High; compression: Low, Medium, High), high-resolution image capture at 1920x1080, and a user-friendly web interface for monitoring. The system logs events with timestamps to `/var/log/smartcampro.log` and the console, aiding debugging. Styled with Tailwind CSS via a CDN, the interface is modern and responsive, suitable for various devices. The application runs on port 5000, accessible via the Raspberry Pi’s IP address, and starts automatically on boot via a systemd service.

## Features
- **Live Video Streaming**: Real-time video feed accessible via a web browser, with a loading spinner for initialization.
- **Camera Settings**: Adjust settings including:
  - Resolution (640x480, 1280x960, 1920x1440)
  - Frames per Second (FPS) (Auto, 30, 60)
  - Color Mode (Color, Grayscale)
  - Rotation (-90°, 0°, 90°, 180°)
  - Effects (Normal, Negative)
  - Sharpness (Low, Medium, High, Very High)
  - Compression (Low, Medium, High)
- **Image Capture**: Capture high-resolution images (1920x1080) with instant preview in the browser.
- **Auto-Run on Boot**: Automatically starts on Raspberry Pi power-on using a systemd service.
- **Responsive Design**: Mobile- and desktop-compatible interface with a dark theme featuring teal and purple accents.
- **Logging**: Detailed logs for debugging, stored at `/var/log/smartcampro.log` and output to console.
- **System Status Monitoring**: Displays status, last access, transmitted data, temperature, and ping (currently static, extensible for dynamic data).

## Applications
SmartCam Pro can be applied in various scenarios:
- **Home Security**: Monitor homes or apartments for intruder detection or safety, ideal for doorways or living areas.
- **Wildlife Monitoring**: Observe animals in natural habitats or research settings for ecological studies or personal interest.
- **Industrial Inspection**: Inspect machinery or processes in industrial environments for quality control or maintenance.
- **Educational Projects**: Learn about Raspberry Pi, Python, Flask, web development, and computer vision through hands-on experimentation.
- **DIY Surveillance**: Build custom surveillance systems for personal use, such as monitoring a garage, workshop, or pet areas.

## System Requirements

### Hardware
| Component                | Description                                      |
|--------------------------|--------------------------------------------------|
| **Raspberry Pi**         | Zero 2 W or higher (e.g., Pi 3, Pi 4) with a compatible camera module. |
| **Pi Camera Module**     | Camera Module v2 or v3 for video streaming and image capture. |
| **Power Supply**         | Stable 5V power supply (2.5A recommended for Zero 2 W with camera). |
| **MicroSD Card**        | 16GB or larger (32GB recommended) with Raspberry Pi OS installed. |
| **Monitor/Keyboard**     | Optional for initial setup (can use SSH or VNC). |

### Software
- **Operating System**: Raspberry Pi OS (Debian-based, preferably Bookworm, Lite or Desktop).
- **Python**: Version 3.9 or higher (included with Raspberry Pi OS).
- **Dependencies**:
  - **System**: `python3-picamera2`, `git`, `python3-venv`.
  - **Python**: `flask`, `picamera2`, `opencv-python`, `numpy` (listed in `requirements.txt`).
- **Network**: Internet connection for Tailwind CSS CDN and initial dependency installation; local network for accessing the web interface.

## Installation and Setup

### Prerequisites
Ensure your Raspberry Pi is updated and has the necessary tools installed:
1. Update the system:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
2. Install required tools for development and camera support:
   ```bash
   sudo apt install -y git python3-venv python3-picamera2
   ```

### Enabling the Camera
1. Open the Raspberry Pi configuration tool:
   ```bash
   sudo raspi-config
   ```
2. Navigate to `Interface Options` > `Camera` (or `Legacy Camera` in older OS versions).
3. Enable the camera and select `Finish`.
4. Reboot if prompted:
   ```bash
   sudo reboot
   ```

### Steps to Set Up
1. **Clone the Repository**:
   - Clone the repository to your Raspberry Pi:
     ```bash
     git clone https://github.com/AbdulHasib-IRE/SmartCamPro.git
     cd SmartCamPro
     ```
    

2. **Set Up Virtual Environment**:
   - Create a virtual environment with access to system packages (required for `picamera2`):
     ```bash
     python3 -m venv --system-site-packages venv
     source venv/bin/activate
     ```
   - Install Python dependencies listed in `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

3. **Test the Application Manually**:
   - Run the application to ensure it works:
     ```bash
     python app.py
     ```
   - Find the Raspberry Pi’s IP address:
     ```bash
     hostname -I
     ```
   - Open a web browser on a device on the same network and navigate to `http://<your-pi-ip>:5000` (e.g., `http://192.168.1.100:5000`).
   - Verify the live video feed, settings adjustments, and image capture functionality.
   - Stop the test with `Ctrl+C`.

4. **Configure Logging**:
   - Create a log directory and file with appropriate permissions:
     ```bash
     sudo mkdir -p /var/log
     sudo touch /var/log/smartcampro.log
     sudo chown pi:pi /var/log/smartcampro.log
     sudo chmod 664 /var/log/smartcampro.log
     ```
   - Alternatively, modify `app.py` to log to a user-writable directory (e.g., `./smartcampro.log`) to avoid `sudo`:
     ```python
     logging.basicConfig(
         level=logging.INFO,
         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
         handlers=[
             logging.FileHandler('./smartcampro.log'),
             logging.StreamHandler(sys.stdout)
         ]
     )
     ```

5. **Set Up Systemd Service for Auto-Run**:
   - Create a systemd service file:
     ```bash
     sudo nano /etc/systemd/system/smartcampro.service
     ```
   - Paste the following content:
     ```
     [Unit]
     Description=SmartCam Pro Surveillance Camera Service
     After=network.target

     [Service]
     User=pi
     WorkingDirectory=/home/pi/SmartCamPro
     ExecStart=/home/pi/SmartCamPro/venv/bin/python3 /home/pi/SmartCamPro/app.py
     Restart=always
     StandardOutput=journal
     StandardError=journal
     Environment="PATH=/home/pi/SmartCamPro/venv/bin:/usr/local/bin:/usr/bin:/bin"

     [Install]
     WantedBy=multi-user.target
     ```
     Replace `/home/pi/SmartCamPro` with your project directory if different.
   - Save and exit (`Ctrl+X`, `Y`, `Enter`).

6. **Enable and Start the Service**:
   - Reload systemd:
     ```bash
     sudo systemctl daemon-reload
     ```
   - Enable the service to start on boot:
     ```bash
     sudo systemctl enable smartcampro.service
     ```
   - Start the service:
     ```bash
     sudo systemctl start smartcampro.service
     ```

7. **Verify Setup**:
   - Check the service status:
     ```bash
     sudo systemctl status smartcampro.service
     ```
     Look for `Active: active (running)`.
   - Access the interface at `http://<your-pi-ip>:5000`.
   - Check logs for errors:
     ```bash
     cat /var/log/smartcampro.log
     ```

8. **Test Auto-Run on Boot**:
   - Reboot the Raspberry Pi:
     ```bash
     sudo reboot
     ```
   - Verify the service is running:
     ```bash
     sudo systemctl status smartcampro.service
     ```
   - Access the interface to confirm functionality.

## Usage

### Accessing the Interface
- Open a web browser on any device on the same network.
- Navigate to `http://<your-pi-ip>:5000` (e.g., `http://192.168.1.100:5000`).
- The interface displays:
  - **Live Video Feed**: Real-time stream with a loading spinner during initialization.
  - **Camera Settings**: Dropdowns for adjusting settings.
  - **Capture Image**: Button for high-resolution photo capture with preview.
  - **System Status**: Static display (extensible for dynamic data).

### Live Video Feed
- The “Live Video Feed” section shows a real-time stream from the Pi Camera.
- Adjust settings to optimize stream quality based on network and hardware.

### Camera Settings
- Use the “Camera Settings” panel to adjust:
  - **Monitor**: Toggle streaming (Yes/No).
  - **Resolution**: 640x480, 1280x960, 1920x1440.
  - **Compression**: Low, Medium, High.
  - **FPS**: Auto, 30, 60.
  - **Color Mode**: Color, Grayscale.
  - **Rotation**: -90°, 0°, 90°, 180°.
  - **Effect**: Normal, Negative.
  - **Sharpness**: Low, Medium, High, Very High.
- Click “Apply Settings” to save changes. A confirmation alert appears on success.

### Image Capture
- Click “Capture Image” to take a 1920x1080 photo, saved as `captured_image.jpg`.
- The image displays below the button for preview.
- Access saved images in the project directory.

## Managing the Service
- **Stop the Service**:
  ```bash
  sudo systemctl stop smartcampro.service
  ```
- **Restart the Service**:
  ```bash
  sudo systemctl restart smartcampro.service
  ```
- **Disable Auto-Start**:
  ```bash
  sudo systemctl disable smartcampro.service
  ```
- **View Service Logs**:
  ```bash
  journalctl -u smartcampro.service -b
  ```

## Customization
SmartCam Pro is highly customizable:
- **Web Interface**: Modify `templates/index.html` to change layout, add controls, or update Tailwind CSS styling.
- **Camera Settings**: Adjust defaults in `app.py` (e.g., `current_resolution = (1280, 960)`).
- **System Status**: Add dynamic data:
  - **Temperature**:
    ```python
    import subprocess
    temp = subprocess.check_output(["vcgencmd", "measure_temp"]).decode().strip()
    ```
  - **Ping**:
    ```python
    import subprocess
    ping = subprocess.check_output(["ping", "-c", "1", "8.8.8.8"]).decode()
    ```
- **Features**:
  - Add motion detection using OpenCV.
  - Integrate cloud storage (e.g., Google Drive API).
  - Send email alerts for events (e.g., using `smtplib`).
- **Logging**: Change log path in `app.py` to `./smartcampro.log` to avoid `sudo`.
- **Camera Module**: Use Camera Module 3 or other compatible modules, ensuring `picamera2` compatibility.
- **Effects**: Extend `gen_frames()` for additional image processing (e.g., edge detection).

## Troubleshooting
| Issue                     | Possible Cause                     | Solution                                                                 |
|---------------------------|------------------------------------|--------------------------------------------------------------------------|
| **Camera Not Detected**   | Camera not connected or disabled   | Verify CSI port connection (blue ribbon up). Enable camera in `raspi-config`. Run `vcgencmd get_camera` (should show `detected=1`). |
| **Video Feed Not Displaying** | Server not running or network issue | Ensure server is running (`sudo systemctl status smartcampro.service`). Check IP/port 5000. Verify network connectivity. |
| **Settings Not Applying** | Form data or server error          | Check browser console and `/var/log/smartcampro.log`. Ensure valid inputs. |
| **Image Capture Failing** | Storage or config issue            | Verify write permissions (`chmod u+rw .`). Check camera config in `app.py`. |
| **Service Fails to Start**| Incorrect paths or permissions     | Check `smartcampro.service` paths. Verify permissions (`chown pi:pi`). Review `journalctl -u smartcampro.service -b`. |
| **High CPU Usage**       | High resolution/FPS                | Use 640x480 and 30 FPS. Monitor with `top`.                              |
| **Log Permission Error**  | No access to `/var/log`            | Use `sudo` or change log path to `./smartcampro.log`.                    |

## Maintenance
- **Logs**:
  - View systemd logs:
    ```bash
    journalctl -u smartcampro.service -b
    ```
  - View application logs:
    ```bash
    cat /var/log/smartcampro.log
    ```
  - Back up logs:
    ```bash
    cp /var/log/smartcampro.log ~/smartcampro_backup.log
    sudo truncate -s 0 /var/log/smartcampro.log
    ```
- **Updates**:
  - Update Python packages:
    ```bash
    source venv/bin/activate
    pip install --upgrade -r requirements.txt
    ```
  - Update system:
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```
- **Service Config**:
  - Edit `smartcampro.service`:
    ```bash
    sudo nano /etc/systemd/system/smartcampro.service
    ```
  - Reload:
    ```bash
    sudo systemctl daemon-reload
    ```

## Security
- **Network**: Use a static IP:
  ```bash
  sudo nano /etc/dhcpcd.conf
  ```
  Add:
  ```
  interface wlan0
  static ip_address=192.168.1.100/24
  static routers=192.168.1.1
  static domain_name_servers=8.8.8.8
  ```
- **Authentication**: Add Flask-Login for password protection.
- **HTTPS**: Use NGINX as a reverse proxy with SSL.
- **Firewall**: Allow port 5000:
  ```bash
  sudo ufw allow 5000
  ```
- **Credentials**: Avoid hardcoding sensitive data in `app.py`.

## Testing
- **Camera**: Test with `rpicam-still -o test.jpg`.
- **Service**: Verify auto-start after reboot.
- **Interface**: Test on multiple devices (desktop, mobile).
- **Settings**: Apply all combinations of settings.
- **Image Capture**: Confirm images save and display.

## FAQ
- **Q: Why is the video feed lagging?**
  - A: Reduce resolution/FPS or check network stability.
- **Q: Can I use a different Raspberry Pi model?**
  - A: Yes, compatible with Pi 3, Pi 4, etc., with a Pi Camera.
- **Q: How do I access logs?**
  - A: Use `cat /var/log/smartcampro.log` or `journalctl -u smartcampro.service`.

## Contributing
To contribute:
1. Fork the repository.
2. Create a branch (`git checkout -b feature/your-feature`).
3. Make and test changes.
4. Commit with clear messages (`git commit -m "Add feature"`).
5. Push to your fork (`git push origin feature/your-feature`).
6. Submit a pull request with a detailed description.
Follow PEP 8 and include documentation.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file.

## Contact
For support, open an issue at [https://github.com/AbdulHasib-IRE/SmartCamPro/issues](https://github.com/AbdulHasib-IRE/SmartCamPro/issues) or email [sm.abdulhasib.bd@gmail.com]. 

## Acknowledgments
- [Flask](https://flask.palletsprojects.com) for the web framework.
- [Tailwind CSS](https://tailwindcss.com) for styling.
- [Picamera2](https://github.com/raspberrypi/picamera2) for camera control.
- Raspberry Pi community for tutorials and resources.

## Revision History
- **Last Updated**: 01:54 AM +06, Saturday, June 07, 2025.
