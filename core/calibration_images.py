import os
import cv2
import stereo_camera


num = 0
sc = stereo_camera.StereoCamera()

os.makedirs('./calibration/left')
os.makedirs('./calibration/right')

while sc.isOpened():
    _, frame_left = sc.cam_left.read()
    _, frame_right = sc.cam_right.read()

    k = cv2.waitKey(5)
    if k == ord('q'): # q for exit
        break
    elif k == ord('s'): # s for saving images
        cv2.imwrite(f'./calibration/left/imgL{num}.png', frame_left)
        cv2.imwrite(f'./calibration/right/imgR{num}.png', frame_right)
        print('images saved!')
        num += 1

    cv2.imshow('Left', frame_left)
    cv2.imshow('Right', frame_right)

sc.release()
cv2.destroyAllWindows()
