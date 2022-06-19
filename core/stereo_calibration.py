import cv2
import glob
import numpy as np


BOARD_SIZE = (9, 6)
FRAME_SIZE = (420, 420)


def find_corners(image_path: str, imgpoints: list, title: str) -> 'image':
    image_org = cv2.imread(image_path)
    image_gray = cv2.cvtColor(image_org, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(image_gray, BOARD_SIZE, None)

    if ret:
        corners = cv2.cornerSubPix(image_gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)

        cv2.drawChessboardCorners(image_org, BOARD_SIZE, corners, ret)
        cv2.imshow(title, image_org)
    return ret, image_org, image_gray


def calibrate_camera(imgpoints: list, image: 'image') -> tuple:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, FRAME_SIZE, None, None)
    height, width, channels = image.shape
    return dist, cv2.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))


if __name__ == '__main__':
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((BOARD_SIZE[0] * BOARD_SIZE[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:BOARD_SIZE[0], 0:BOARD_SIZE[1]].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints_left = [] # 2d points in image plane.
    imgpoints_right = [] # 2d points in image plane.

    image_list = zip(glob.glob('./calibration/left/*.png'), glob.glob('./calibration/right/*.png'))

    for image_left, image_right in image_list:
        ret_left, img_left, gray_left = find_corners(image_left, imgpoints_left, 'Image Left')
        ret_right, img_right, gray_right = find_corners(image_right, imgpoints_right, 'Image Right')
        if ret_left and ret_right:
            objpoints.append(objp)
        cv2.waitKey(1000)

    cv2.destroyAllWindows()


    dist_left, (newcameramtx_left, roi_left) = calibrate_camera(imgpoints_left, img_left)
    dist_right, (newcameramtx_right, roi_right) = calibrate_camera(imgpoints_right, img_right)


    flags = 0
    flags |= cv2.CALIB_FIX_INTRINSIC
    # Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
    # Hence intrinsic parameters are the same 

    criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
    ret_stereo, newcameramtx_left, dist_left, newcameramtx_right, dist_right, rot, trans, essential_matrix, fundamental_matrix = cv2.stereoCalibrate(
        objpoints, imgpoints_left, imgpoints_right,
        newcameramtx_left, dist_left, newcameramtx_right, dist_right,
        gray_left.shape[::-1], criteria_stereo, flags
    )

    rectify_scale = 1
    rect_left, rect_right, proj_matrix_left, proj_matrix_right, _, roi_left, roi_right = cv2.stereoRectify(
        newcameramtx_left, dist_left,
        newcameramtx_right, dist_right,
        gray_left.shape[::-1], rot, trans,
        rectify_scale,(0,0)
    )

    stereo_map_left = cv2.initUndistortRectifyMap(newcameramtx_left, dist_left, rect_left, proj_matrix_left, gray_left.shape[::-1], cv2.CV_16SC2)
    stereo_map_right = cv2.initUndistortRectifyMap(newcameramtx_right, dist_right, rect_right, proj_matrix_right, gray_right.shape[::-1], cv2.CV_16SC2)

    print('Saving parameters!')
    cv_file = cv2.FileStorage('stereo_map.xml', cv2.FILE_STORAGE_WRITE)

    cv_file.write('stereo_map_left_x', stereo_map_left[0])
    cv_file.write('stereo_map_left_y', stereo_map_left[1])
    cv_file.write('stereo_map_right_x', stereo_map_right[0])
    cv_file.write('stereo_map_right_y', stereo_map_right[1])

    cv_file.release()
