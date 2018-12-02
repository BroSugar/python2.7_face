import numpy as np
import cv2
import requests
from json import JSONDecoder
import os
import time

def camera():
    face_cascade = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    count = 0
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            cv2.imwrite("Face/face" + str(count) + '.jpg', gray[y:y + h, x:x + w])
        cv2.imshow('img', img)
        if count > 10:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def save_pricame():
    w_size = []
    for i in range(1, 11):
        fn = "Face/face" + str(i) + ".jpg"
        # print 'load %s as ...' % fn
        img = cv2.imread(fn)
        sp = img.shape
        # print sp
        sz1 = sp[0]  # height(rows) of image
        sz2 = sp[1]  # width(colums) of image
        sz3 = sp[2]  # the pixels value is made up of three primary colors
        # print 'width: %d \nheight: %d \nnumber: %d' % (sz1, sz2, sz3)
        w_size.append(sz2)
    a = w_size
    b = max(w_size)
    c = a.index(b)
    c += 1
    print(c)
    return c;


def drawFace(face_rectangle,img):
    width=face_rectangle['width']
    top = face_rectangle['top']
    left = face_rectangle['left']
    height = face_rectangle['height']
    start = (left, top)
    end = (left + width, top + height)
    color = (55, 255, 155)
    thickness = 3
    cv2.rectangle(img, start, end, color, thickness)

def  cheack():
    compare_url = "https://api-cn.faceplusplus.com/facepp/v3/compare"
    key = "SASuuvcBxQmaweSsUH06xeV3ouCdjrLU"
    secret = "JP6XgFiqH7zMZSh0nUh0LngyYg8Fe0UQ"
    faceId1 = "face2.jpg"
    faceId2 = "Face/face" + str(save_pricame()) + ".jpg"
    data = {"api_key": key, "api_secret": secret}
    files = {"image_file1": open(faceId1, "rb"), "image_file2": open(faceId2, "rb")}
    # file_2 = {"image_file2": open(faceId2, "rb")}
    response = requests.post(compare_url, data=data, files=files)
    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)
    # print req_dict

    confindence = req_dict['confidence']
    print(confindence)

    face_rectangle_1 = req_dict['faces1'][0]['face_rectangle']
    # print(face_rectangle_1)
    face_rectangle_2 = req_dict['faces2'][0]['face_rectangle']
    img1 = cv2.imread(faceId1)
    img2 = cv2.imread(faceId2)
    if confindence >= 70:
        drawFace(face_rectangle_1, img1)
        drawFace(face_rectangle_2, img2)
        img1 = cv2.resize(img1, (500, 500))
        img2 = cv2.resize(img2, (500, 500))
        cv2.imshow("img1", img1)
        cv2.imshow("img2", img2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def text():
    camera()
    cheack()


text()
os.system("pause")
