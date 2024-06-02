import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time
import serial

# Path of model file
file1path = "MobileNetSSD_deploy.prototxt"
file2path = "MobileNetSSD_deploy.caffemodel"
net = cv2.dnn.readNetFromCaffe(file1path, file2path)

# Labels of Network
classNames = {
    15: 'person'
}

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # Open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot = tk.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            frame_resized = cv2.resize(frame, (300, 300))  # Resize frame for prediction
            blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
            net.setInput(blob)
            detections = net.forward()

            cols = frame_resized.shape[1]
            rows = frame_resized.shape[0]

            theft_alert = False
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]  # Confidence of prediction
                if confidence > 0.5:  # Filter prediction
                    class_id = int(detections[0, 0, i, 1])  # Class label

                    # Object location
                    xLeftBottom = int(detections[0, 0, i, 3] * cols)
                    yLeftBottom = int(detections[0, 0, i, 4] * rows)
                    xRightTop = int(detections[0, 0, i, 5] * cols)
                    yRightTop = int(detections[0, 0, i, 6] * rows)

                    heightFactor = frame.shape[0] / 300.0
                    widthFactor = frame.shape[1] / 300.0
                    xLeftBottom = int(widthFactor * xLeftBottom)
                    yLeftBottom = int(heightFactor * yLeftBottom)
                    xRightTop = int(widthFactor * xRightTop)
                    yRightTop = int(heightFactor * yRightTop)

                    cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop), (0, 255, 0))

                    if class_id in classNames:
                        label = classNames[class_id] + ": " + str(confidence)
                        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                        yLeftBottom = max(yLeftBottom, labelSize[1])
                        cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
                                      (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                                      (255, 255, 255), cv2.FILLED)
                        cv2.putText(frame, label, (xLeftBottom, yLeftBottom), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
                        print(label)

                        theft_alert = True

            if theft_alert:
                try:
                    ser = serial.Serial('COM9', 9600)
                    b = ser.readline()
                    string_n = b.decode()
                    string = string_n.rstrip()
                    alert = string
                    ser.close()
                    if alert == "Theft Alert":
                        arduino = serial.Serial('COM3', 9600)
                        time.sleep(2)
                        arduino.write(b'1')
                        print("Emergency Theft Alert")
                        arduino.close()
                except Exception as e:
                    print(f"Error: {e}")

            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (False, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(tk.Tk(), "Tkinter and OpenCV")
