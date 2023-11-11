# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'openai_options.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)
import resources_rc

class Ui_Openai_dlg(object):
    def setupUi(self, Openai_dlg):
        if not Openai_dlg.objectName():
            Openai_dlg.setObjectName(u"Openai_dlg")
        Openai_dlg.resize(758, 249)
        Openai_dlg.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.987, y2:0.579545, stop:0.028065 rgba(30, 82, 139, 255), stop:0.731343 rgba(12, 34, 89, 255));\n"
"color: rgb(255, 255, 255);\n"
"\n"
"")
        self.verticalLayout = QVBoxLayout(Openai_dlg)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(Openai_dlg)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tokenEdit = QLineEdit(self.frame_3)
        self.tokenEdit.setObjectName(u"tokenEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tokenEdit.sizePolicy().hasHeightForWidth())
        self.tokenEdit.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.tokenEdit)

        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)


        self.verticalLayout_2.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.openai_engine_cb = QComboBox(self.frame_4)
        self.openai_engine_cb.setObjectName(u"openai_engine_cb")

        self.horizontalLayout_3.addWidget(self.openai_engine_cb)

        self.choose_engine_lbl = QLabel(self.frame_4)
        self.choose_engine_lbl.setObjectName(u"choose_engine_lbl")

        self.horizontalLayout_3.addWidget(self.choose_engine_lbl)


        self.verticalLayout_2.addWidget(self.frame_4)


        self.verticalLayout.addWidget(self.frame)

        self.frame_2 = QFrame(Openai_dlg)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.openai_close_pb = QPushButton(self.frame_2)
        self.openai_close_pb.setObjectName(u"openai_close_pb")
        icon = QIcon()
        icon.addFile(u":/icons/images/close.png", QSize(), QIcon.Normal, QIcon.On)
        self.openai_close_pb.setIcon(icon)

        self.horizontalLayout.addWidget(self.openai_close_pb)


        self.verticalLayout.addWidget(self.frame_2)


        self.retranslateUi(Openai_dlg)

        QMetaObject.connectSlotsByName(Openai_dlg)
    # setupUi

    def retranslateUi(self, Openai_dlg):
        Openai_dlg.setWindowTitle(QCoreApplication.translate("Openai_dlg", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Openai_dlg", u"Openai token", None))
        self.choose_engine_lbl.setText(QCoreApplication.translate("Openai_dlg", u"Choose the openai engine you wish to use", None))
        self.openai_close_pb.setText(QCoreApplication.translate("Openai_dlg", u"Close", None))
    # retranslateUi

