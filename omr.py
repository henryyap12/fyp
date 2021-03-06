import ast
import csv
import glob
import os
import cv2
import numpy as np
import pandas as pd
from detect import detect
import time


def get_list(x):
    df = pd.DataFrame(x)
    df.to_csv('answer.csv', header=False, index=False)


def showAnswer(img, ans, question, c_w, c_h):
    for x in range(len(question)):
        if len(question) == 10:
            myans = question[x]
            cX = (myans * c_w) + c_w // 2
            cY = (x * c_h) + c_w // 2
            if ans[x] == question[x]:
                myColor = (0, 255, 0)
                cv2.circle(img, (cX, cY), 150, myColor, cv2.FILLED)
            else:
                myColor = (0, 0, 255)
                cv2.circle(img, (cX, cY), 150, myColor, cv2.FILLED)

                # CORRECT ANSWER
                myColor = (0, 255, 0)
                correctAns = ans[x]
                cv2.circle(img, ((correctAns * c_w) + c_w // 2, (x * c_h) + c_w // 2),
                           100, myColor, cv2.FILLED)
        elif len(question) == 20 or len(question) == 40:
            myans = question[x]
            cX = (myans * c_w) + c_w // 2
            cY = (x * c_h) + c_w // 2
            if ans[x] == question[x]:
                myColor = (0, 255, 0)
                cv2.circle(img, (cX, cY), 50, myColor, cv2.FILLED)
            else:
                myColor = (0, 0, 255)
                cv2.circle(img, (cX, cY), 50, myColor, cv2.FILLED)

                # CORRECT ANSWER
                myColor = (0, 255, 0)
                correctAns = ans[x]
                cv2.circle(img, ((correctAns * c_w) + c_w // 2, (x * c_h) + c_w // 2),
                           30, myColor, cv2.FILLED)
        elif len(question) == 5:
            myans = question[x]
            cX = (myans * c_w) + c_w // 2
            cY = (x * c_h) + c_w // 2
            if ans[x] == question[x]:
                myColor = (0, 255, 0)
                cv2.circle(img, (cX, cY), 200, myColor, cv2.FILLED)
            else:
                myColor = (0, 0, 255)
                cv2.circle(img, (cX, cY), 200, myColor, cv2.FILLED)

                # CORRECT ANSWER
                myColor = (0, 255, 0)
                correctAns = ans[x]
                cv2.circle(img, ((correctAns * c_w) + c_w // 2, (x * c_h) + c_w // 2),
                           100, myColor, cv2.FILLED)
        elif len(question) == 50:
            myans = question[x]
            cX = (myans * c_w) + c_w // 2
            cY = (x * c_h) + c_w // 2
            if ans[x] == question[x]:
                myColor = (0, 255, 0)
                cv2.circle(img, (cX, cY), 30, myColor, cv2.FILLED)
            else:
                myColor = (0, 0, 255)
                cv2.circle(img, (cX, cY), 30, myColor, cv2.FILLED)

                # CORRECT ANSWER
                myColor = (0, 255, 0)
                correctAns = ans[x]
                cv2.circle(img, ((correctAns * c_w) + c_w // 2, (x * c_h) + c_w // 2),
                           10, myColor, cv2.FILLED)


def omrmarking(path, csvpath, mark, choice):
    reader = csv.reader(open(csvpath))
    ANSWER_KEY = {}
    next(reader, None)
    for row in reader:
        key = int(row[0]) - 1
        ANSWER_KEY[key] = row[1]
        if row[1] == 'A' or row[1] == 'a':
            ANSWER_KEY[key] = 0
        elif row[1] == 'B' or row[1] == 'b':
            ANSWER_KEY[key] = 1
        elif row[1] == 'C' or row[1] == 'c':
            ANSWER_KEY[key] = 2
        elif row[1] == 'D' or row[1] == 'd':
            ANSWER_KEY[key] = 3
        elif row[1] == 'E' or row[1] == 'e':
            ANSWER_KEY[key] = 4
        elif row[1] is None or row[1] == '':
            ANSWER_KEY[key] = -1
        elif row[1] == 'bonus' or row[1] == 'Bonus' or row[1] == 'BONUS':
            ANSWER_KEY[key] = 'bonus'
    question = {key: val for key, val in ANSWER_KEY.items() if val != -1}

    width = 4960
    height = 7016
    # width = 850
    # height = 1050
    img = cv2.imread(path)
    img = cv2.resize(img, (width, height))
    img1 = img.copy()
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgblur = cv2.GaussianBlur(imggray, (5, 5), 1)
    kernel = np.ones((5, 8), np.uint8)
    imgthres = cv2.threshold(imgblur, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    savepath = 'C:/Users/Asus/PycharmProjects/PSM/thrs/1.png'
    cv2.imwrite(savepath, imgthres)
    if len(question) == 20 or len(question) == 10 or len(question) == 5:
        cmd = 'python detect.py --source C:/Users/Asus/PycharmProjects/PSM/thrs/1.png --img 416 --weights runs/train/yolov5s_results/weights/best.pt --conf 0.4'
    elif len(question) == 40:
        cmd = 'python detect.py --source C:/Users/Asus/PycharmProjects/PSM/thrs/1.png --img 512 --weights  runs/train/yolov5s_results/weights/best.pt --conf 0.4'
    else:
        cmd = 'python detect.py --source C:/Users/Asus/PycharmProjects/PSM/thrs/1.png --weights runs/train/yolov5s_results/weights/best.pt --conf 0.4'
    os.system(cmd)
    imgthres = cv2.morphologyEx(imgthres, cv2.MORPH_CLOSE, kernel)
    data = pd.read_csv("GFG.csv")
    arr = data.to_numpy()
    j = arr.tolist()
    x = 0
    res = []
    if len(j) < 2:
        for x in list(j)[0][1:5]:
            res.append(x)
    elif len(j) >= 2:
        for x in list(j):
            for y in list(x)[1:5]:
                res.append(y)
    # print(res)
    b = int(len(res) / 4)
    i = 0
    imglist = []
    for i in range(b):
        n = int(i * 4 + 1)
        croped_img = imgthres[int(res[int(n)]):int(res[int(n + 2)]), int(res[int(n - 1)]):int(res[int(n + 1)])]
        im = img1[int(res[int(n)]):int(res[int(n + 2)]), int(res[int(n - 1)]):int(res[int(n + 1)])]
        #print(im.shape)
        imglist.append(im)

        # cv2.imshow("sda", img1)
        # spath = "C:/Users/Asus/PycharmProjects/fyp/omr/omr%i.png" % i
        # cv2.imwrite(spath, img2)
        if i == 0:
            shape = croped_img.shape
            #print(shape)
            pppp = np.zeros((shape[0] * b, shape[1])).astype('uint8')
            pppp[shape[0] * i:shape[0] * (i + 1), :] = croped_img
            # cv2.imshow("sda", croped_img)
        else:
            croped_img = cv2.resize(croped_img, (shape[1], shape[0]))
            pppp[shape[0] * i:shape[0] * (i + 1), :] = croped_img

    # print(len(imglist))
    aaa = pppp
    question_num = len(ANSWER_KEY)

    h, w = aaa.shape
    c_h = int(h / question_num)
    c_w = int(w / float(choice))

    ans_lists = []

    for row in range(question_num):
        y1 = int(c_h * row)
        y2 = y1 + c_h
        x1 = 0
        option_list = []
        for column in range(int(choice)):
            x1 = int(c_w * column)
            x2 = x1 + c_w
            x = np.sum(aaa[y1:y2, x1:x2])
            option_list.append(x / 10000)
        ans_lists.append(option_list)
    # print(ans_lists)

    ans = []
    for ans_list in ans_lists:
        m = np.max(ans_list)
        # print(m)
        max_accept = int(m * 1.5)
        min_accept = int(m * 0.95)
        sum_of_white = np.sum(ans_lists)
        v = 1 + (1 / float(choice))
        filter = (question_num / v) * float(choice)
        filter = sum_of_white / filter

        if question_num == 50:
            filter = filter * 0.825
        elif question_num == 10 or question_num == 5:
            filter = filter * 0.9
        elif question_num == 20 or question_num == 40:
            filter = filter * 0.95
        else:
            filter = filter * 0.75
        detected_ans_num = 0
        for i in ans_list:
            if i in range(min_accept, max_accept):
                detected_ans_num += 1
        if detected_ans_num > 1:
            ans.append(999)
        else:
            if m > filter:
                ans.append(ans_list.index(m))
            else:
                ans.append(999)
    # print(ans)
    rows = []
    row = 1
    x = 0
    for x in ans:
        if x == 999:
            # print('question:', row, 'not enough swallow or empty')
            rows.append(row)
        row += 1

    correct = 0
    for y in range(len(question)):
        if ans[y] == question[y] or question[y] == 'bonus':
            correct += 1
    result = img.copy()
    j = 0
    k = 0
    i = 0
    for im in imglist:
        print(im.shape)
        print(c_w,c_h)
        showAnswer(im, ans, question, c_w, c_h)
        cv2.imwrite("mark%i.png" % i, im)
        i += 1
        n = int(j * 4 + 1)
        for j in range(b):
            result[int(res[int(n)]):int(res[int(n + 2)]), int(res[int(n - 1)]):int(res[int(n + 1)])] = im

    ans = ['a' if x == 0 else x for x in ans]
    ans = ['b' if x == 1 else x for x in ans]
    ans = ['c' if x == 2 else x for x in ans]
    ans = ['d' if x == 3 else x for x in ans]
    ans = ['e' if x == 4 else x for x in ans]
    ans = ['empty' if x == 999 else x for x in ans]
    get_list(ans)
    row = 1
    for a in ans:
        print('question : ', row, 'ans : ', a)
        row += 1
    cv2.imwrite("mark.png", result)
    score = (correct / len(question)) * int(mark)
    rows = list(rows)
    return correct, score, rows
