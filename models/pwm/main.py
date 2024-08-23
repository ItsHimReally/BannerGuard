import cv2
import numpy as np

video_path = "video_with_pwm.mp4"
cap = cv2.VideoCapture(video_path)
frames = []
num_frames = 10

for i in range(num_frames):
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)

frames = np.array(frames)
average_frame = np.mean(frames, axis=0).astype(np.uint8)
output_image_path = "output_image.png"
cv2.imwrite(output_image_path, average_frame)
cap.release()

print(f"Saves as {output_image_path}")
