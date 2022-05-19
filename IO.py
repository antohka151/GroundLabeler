import cv2
import os


def load_images_folder(folder):
    if folder is None:
        raise ValueError('Folder name is None')
    imgs = []
    for filename in os.listdir(folder):
        imgs.append(os.path.join(folder, filename))
    return imgs


def show_images(images):
    for imname in images:
        img = cv2.imread(imname)
        cv2.imshow(imname, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def load_videos_folder(folder):
    if folder is None:
        raise ValueError('Folder name is None')
    videos = []
    for filename in os.listdir(folder):
        if filename != ".gitkeep":
            videos.append(filename)
    return videos


def show_videos(videos):
    for vidname in videos:
        cap = cv2.VideoCapture(vidname)
        if cap.isOpened() is False:
            print("Error opening video stream or file")
        while cap.isOpened():
            ret, frame = cap.read()
            if ret is True:
                cv2.imshow(vidname, frame)
                if cv2.waitKey(16) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
