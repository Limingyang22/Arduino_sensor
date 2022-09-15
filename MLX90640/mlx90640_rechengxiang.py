# -*- coding: utf-8 -*-

import sys
import datetime as dt
import numpy as np
import cv2
import serial
import serial.tools.list_ports
import time


def getTempArray(ser_data):
    datum_error = False
    T_a = (int(ser_data[1540]) + int(ser_data[1541]) * 256) / 100
    print('T_a:', T_a)
    raw_data = ser_data[4:1540]  # getting raw array of pixels temperature
    T_array = np.frombuffer(raw_data, dtype=np.int16)
    if 0 < min(T_array) < 4500:
        pass
    else:
        datum_error = True
    return T_a, T_array, datum_error


def td2Image(f):
    Tmax = 45
    Tmin = 15
    norm = np.uint8((f / 100 - Tmin) * 255 / (Tmax - Tmin))
    norm.shape = (24, 32)
    return norm


ser = serial.Serial('com3', 115200, timeout=1000)
if __name__ == "__main__":
    while True:
        data = ser.read(1544)
        if data[0] == 0x5a and data[1] == 0x5a:
            if data[2] == 0x02 and data[3] == 0x06:
                Ta, temp_array, f = getTempArray(data)
                print(temp_array)
                if f:
                    continue
                ta_img = td2Image(temp_array)
                img = cv2.applyColorMap(ta_img, cv2.COLORMAP_JET)
                img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_CUBIC)
                img = cv2.flip(img, 1)
                text = 'Envirment: {:.1f}'.format(Ta)
                blur = cv2.GaussianBlur(img, (5, 5), 0)
                median = cv2.medianBlur(blur, 5)
                x_s = int(median.shape[1] * 0.15)
                y_s = int(median.shape[0] * 0.8)
                cv2.putText(median, text, (x_s, y_s), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 1)
                cv2.imshow('Heatmap', median)
                c = cv2.waitKey(1) & 0xFF  # if 's' is pressed - saving of picture
                if c == ord("s"):
                    fname = 'pic_' + dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.jpg'
                    cv2.imwrite(fname, img)
                    print('Saving image ', fname)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    ser.close()
    cv2.destroyAllWindows()
