import cv2


cv_file = cv2.FileStorage()
cv_file.open('stereo_map.xml', cv2.FileStorage_READ)

stereo_map_left_x = cv_file.getNode('stereo_map_left_x').mat()
stereo_map_left_y = cv_file.getNode('stereo_map_left_y').mat()
stereo_map_right_x = cv_file.getNode('stereo_map_right_x').mat()
stereo_map_right_y = cv_file.getNode('stereo_map_right_y').mat()


def undistort_image(frame_left, frame_right):
    # Undistort and rectify images
    undistorted_left = cv2.remap(frame_left, stereo_map_left_x, stereo_map_left_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    undistorted_right = cv2.remap(frame_right, stereo_map_right_x, stereo_map_right_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    return undistorted_left, undistorted_right
