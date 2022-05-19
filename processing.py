import cv2
import os
import math
import pandas as pd
import mediapipe as mp

DESIRED_HEIGHT = 780
DESIRED_WIDTH = 780

_PRESENCE_THRESHOLD = 0.5
_VISIBILITY_THRESHOLD = 0.5

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


def get_video_auto():
    df = pd.read_csv(os.path.join("assets", "video_list.csv"))
    for idx in range(len(df)):
        if df.loc[idx, 'skipped'] == False and df.loc[idx, 'labelled'] == False:
            return df.loc[idx, 'video_path']

    print()
    print("All videos have been labelled or skipped")
    print("Trying to for a video with the flag skipped.. ")
    print()

    for idx in range(len(df)):
        if df.loc[idx, 'skipped']:
            return df.loc[idx, 'video_path']

    print()
    print("All videos have been labelled. Nice work!")
    print()
    return -1


def update_video_list(vid_names, labelled=False, skipped=False, force=False):
    df = pd.read_csv(os.path.join("assets", "video_list.csv"))
    labelled, skipped = int(labelled), int(skipped)
    if not isinstance(vid_names, list):
        vid_names = [vid_names]
    if labelled or skipped:
        for video in vid_names:
            if any(video == df['video_path']):
                index = df.index[df['video_path'] == video]
                if force:
                    df.loc[index, 'labelled'] = labelled
                    df.loc[index, 'skipped'] = skipped
                else:
                    if labelled:
                        df.loc[index, 'labelled'] = labelled
                    if skipped:
                        df.loc[index, 'skipped'] = skipped
                df.to_csv(os.path.join("assets", "video_list.csv"), index=False)
            else:
                pd.DataFrame({"video_path": video, "labelled": [labelled], "skipped": [skipped]}).to_csv(
                    os.path.join("assets", "video_list.csv"), mode='a', header=False, index=False)
    else:
        videos = [video for video in vid_names if not any(video == df['video_path'])]
        pd.DataFrame({"video_path": videos, "labelled": [0] * len(videos), "skipped": [0] * len(videos)}).to_csv(
            os.path.join("assets", "video_list.csv"), mode='a', header=False, index=False)


def process_videos(videos_path):
    if not isinstance(videos_path, list):
        videos_path = [videos_path]
    for vid_path in videos_path:
        path2check = os.path.join("assets", "videos_csv", vid_path.split('.')[0] + ".csv")
        try:
            df = pd.read_csv(path2check)
        except FileNotFoundError:
            _process_videos_get_csv([vid_path])
            df = pd.read_csv(path2check)
        cap = cv2.VideoCapture(os.path.join("assets", "videos", vid_path))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(
            os.path.join("assets", "labelling_video", "annotated_" + vid_path.split('.')[0] + '.mp4'),
            fourcc, 20.0, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        frame = 1
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break
            image_height, image_width, _ = image.shape
            scale = math.ceil((image_height / 800 + image_width / 800) / 2)

            image = cv2.rectangle(image, (0, 105), (120, 53), (255, 255, 255), -1)
            image = cv2.putText(image, str(frame), (0, 100), cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 0), scale,
                                cv2.LINE_AA)
            for kpoint_num in range(33):
                if df.loc[(frame - 1) * 33 + kpoint_num]["flag"] == 1:
                    color = (122, 160, 255)
                else:
                    color = (240, 255, 240)
                point_location = (math.floor(df.loc[(frame - 1) * 33 + kpoint_num]["x"] * image_width),
                                  math.floor(df.loc[(frame - 1) * 33 + kpoint_num]["y"] * image_height))
                image = cv2.circle(image, point_location, 2 * max(1, scale-1) + 1, color, -1, cv2.LINE_AA)
                if kpoint_num <= 10 or 17 <= kpoint_num <= 22:
                    continue
                elif kpoint_num % 2 == 0:
                    bias = -15 * scale
                else:
                    bias = 5 * scale
                image = cv2.rectangle(image, (point_location[0] + bias, point_location[1] + scale),
                                      (point_location[0] + bias + 8 * scale, point_location[1] - 6 * scale), (0, 0, 0),
                                      -1)
                image = cv2.putText(image, str(kpoint_num), (point_location[0] + bias, point_location[1]),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.2 * scale, color, max(1, scale-1), cv2.LINE_AA)
            for _ in range(10):
                out.write(image)
            frame += 1
        cap.release()
        out.release()


def _process_videos_get_csv(videos):
    if not isinstance(videos, list):
        videos = [videos]
    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5, model_complexity=2) as pose:
        files_csv = []
        for vid_name in videos:
            df = pd.DataFrame()
            frame = 1
            cap = cv2.VideoCapture(os.path.join("assets", "videos", vid_name))
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    break
                image_height, image_width, _ = image.shape
                result = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                if not result.pose_landmarks:
                    print(f'{vid_name} - frame #{frame} error')
                    frame += 1
                    continue

                tmp = pd.DataFrame(
                    [(result.pose_landmarks.landmark[i].x, result.pose_landmarks.landmark[i].y) for i in range(33)],
                    columns=['x', 'y'])
                tmp["flag"] = [0 if keypoint_id <= 28 else 1 for keypoint_id in range(33)]
                tmp["frame"] = frame
                df = pd.concat([df, tmp])
                frame += 1

            fpath = os.path.join("assets", "videos_csv", vid_name.split('.')[0] + ".csv")
            df.to_csv(fpath)
            files_csv.append(fpath)
            cap.release()
        return files_csv


# Function to clear videos_list. Supposed to be used manually.
def clear_videos_list():
    pd.DataFrame(columns=("video_path", "labelled", "skipped")).to_csv(
        os.path.join("assets", "video_list.csv"), mode='w',
        index=False)
