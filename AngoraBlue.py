import cv2
import os
import socket
import sys

import utils


def recognizeAndReport(recognizer, grayImage, rects, maxDistance,
                       noun='human'):
    for x, y, w, h in rects:
        crop = cv2.equalizeHist(grayImage[y:y+h, x:x+w])
        labelAsInt, distance = recognizer.predict(crop)
        labelAsStr = utils.intToFourChars(labelAsInt)
        #print noun, labelAsStr, distance
        if distance <= maxDistance:
            fromAddr = 'username@gmail.com' # TODO: Replace
            toAddrList = ['username@gmail.com'] # TODO: Replace
            ccAddrList = []
            subject = 'Angora Blue'
            message = 'We have sighted the %s known as %s.' % \
                    (noun, labelAsStr)
            login = 'username' # TODO: Replace
            password = 'password' # TODO: Replace
            # TODO: Replace if not using Gmail.
            smtpServer='smtp.gmail.com:587'
            try:
                problems = utils.sendEmail(
                        fromAddr, toAddrList, ccAddrList, subject,
                        message, login, password, smtpServer)
                if problems:
                    print >> sys.stderr, 'Email problems:', problems
                else:
                    return True
            except socket.gaierror:
                print >> sys.stderr, 'Unable to reach email server'
    return False

def main():

    humanClassifierPath = utils.pyInstallerResourcePath(
            'cascades/haarcascade_frontalface_alt.xml')
    humanLBPHPath = utils.pyInstallerResourcePath(
            'recognizers/lbph_human_faces.xml')
    if not os.path.isfile(humanLBPHPath):
        print >> sys.stderr, \
                'Human face recognizer not trained. Exiting.'
        return

    catClassifierPath = utils.pyInstallerResourcePath(
            'cascades/haarcascade_frontalcatface.xml')
    catLBPHPath = utils.pyInstallerResourcePath(
            'recognizers/lbph_cat_faces.xml')
    if not os.path.isfile(catLBPHPath):
        print >> sys.stderr, \
                'Cat face recognizer not trained. Exiting.'
        return

    capture = cv2.VideoCapture(0)
    imageWidth = capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    imageHeight = capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    minImageSize = min(imageWidth, imageHeight)

    humanDetector = cv2.CascadeClassifier(humanClassifierPath)
    humanRecognizer = cv2.createLBPHFaceRecognizer()
    humanRecognizer.load(humanLBPHPath)
    humanMinSize = (int(minImageSize * 0.25),
                    int(minImageSize * 0.25))
    humanMaxDistance = 25

    catDetector = cv2.CascadeClassifier(catClassifierPath)
    catRecognizer = cv2.createLBPHFaceRecognizer()
    catRecognizer.load(catLBPHPath)
    catMinSize = humanMinSize
    catMaxDistance = 25

    while True:
        success, image = capture.read()
        if image is not None:
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            equalizedGrayImage = cv2.equalizeHist(grayImage)

            humanRects = humanDetector.detectMultiScale(
                    equalizedGrayImage, scaleFactor=1.3,
                    minNeighbors=4, minSize=humanMinSize,
                    flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
            if recognizeAndReport(
                    humanRecognizer, grayImage, humanRects,
                    humanMaxDistance, 'human'):
                break

            catRects = catDetector.detectMultiScale(
                    equalizedGrayImage, scaleFactor=1.3,
                    minNeighbors=8, minSize=catMinSize,
                    flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
            # Reject any cat faces that overlap with human faces.
            catRects = utils.difference(catRects, humanRects)
            if recognizeAndReport(
                    catRecognizer, grayImage, catRects,
                    catMaxDistance, 'cat'):
                break

if __name__ == '__main__':
    main()
