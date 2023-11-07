# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'process_image.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1294, 1009)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setStyleSheet(u"\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(8, 24, 62, 255), stop:1 rgba(21, 57, 96, 255));\n"
"color: rgb(246, 245, 244);")
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 50))
        self.frame.setStyleSheet(u"\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(8, 24, 62, 255), stop:1 rgba(21, 57, 96, 255));\n"
"color: rgb(246, 245, 244);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.process_directory_pb = QPushButton(self.frame_4)
        self.process_directory_pb.setObjectName(u"process_directory_pb")

        self.horizontalLayout_2.addWidget(self.process_directory_pb)

        self.process_directory_le = QLineEdit(self.frame_4)
        self.process_directory_le.setObjectName(u"process_directory_le")
        self.process_directory_le.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(36, 31, 49);")

        self.horizontalLayout_2.addWidget(self.process_directory_le)


        self.horizontalLayout.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.process_image_pb = QPushButton(self.frame_5)
        self.process_image_pb.setObjectName(u"process_image_pb")

        self.horizontalLayout_3.addWidget(self.process_image_pb)

        self.process_image_le = QLineEdit(self.frame_5)
        self.process_image_le.setObjectName(u"process_image_le")
        self.process_image_le.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(36, 31, 49);")

        self.horizontalLayout_3.addWidget(self.process_image_le)


        self.horizontalLayout.addWidget(self.frame_5)


        self.verticalLayout.addWidget(self.frame)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_2 = QFrame(self.frame_3)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.image_widget = QWidget(self.frame_2)
        self.image_widget.setObjectName(u"image_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.image_widget.sizePolicy().hasHeightForWidth())
        self.image_widget.setSizePolicy(sizePolicy1)
        self.image_widget.setStyleSheet(u"\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(8, 24, 62, 255), stop:1 rgba(21, 57, 96, 255));\n"
"color: rgb(246, 245, 244);")
        self.horizontalLayout_5 = QHBoxLayout(self.image_widget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.image_label = QLabel(self.image_widget)
        self.image_label.setObjectName(u"image_label")

        self.horizontalLayout_5.addWidget(self.image_label)


        self.verticalLayout_3.addWidget(self.image_widget)

        self.form_edit_widget = QWidget(self.frame_2)
        self.form_edit_widget.setObjectName(u"form_edit_widget")
        sizePolicy1.setHeightForWidth(self.form_edit_widget.sizePolicy().hasHeightForWidth())
        self.form_edit_widget.setSizePolicy(sizePolicy1)
        self.form_edit_widget.setStyleSheet(u"\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(8, 24, 62, 255), stop:1 rgba(21, 57, 96, 255));\n"
"color: rgb(246, 245, 244);")
        self.horizontalLayout_4 = QHBoxLayout(self.form_edit_widget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.widget_2 = QWidget(self.form_edit_widget)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_5 = QVBoxLayout(self.widget_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame_6 = QFrame(self.widget_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMaximumSize(QSize(16777215, 100))
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label = QLabel(self.frame_6)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout_6.addWidget(self.label)

        self.question_edit = QLineEdit(self.frame_6)
        self.question_edit.setObjectName(u"question_edit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.question_edit.sizePolicy().hasHeightForWidth())
        self.question_edit.setSizePolicy(sizePolicy2)
        self.question_edit.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(36, 31, 49);")

        self.verticalLayout_6.addWidget(self.question_edit)


        self.verticalLayout_5.addWidget(self.frame_6)

        self.answer_frame = QFrame(self.widget_2)
        self.answer_frame.setObjectName(u"answer_frame")
        self.answer_frame.setFrameShape(QFrame.StyledPanel)
        self.answer_frame.setFrameShadow(QFrame.Raised)

        self.verticalLayout_5.addWidget(self.answer_frame)


        self.horizontalLayout_4.addWidget(self.widget_2)

        self.widget = QWidget(self.form_edit_widget)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(175, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.add_answer_pb = QPushButton(self.widget)
        self.add_answer_pb.setObjectName(u"add_answer_pb")
        self.add_answer_pb.setStyleSheet(u"")

        self.verticalLayout_4.addWidget(self.add_answer_pb)

        self.delete_answer_pb = QPushButton(self.widget)
        self.delete_answer_pb.setObjectName(u"delete_answer_pb")
        self.delete_answer_pb.setStyleSheet(u"")

        self.verticalLayout_4.addWidget(self.delete_answer_pb)

        self.verticalSpacer = QSpacerItem(20, 276, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.next_btn = QPushButton(self.widget)
        self.next_btn.setObjectName(u"next_btn")

        self.verticalLayout_4.addWidget(self.next_btn)

        self.save_btn = QPushButton(self.widget)
        self.save_btn.setObjectName(u"save_btn")

        self.verticalLayout_4.addWidget(self.save_btn)


        self.horizontalLayout_4.addWidget(self.widget)


        self.verticalLayout_3.addWidget(self.form_edit_widget)


        self.verticalLayout_2.addWidget(self.frame_2)


        self.verticalLayout.addWidget(self.frame_3)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.process_directory_pb.setText(QCoreApplication.translate("Dialog", u"Process Directory", None))
        self.process_image_pb.setText(QCoreApplication.translate("Dialog", u"Process Image", None))
        self.image_label.setText("")
        self.label.setText(QCoreApplication.translate("Dialog", u"Question", None))
        self.add_answer_pb.setText(QCoreApplication.translate("Dialog", u"Add Answer", None))
        self.delete_answer_pb.setText(QCoreApplication.translate("Dialog", u"Delete Answer", None))
        self.next_btn.setText(QCoreApplication.translate("Dialog", u"Next", None))
        self.save_btn.setText(QCoreApplication.translate("Dialog", u"Save Question", None))
    # retranslateUi

