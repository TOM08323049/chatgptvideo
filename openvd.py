import cv2
import os

def extract_frames(video_path, output_folder, interval=0.5):
    # 使用OpenCV打开视频
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file {video_path}")
        return

    # 获取视频的帧率
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval)

    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        # 如果正确读取帧，ret为True
        if not ret:
            break

        # 每隔frame_interval帧处理一次
        if frame_count % frame_interval == 0:
            frame_file = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_file, frame)
            print(f"Saved {frame_file}")

        frame_count += 1

    cap.release()
    print("Done processing video.")

def process_videos_in_folder(folder_path, interval=0.5):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.mp4', '.avi', '.mov')):  # 检查文件扩展名
            video_path = os.path.join(folder_path, filename)
            output_folder = os.path.join(folder_path, os.path.splitext(filename)[0])
            extract_frames(video_path, output_folder, interval)

# 调用函数处理指定文件夹内的视频
source_folder = 'testvd'  # 设置你的视频文件夹路径
num =0.5 #0.5是指每0.5秒获取一帧图片
process_videos_in_folder(source_folder, num)