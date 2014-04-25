import cv2
import numpy # Hint to PyInstaller


def fourCharsToInt(s):
    import binascii
    return int(binascii.hexlify(s), 16)

def intToFourChars(i):
    import binascii
    return binascii.unhexlify(format(i, 'x'))

def intersects(rect0, rect1):
    x0, y0, w0, h0 = rect0
    x1, y1, w1, h1 = rect1
    if x0 > x1 + w1: # rect0 is wholly to right of rect1
        return False
    if x1 > x0 + w0: # rect1 is wholly to right of rect0
        return False
    if y0 > y1 + h1: # rect0 is wholly below rect1
        return False
    if y1 > y0 + h0: # rect1 is wholly below rect0
        return False
    return True

def difference(rects0, rects1):
    result = []
    for rect0 in rects0:
        anyIntersects = False
        for rect1 in rects1:
            if intersects(rect0, rect1):
                anyIntersects = True
                break
        if not anyIntersects:
            result += [rect0]
    return result

def sendEmail(fromAddr, toAddrList, ccAddrList, subject, message,
              login, password, smtpServer='smtp.gmail.com:587'):

    # Taken from http://rosettacode.org/wiki/Send_an_email#Python

    import smtplib

    header = 'From: %s\n' % fromAddr
    header += 'To: %s\n' % ','.join(toAddrList)
    header += 'Cc: %s\n' % ','.join(ccAddrList)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpServer)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(fromAddr, toAddrList, message)
    server.quit()
    return problems

def wxBitmapFromCvImage(image):
    import wx
    image = cv2.cvtColor(image, cv2.cv.CV_BGR2RGB)
    h, w = image.shape[:2]
    bitmap = wx.BitmapFromBuffer(w, h, image)
    return bitmap

def pyInstallerResourcePath(relativePath):
    import os
    import sys
    basePath = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    return os.path.join(basePath, relativePath)