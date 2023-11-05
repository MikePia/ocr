# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'quiz.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTextEdit, QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1188, 644)
        icon = QIcon()
        icon.addFile(u"../../images/ZSLogo1.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.987, y2:0.579545, stop:0.028065 rgba(30, 82, 139, 255), stop:0.731343 rgba(12, 34, 89, 255));\n"
"color: rgb(255, 255, 255);\n"
"\n"
"")
        self.actionStart_Quiz = QAction(MainWindow)
        self.actionStart_Quiz.setObjectName(u"actionStart_Quiz")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.quiz_frame = QFrame(self.centralwidget)
        self.quiz_frame.setObjectName(u"quiz_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quiz_frame.sizePolicy().hasHeightForWidth())
        self.quiz_frame.setSizePolicy(sizePolicy)
        self.quiz_frame.setFrameShape(QFrame.StyledPanel)
        self.quiz_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.quiz_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.question_frame = QFrame(self.quiz_frame)
        self.question_frame.setObjectName(u"question_frame")
        self.question_frame.setMinimumSize(QSize(0, 75))
        self.question_frame.setMaximumSize(QSize(16777215, 300))
        self.question_frame.setFrameShape(QFrame.StyledPanel)
        self.question_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.question_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.question_label = QLabel(self.question_frame)
        self.question_label.setObjectName(u"question_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(2)
        sizePolicy1.setHeightForWidth(self.question_label.sizePolicy().hasHeightForWidth())
        self.question_label.setSizePolicy(sizePolicy1)

        self.verticalLayout_4.addWidget(self.question_label)


        self.verticalLayout.addWidget(self.question_frame)

        self.answer_frame = QFrame(self.quiz_frame)
        self.answer_frame.setObjectName(u"answer_frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.answer_frame.sizePolicy().hasHeightForWidth())
        self.answer_frame.setSizePolicy(sizePolicy2)
        self.answer_frame.setFrameShape(QFrame.NoFrame)
        self.answer_frame.setLineWidth(2)
        self.verticalLayout_2 = QVBoxLayout(self.answer_frame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.answers_frame = QFrame(self.answer_frame)
        self.answers_frame.setObjectName(u"answers_frame")
        self.answers_frame.setFrameShape(QFrame.NoFrame)
        self.answers_frame.setFrameShadow(QFrame.Plain)
        self.answers_frame.setLineWidth(0)
        self.answers_verticalLayout = QVBoxLayout(self.answers_frame)
        self.answers_verticalLayout.setSpacing(0)
        self.answers_verticalLayout.setObjectName(u"answers_verticalLayout")
        self.answers_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.answers_label = QLabel(self.answers_frame)
        self.answers_label.setObjectName(u"answers_label")

        self.answers_verticalLayout.addWidget(self.answers_label)

        self.answers_list_widget = QListWidget(self.answers_frame)
        self.answers_list_widget.setObjectName(u"answers_list_widget")
        self.answers_list_widget.setFrameShape(QFrame.StyledPanel)

        self.answers_verticalLayout.addWidget(self.answers_list_widget)


        self.verticalLayout_2.addWidget(self.answers_frame)

        self.pushButton_3 = QPushButton(self.answer_frame)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u"\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_2.addWidget(self.pushButton_3)

        self.next_btn = QPushButton(self.answer_frame)
        self.next_btn.setObjectName(u"next_btn")
        self.next_btn.setStyleSheet(u"\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_2.addWidget(self.next_btn)


        self.verticalLayout.addWidget(self.answer_frame)


        self.horizontalLayout.addWidget(self.quiz_frame)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy3)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.explanation_frame = QFrame(self.frame_2)
        self.explanation_frame.setObjectName(u"explanation_frame")
        self.explanation_frame.setFrameShape(QFrame.StyledPanel)
        self.explanation_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.explanation_frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.explanation_btn = QPushButton(self.explanation_frame)
        self.explanation_btn.setObjectName(u"explanation_btn")
        self.explanation_btn.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.verticalLayout_3.addWidget(self.explanation_btn)

        self.explanation_edit = QTextEdit(self.explanation_frame)
        self.explanation_edit.setObjectName(u"explanation_edit")

        self.verticalLayout_3.addWidget(self.explanation_edit)


        self.verticalLayout_6.addWidget(self.explanation_frame)

        self.notes_frame = QFrame(self.frame_2)
        self.notes_frame.setObjectName(u"notes_frame")
        self.notes_frame.setFrameShape(QFrame.StyledPanel)
        self.notes_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.notes_frame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label = QLabel(self.notes_frame)
        self.label.setObjectName(u"label")

        self.verticalLayout_5.addWidget(self.label)

        self.notes_edit = QTextEdit(self.notes_frame)
        self.notes_edit.setObjectName(u"notes_edit")

        self.verticalLayout_5.addWidget(self.notes_edit)

        self.save_notes_btn = QPushButton(self.notes_frame)
        self.save_notes_btn.setObjectName(u"save_notes_btn")

        self.verticalLayout_5.addWidget(self.save_notes_btn)


        self.verticalLayout_6.addWidget(self.notes_frame)


        self.horizontalLayout.addWidget(self.frame_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1188, 22))
        self.filemenu = QMenu(self.menubar)
        self.filemenu.setObjectName(u"filemenu")
        self.filemenu.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(153, 193, 241);")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.filemenu.menuAction())
        self.filemenu.addSeparator()
        self.filemenu.addAction(self.actionStart_Quiz)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionStart_Quiz.setText(QCoreApplication.translate("MainWindow", u"Start Quiz", None))
        self.question_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:22pt; font-weight:700; color:#deddda;\">Question:</span></p><p class=\"question\"><span style=\" color:#ffffff;\">This is a question about python and you should anser it.</span></p></body></html>", None))
        self.answers_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:22pt; color:#deddda;\">Answers:</span></p></body></html>", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Submit", None))
        self.next_btn.setText(QCoreApplication.translate("MainWindow", u"Next Question", None))
        self.explanation_btn.setText(QCoreApplication.translate("MainWindow", u"Show Explanation", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Take notes", None))
        self.save_notes_btn.setText(QCoreApplication.translate("MainWindow", u"Save Notes", None))
        self.filemenu.setTitle(QCoreApplication.translate("MainWindow", u"file", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

