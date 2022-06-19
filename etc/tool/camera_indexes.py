import cv2


RANGE = 10

for index in range(RANGE):
    cam = cv2.VideoCapture(index)
    if cam.read()[0]:
        print(f'cv2.VideoCapture available at index {index}.')
        cam.release()
