import csv
import os
import pandas as pd
import tkinter as tk
from imutils import resize
import numpy as np
import cv2
import pyautogui
from tkinter import *
import main
from GazeTracking.gaze_tracking.gaze_tracking import GazeTracking
import time

tk = Tk()
tk.resizable(0, 0)
gaze = GazeTracking()
c = Canvas(tk, width=400, height=400, bg='light grey')
c.pack()
list_cords = []
dist_x = 0
dist_y = 0
mid_list = []
list_dist = []
x = 0
y = 0
click = 0
resolution = (1920, 1080)

codec = cv2.VideoWriter_fourcc(*"XVID")

filename = "Recording2.avi"

fps = 9
out = cv2.VideoWriter(filename, codec, fps, resolution)


def test_demo():
    new_drawing_window = Toplevel(tk)
    new_drawing_window.title("Drawing window")
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    drawing_canvas = Canvas(new_drawing_window, width=width, height=height, background="black")
    drawing_canvas.pack()

    global X_left_coef, Y_left_coef, list_cords, dist_x, koef_dist_x, x, y
    drawing_canvas.pack()
    while len(list_cords) < 4:

        if len(list_cords) > 1:
            drawing_canvas.create_oval(width / 2, y, width / 2 + 30, y + 30, fill='red')
            tk.update()
            time.sleep(1.5)
            y = height - 100
            x_L, y_L, rad_x = main.webcam()
            list_cords.append((x_L, y_L))
            drawing_canvas.delete("all")
        else:
            drawing_canvas.create_oval(x, height / 2, x + 30, height / 2 + 30, fill='red')
            tk.update()
            time.sleep(1.5)
            x = x + width - 40
            x_L, y_L, rad_x = main.webcam()
            list_cords.append((x_L, y_L))
            drawing_canvas.delete("all")

        print(f' X - {x_L}')
        print(f' Y - {y_L}')

        print(f' X canvas - {width}')
        print(f' Y canvas- {height}')
        print(f'list {list_cords}')

        try:
            X_left_coef = width / (list_cords[1][0][0] - list_cords[0][0][0])
            Y_left_coef = height / (list_cords[3][1][0] - list_cords[2][1][0])
            koef_dist_x = int(dist_x / 4)
            print(f'X_left_coef {X_left_coef}')
            print(f'Y_left_coef {Y_left_coef}')
        except:
            pass

    drawing_canvas.delete("all")
    time.sleep(2)

    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)
    while True:
        _, frame = webcam.read()
        frame = cv2.flip(frame, 1)
        gaze.refresh(frame)
        img = pyautogui.screenshot()
        screen_frame = np.array(img)
        screen_frame1 = cv2.cvtColor(screen_frame, cv2.COLOR_BGR2RGB)
        cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Live", 1920, 1080)

        if gaze.horizontal_ratio() is not None:
            horizontal = round(gaze.horizontal_ratio(), 3)
            vertical = round(gaze.vertical_ratio(), 3)
            x1 = int((horizontal - list_cords[0][0][0]) * X_left_coef)
            y1 = int((vertical - list_cords[2][1][0]) * Y_left_coef)

            if vertical > list_cords[3][1][0]:
                x1 = int((horizontal - list_cords[0][0][0]) * X_left_coef)
                y1 = list_cords[3][1][0]

            if vertical < list_cords[2][1][0]:
                x1 = int((horizontal - list_cords[0][0][0]) * X_left_coef)
                y1 = list_cords[2][1][0]

            if horizontal > list_cords[1][0][0]:
                x1 = list_cords[1][0][0]
                y1 = int((vertical - list_cords[2][1][0]) * Y_left_coef)

            if horizontal < list_cords[0][0][0]:
                x1 = list_cords[0][0][0]
                y1 = int((vertical - list_cords[2][1][0]) * Y_left_coef)

            circle = cv2.circle(screen_frame1, (int(x1), int(y1)), 10, (255, 255, 0), -2)

            with open("coordinates2.csv", 'a', newline="") as file:
                writer = csv.writer(file)
                if os.stat("coordinates2.csv").st_size == 0:
                    writer.writerow(
                        ["x", "y"])
                try:
                    writer.writerow([str(x1), str(y1)])
                except KeyError:
                    print("something wrong with writing to the file")

            out.write(circle)

            cv2.imshow('Live', circle)

            if cv2.waitKey(1) == ord('q'):
                break
        else:
            pass

    cv2.destroyAllWindows()


b3 = Button(text="Demo start", width=15, height=3, command=test_demo, bg="gray")
b3.place(x=40, y=100)


tk.mainloop()
