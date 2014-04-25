import wx

from InteractiveRecognizer import InteractiveRecognizer
import utils


def main():
    app = wx.App()
    lbphPath = utils.pyInstallerResourcePath(
            'recognizers/lbph_human_faces.xml')
    classifierPath = utils.pyInstallerResourcePath(
            'cascades/haarcascade_frontalface_alt.xml')
    interactiveRecognizer = InteractiveRecognizer(
            lbphPath, classifierPath,
            title='Interactive Human Face Recognizer')
    interactiveRecognizer.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()