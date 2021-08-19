import time

from plyer.utils import platform
from plyer import notification
import cv2
from GazeTracking.gaze_tracking import GazeTracking
import numpy as np
from scipy import stats

gaze = GazeTracking()


# def webcam():
start_time = time.time()
seconds = 5

webcam = cv2.VideoCapture(0)
left_pupil = []
right_pupil = []
list_x_L = []
list_x_R = []
list_y_L = []
list_y_R = []

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time
    _, frame = webcam.read()
    frame = cv2.flip(frame, 1)
    gaze.refresh(frame)

    new_frame = gaze.annotated_frame()

    #cond = True
    #while cond:
    if gaze.horizontal_ratio() is not None:
        # left = round(gaze.pupil_right_coords(), 3)
        # right = round(gaze.pupil_right_coords(), 3)
        horizontal = round(gaze.horizontal_ratio(), 3)
        vertical = round(gaze.vertical_ratio(), 3)
        # if horizontal is None or vertical is None:
        #     notification.notify(
        #         title='Calibration',
        #         message='Error while calibration',
        #         app_name='Demo test',
        #     )
        #     time.sleep(1)
        # left_pupil.append(left)
        # right_pupil.append(right)
        # print(left_pupil, right_pupil)
        list_x_L.append(horizontal)
        list_x_R.append(gaze.pupil_right_coords()[1] - gaze.pupil_left_coords()[1])

        list_y_L.append(vertical)
        list_y_R.append(gaze.pupil_right_coords()[0] - gaze.pupil_left_coords()[0])
        # print(gaze.pupil_right_coords()[0] - gaze.pupil_left_coords()[0])

    if list_y_R and list_y_L is not None:
        mode_x_L = stats.mode(np.array(list_x_L))
        mode_x_R = stats.mode(np.array(list_x_R))
        mode_y_L = stats.mode(np.array(list_y_L))
        mode_y_R = stats.mode(np.array(list_y_R))
        cond = False

    # cv2.imshow("image", new_frame)
    cv2.imshow("image", new_frame)

    # if elapsed_time > seconds:
    #     return mode_x_L[0], mode_y_L[0],
    #     break


    # new_frame = cv2.resize(new_frame, (500, 500))
    cv2.imshow("image", new_frame)
    # print(mode_x_L[0], mode_y_L[0],)

    if cv2.waitKey(1) == 27:
        print(mode_x_L[0], mode_y_L[0], )
        # break
