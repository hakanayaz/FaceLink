import cv2
import numpy as np
import sys
import os
import glob
from PIL import Image

font = cv2.FONT_HERSHEY_SIMPLEX
names = ['David', 'Hakan', 'Unknown']
bios = [
    '''seeking Master's in Electrical Engineering at Colorado School of Mines''',
    'seeking a Ph.D. in __ at Colorado School of Mines',
    'this person is not a FaceLink user.'
]


def do_face_rec(camera, face_detector, face_recognizer):
    """
    Reads frame from camera and does face rec on it.
    :param camera: The camera to read the frame from
    :param face_detector: The cv2 face detector object
    :param face_recognizer: the cv2 face recognizer object
    :return:
    """
    _, img = camera.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # print(gray)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    # print(faces)

    for (x, y, w, h) in faces:

        id, inv_conf = face_recognizer.predict(gray[y:y + h, x:x + w])
        if inv_conf < 100:
            id = names[id - 1]
            confidence = "  {0}%".format(round(100 - inv_conf))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - inv_conf))

        # According the similarity results face box will be change
        if inv_conf < 20:
            color = (0, 255, 0)  # green box
        elif inv_conf < 40:
            color = (0, 255, 255)  # yellow box
        else:
            color = (0, 0, 255)  # red box

        cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, color, 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    cv2.imshow('camera', img)
    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video -- k is for keycode


def main():
    counter = 0

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    # cam.set(3, 640)  # set video width
    # cam.set(4, 480)  # set video height

    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)  # one-tenth of video width
    minH = 0.1 * cam.get(4)  # one-tenth of video height

    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('trainer/trained_model.yml')

    while True:
        # print(cam.read())
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # print(gray)

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        # print(faces)

        for (x, y, w, h) in faces:

            id, inv_conf = face_recognizer.predict(gray[y:y + h, x:x + w])
            if inv_conf < 100:
                id = names[id-1]
                confidence = "  {0}%".format(round(100 - inv_conf))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - inv_conf))

            # According the similarity results face box will be change
            if inv_conf < 20:
                color = (0, 255, 0)    # green box
            elif inv_conf < 40:
                color = (0, 255, 255)  # yellow box
            else:
                color = (0, 0, 255)    # red box

            cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, color, 2)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)
        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video -- k is for keycode
        if k == 27:
            break

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
