import cv2
import numpy as np
import imutils
import time
import logging
import argparse

# ==============================
# Configuration
# ==============================

# Default values
GREEN_LOWER = (20, 60, 60)
GREEN_UPPER = (80, 255, 255)
FRAME_WIDTH = 1200
LATERAL_THRESHOLD = 100  # Pixels to the left/right from center to consider as 'Left' or 'Right'
MIN_RADIUS = 10  # Minimum radius to consider as valid detection
FRAME_TITLE = 'Ball Tracking'

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s: %(message)s',
    datefmt='%H:%M:%S'
)

# ==============================
# Function Definitions
# ==============================

def initialize_video_capture(mode, ip_address=None):
    """
    Initialize the video capture object based on the selected mode.
    """
    if mode == 'web':
        logging.info("Initializing webcam video capture")
        cap = cv2.VideoCapture(0)  # Default webcam index
    elif mode == 'mobile' and ip_address:
        logging.info(f"Initializing mobile camera video capture from URL: {ip_address}")
        cap = cv2.VideoCapture(f'http://{ip_address}:8080/video')
    else:
        logging.error("Invalid mode or missing IP address for mobile mode")
        return None

    if not cap.isOpened():
        logging.error("Failed to open video capture")
        return None
    logging.info("Video capture initialized successfully")
    return cap

def process_frame(frame):
    """
    Process the frame to detect the green ball and determine its position.
    """
    # Resize frame for consistency
    frame = imutils.resize(frame, width=FRAME_WIDTH)
    logging.debug("Frame resized")

    # Blur the frame to reduce noise
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    logging.debug("Frame blurred for noise reduction")

    # Convert frame from BGR to HSV color space
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    logging.debug("Frame converted to HSV color space")

    # Create mask for green color
    mask = cv2.inRange(hsv, GREEN_LOWER, GREEN_UPPER)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    logging.debug("Mask for green color created and processed")

    # Find contours in the mask
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    logging.debug(f"{len(cnts)} contours found in mask")

    center = None
    direction = "Not Detected"

    if cnts:
        # Find the largest contour
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)

        if M["m00"] > 0 and radius > MIN_RADIUS:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            logging.debug(f"Ball detected at position: {center} with radius: {radius}")

            # Draw the circle and centroid on the frame
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            # Determine direction based on position
            frame_center = FRAME_WIDTH // 2
            if center[0] < frame_center - LATERAL_THRESHOLD:
                direction = "Left"
            elif center[0] > frame_center + LATERAL_THRESHOLD:
                direction = "Right"
            else:
                direction = "Center"

            logging.info(f"Ball direction: {direction}")
        else:
            logging.debug("Detected contour is too small to be considered")
    else:
        logging.info("No ball detected in frame")

    # Draw direction text on frame
    cv2.putText(
        frame,
        f"Direction: {direction}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0) if direction != "Not Detected" else (0, 0, 255),
        2
    )

    # Draw center lines
    draw_guidelines(frame)

    return frame

def draw_guidelines(frame):
    """
    Draw guidelines on the frame to indicate center and thresholds.
    """
    height, width = frame.shape[:2]
    center_x = width // 2

    # Draw center line
    cv2.line(frame, (center_x, 0), (center_x, height), (255, 0, 0), 2)

    # Draw left threshold line
    cv2.line(frame, (center_x - LATERAL_THRESHOLD, 0), (center_x - LATERAL_THRESHOLD, height), (0, 255, 0), 1)

    # Draw right threshold line
    cv2.line(frame, (center_x + LATERAL_THRESHOLD, 0), (center_x + LATERAL_THRESHOLD, height), (0, 255, 0), 1)

    logging.debug("Guidelines drawn on frame")

def main(args):
    """
    Main function to run the ball tracking.
    """
    cap = initialize_video_capture(args.mode, args.ip)
    if cap is None:
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logging.error("Failed to read frame from video capture")
                break

            processed_frame = process_frame(frame)

            # Display the resulting frame
            cv2.imshow(FRAME_TITLE, processed_frame)

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                logging.info("Exit command received - terminating")
                break
    except Exception as e:
        logging.exception(f"An error occurred: {e}")
    finally:
        # Release resources
        cap.release()
        cv2.destroyAllWindows()
        logging.info("Resources released and program terminated")

# ==============================
# Run the Program
# ==============================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ball Tracking with OpenCV")
    parser.add_argument('--mode', type=str, choices=['web', 'mobile'], default='web',
                        help="Selects the mode of operation (web or mobile)")
    parser.add_argument('--ip', type=str, help="Specifies the IP address of your mobile camera (only required for mobile mode)")

    args = parser.parse_args()
    main(args)
