import cv2
import stereo_camera
from calibration import undistort_image


sc = stereo_camera.StereoCamera()

while sc.isOpened():
    _, frame_left = sc.cam_left.read()
    _, frame_right = sc.cam_right.read()

    cv2.imshow('Left Orginal', frame_left)
    cv2.imshow('Right Orginal', frame_right)

    calib_left, calib_right = undistort_image(frame_left, frame_right)
    
    cv2.imshow('Left Calibrated', calib_left)
    cv2.imshow('Right Calibrated', calib_right)

    if cv2.waitKey(1) == ord('q'):
        break

sc.release()
cv2.destroyAllWindows()
