import wx

from InteractiveRecognizer import InteractiveRecognizer
import utils


def main():
    app = wx.App()
    lbphPath = utils.pyInstallerResourcePath(
            'recognizers/lbph_cat_faces.xml')
    classifierPath = utils.pyInstallerResourcePath(
            'cascades/haarcascade_frontalcatface.xml')
    interactiveRecognizer = InteractiveRecognizer(
            lbphPath, classifierPath,
            minNeighbors=8,
            title='Interactive Cat Face Recognizer')
    interactiveRecognizer.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()