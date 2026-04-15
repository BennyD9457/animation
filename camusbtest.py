import cv2
cap = cv2.VideoCapture(0) # 0 is the index of the USB camera
# Set properties
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# Open settings dialog (useful for manual exposure/focus)
cap.set(cv2.CAP_PROP_SETTINGS, 0)
