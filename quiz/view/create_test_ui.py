# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'create_test.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QHeaderView, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(754, 518)
        Dialog.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.987, y2:0.579545, stop:0.028065 rgba(30, 82, 139, 255), stop:0.731343 rgba(12, 34, 89, 255));\n"
"color: rgb(255, 255, 255);\n"
"\n"
"")
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.create_test_pb = QPushButton(self.frame)
        self.create_test_pb.setObjectName(u"create_test_pb")

        self.horizontalLayout.addWidget(self.create_test_pb)

        self.delete_test_pb = QPushButton(self.frame)
        self.delete_test_pb.setObjectName(u"delete_test_pb")

        self.horizontalLayout.addWidget(self.delete_test_pb)


        self.verticalLayout_2.addWidget(self.frame)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.test_tbl = QTableWidget(self.frame_2)
        self.test_tbl.setObjectName(u"test_tbl")

        self.verticalLayout.addWidget(self.test_tbl)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.close_pb = QPushButton(Dialog)
        self.close_pb.setObjectName(u"close_pb")
        icon = QIcon()
        icon.addFile(u":/icons/images/close.png", QSize(), QIcon.Normal, QIcon.On)
        self.close_pb.setIcon(icon)

        self.verticalLayout_2.addWidget(self.close_pb)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.create_test_pb.setText(QCoreApplication.translate("Dialog", u"Create Test", None))
        self.delete_test_pb.setText(QCoreApplication.translate("Dialog", u"Delete Test", None))
        self.close_pb.setText(QCoreApplication.translate("Dialog", u"CLose", None))
    # retranslateUi

