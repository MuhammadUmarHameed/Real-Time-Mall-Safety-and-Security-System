import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time
import numpy as np
import serial

class App:
    def __init__(self, window, window_title, video_source=1):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # Open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        fire_count = 0
        fire_alert = False

        ret, frame = self.vid.get_frame()
        if ret:
            blur = cv2.GaussianBlur(frame, (15, 15), 0)
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

            lower = [0, 74, 200]
            upper = [18, 166, 230]

            lower = np.array(lower, dtype='uint8')
            upper = np.array(upper, dtype='uint8')

            mask = cv2.inRange(hsv, lower, upper)
            output = cv2.bitwise_and(frame, hsv, mask=mask)

            number_of_total = cv2.countNonZero(mask)

            if number_of_total > 10000:
                print("Fire Alert in Camera")
                try:
                    ser = serial.Serial('COM3', 9600)
                    temp_read = ser.readline().decode().rstrip()
                    flame_read = ser.readline().decode().rstrip()

                    if flame_read == 'FIRE ALERT':
                        fire_count += 1
                        fire_alert = True
                        print(f"Fire count: {fire_count}")

                    ser.close()
                except Exception as e:
                    print(f"Error in serial communication: {e}")

            if number_of_total > 5000 and fire_alert:
                try:
                    arduino = serial.Serial('COM3', 9600)
                    time.sleep(2)
                    arduino.write(b'1')
                    print("Buzzer turned ON")
                    arduino.close()
                except Exception as e:
                    print(f"Error activating buzzer: {e}")

            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(output))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)

        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

App(tk.Tk(), "Tkinter and OpenCV")
