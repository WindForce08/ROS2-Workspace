#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
import cv2
import numpy as np
import json
import time

try:
    from cv_bridge import CvBridge
    HAS_CV_BRIDGE = True
except ImportError:
    HAS_CV_BRIDGE = False

class AIVisionNode(Node):
    def __init__(self):
        super().__init__('ai_vision_node')
        self.get_logger().info("AI Vision Node starting...")

        if HAS_CV_BRIDGE:
            self.bridge = CvBridge()
        else:
            self.get_logger().warn("cv_bridge not found. Using fallback image decoding.")

        self.image_sub = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10
        )
        self.processed_pub = self.create_publisher(Image, '/camera/image_processed', 10)
        self.detection_pub = self.create_publisher(String, '/ai/detections', 10)

        self.fps_counter = 0
        self.fps_time = time.time()
        self.fps = 0.0

    def image_callback(self, msg: Image):
        try:
            if HAS_CV_BRIDGE:
                frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            else:
                frame = np.frombuffer(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, 3))

            # AI / Object Detection Pipeline (Color & Contour Tracking Example)
            processed_frame, detections = self.process_vision_pipeline(frame)

            # Publish Processed Frame
            if HAS_CV_BRIDGE:
                out_msg = self.bridge.cv2_to_imgmsg(processed_frame, encoding='bgr8')
                out_msg.header = msg.header
                self.processed_pub.publish(out_msg)

            # Publish Detection JSON
            if detections:
                det_msg = String()
                det_msg.data = json.dumps(detections)
                self.detection_pub.publish(det_msg)

        except Exception as e:
            self.get_logger().error(f"Error processing camera frame: {e}")

    def process_vision_pipeline(self, frame):
        # Calculate FPS
        self.fps_counter += 1
        now = time.time()
        if now - self.fps_time >= 1.0:
            self.fps = self.fps_counter / (now - self.fps_time)
            self.fps_counter = 0
            self.fps_time = now

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Color Thresholding Example (Red / Orange Target Detection)
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 | mask2

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detections = []
        height, width = frame.shape[:2]

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 400:  # Minimum area threshold
                x, y, w, h = cv2.boundingRect(cnt)
                cx = x + w // 2
                cy = y + h // 2

                # Normalize coordinates (-1.0 to 1.0)
                norm_x = round((cx - (width / 2.0)) / (width / 2.0), 3)
                norm_y = round(((height / 2.0) - cy) / (height / 2.0), 3)

                detections.append({
                    "label": "target_object",
                    "bbox": [x, y, w, h],
                    "norm_center": [norm_x, norm_y],
                    "area": float(area)
                })

                # Draw bounding box and target crosshair
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                cv2.putText(frame, f"Target ({norm_x}, {norm_y})", (x, y - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Draw Overlay Text
        cv2.putText(frame, f"FPS: {self.fps:.1f} | Detections: {len(detections)}", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        return frame, detections

def main(args=None):
    rclpy.init(args=args)
    node = AIVisionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
