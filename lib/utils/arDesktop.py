#*********************************************************************
# content   = OS startup file
# version   = 0.6.0
# date      = 2018-12-01
#
# license   = MIT
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************

import os
import sys
import webbrowser

from Qt import QtWidgets, QtGui, QtCore

import libLog
import libData
import libFunc
from tank import Tank
from software import Software

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

#**********************
# CLASS
class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, parent)
        # self.activated.connect(self.showMainWidget)
        self.setIcon(QtGui.QIcon(libData.get_img_path('software/default')))

        self.parent = parent

        Tank().init_os()
        self.data = Tank().data
        self.user = Tank().user
        self.project_data = Tank().data['project']

        menu = QtWidgets.QMenu()
        menu.setStyleSheet(self.data['script'][TITLE]['style'])

        # ADMIN UI
        if True: # self.user.is_admin:
            adminMenu = QtWidgets.QMenu('Admin')
            adminMenu.setStyleSheet(self.data['script'][TITLE]['style'])
            menu.addMenu(adminMenu)

            menuItem = adminMenu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnFolder48')), 'Open Project Data')
            menuItem.triggered.connect(self.press_btnOpenProjectLog)
            menuItem = adminMenu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnFolder48')), 'Open User Data')
            menuItem.triggered.connect(self.press_btnOpenLocalLog)

            menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('user/' + self.user.id)), self.user.id)
        menuItem.triggered.connect(self.press_btnShowUserData)

        menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('project/default')), self.data['project']['name'])
        menuItem.triggered.connect(self.press_btnOpenProjectPath)

        menu.addSeparator()

        subMenu = QtWidgets.QMenu('Software')
        subMenu.setStyleSheet(self.data['script'][TITLE]['style'])
        menu.addMenu(subMenu)

        for soft, soft_func in self.data['script'][TITLE]['SOFTWARE'].items():
            menuItem = subMenu.addAction(QtGui.QIcon(libData.get_img_path('software/' + soft)), soft.title())
            menuItem.triggered.connect(eval(soft_func))

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnFolderSearchGet48')), 'Load')
        menuItem.triggered.connect(self.press_btnLoad)

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnReport48')), 'Report')
        menuItem.triggered.connect(self.press_btnReport)

        menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnHelp48')), 'Help')
        menuItem.triggered.connect(self.press_btnHelp)

        menu.addSeparator()

        menuItem = menu.addAction(QtGui.QIcon(libData.get_img_path('btn/btnDenial48')), 'Quit')
        menuItem.triggered.connect(self.press_closeStartup)

        self.setContextMenu(menu)


    #**********************
    # PRESS_TRIGGER
    def press_btnShowUserData(self):
        libFunc.open_folder(self.project_data['PATH']['user'] + '/' + os.getenv('username'))

    def press_btnOpenProjectPath(self):
        libFunc.open_folder(self.project_data['path'])
    #------------------------------
    def press_btnLoad(self):
        import arLoad
        self.arLoad = arLoad.ArLoad()
    #------------------------------
    def press_btnOpenMaya(self):
        Software().start('maya')

    def press_btnOpenNuke(self):
        Software().start('nuke')

    def press_btnOpenHoudini(self):
        Software().start('houdini')

    def press_btnOpenMax(self):
        Software().start('max')
    #------------------------------
    def press_btnOpenProjectLog(self):
        libFunc.open_folder(libData.get_env('DATA_PROJECT_PATH'))

    def press_btnOpenLocalLog(self):
        libFunc.open_folder(libData.get_env('DATA_USER_PATH'))
    #------------------------------
    def press_btnReport(self):
        libFunc.get_help('issues')

    def press_btnHelp(self):
        libFunc.get_help(TITLE)
    #------------------------------
    def press_closeStartup(self):
        self.parent.instance().quit()


def start():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    trayIcon = SystemTrayIcon(app)
    trayIcon.show()
    trayIcon.setToolTip(trayIcon.data['project']['name'] + ' [right click]')
    trayIcon.showMessage(trayIcon.data['project']['name'], '[right click]', QtWidgets.QSystemTrayIcon.Information , 20000)

    app.exec_()
