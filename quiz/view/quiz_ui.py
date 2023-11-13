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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QListView, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTextEdit, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1188, 644)
        icon = QIcon()
        icon.addFile(u"../../../../../../home/mike/images/ZSLogo1.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.987, y2:0.579545, stop:0.028065 rgba(30, 82, 139, 255), stop:0.731343 rgba(12, 34, 89, 255));\n"
"color: rgb(255, 255, 255);\n"
"\n"
"")
        self.actionStart_Quiz = QAction(MainWindow)
        self.actionStart_Quiz.setObjectName(u"actionStart_Quiz")
        self.actionUser_Login = QAction(MainWindow)
        self.actionUser_Login.setObjectName(u"actionUser_Login")
        self.actionSet_Item_Correct = QAction(MainWindow)
        self.actionSet_Item_Correct.setObjectName(u"actionSet_Item_Correct")
        self.actionRegenerate = QAction(MainWindow)
        self.actionRegenerate.setObjectName(u"actionRegenerate")
        self.actionFind_Duplicates = QAction(MainWindow)
        self.actionFind_Duplicates.setObjectName(u"actionFind_Duplicates")
        self.actionCreate_Q = QAction(MainWindow)
        self.actionCreate_Q.setObjectName(u"actionCreate_Q")
        self.actionDelete_Question = QAction(MainWindow)
        self.actionDelete_Question.setObjectName(u"actionDelete_Question")
        self.actionLoad_csv = QAction(MainWindow)
        self.actionLoad_csv.setObjectName(u"actionLoad_csv")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionOpenai_opt = QAction(MainWindow)
        self.actionOpenai_opt.setObjectName(u"actionOpenai_opt")
        self.actionSearch_for_question = QAction(MainWindow)
        self.actionSearch_for_question.setObjectName(u"actionSearch_for_question")
        self.actionTest_Manager = QAction(MainWindow)
        self.actionTest_Manager.setObjectName(u"actionTest_Manager")
        self.actionEdit_this_question = QAction(MainWindow)
        self.actionEdit_this_question.setObjectName(u"actionEdit_this_question")
        self.actionTake_Test = QAction(MainWindow)
        self.actionTake_Test.setObjectName(u"actionTake_Test")
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
        self.question_label.setWordWrap(True)
        self.question_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

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
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
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

        self.answers_list_widget = QListView(self.answers_frame)
        self.answers_list_widget.setObjectName(u"answers_list_widget")
        self.answers_list_widget.setFrameShape(QFrame.StyledPanel)
        self.answers_list_widget.setWordWrap(True)

        self.answers_verticalLayout.addWidget(self.answers_list_widget)


        self.verticalLayout_2.addWidget(self.answers_frame)

        self.submit_btn = QPushButton(self.answer_frame)
        self.submit_btn.setObjectName(u"submit_btn")
        self.submit_btn.setStyleSheet(u"\n"
"color: rgb(255, 255, 255);")
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/test.png", QSize(), QIcon.Normal, QIcon.On)
        self.submit_btn.setIcon(icon1)

        self.verticalLayout_2.addWidget(self.submit_btn)

        self.button_frame = QFrame(self.answer_frame)
        self.button_frame.setObjectName(u"button_frame")
        self.button_frame.setFrameShape(QFrame.StyledPanel)
        self.button_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.button_frame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.previous_btn = QPushButton(self.button_frame)
        self.previous_btn.setObjectName(u"previous_btn")
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/previous1.png", QSize(), QIcon.Normal, QIcon.On)
        self.previous_btn.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.previous_btn)

        self.next_btn = QPushButton(self.button_frame)
        self.next_btn.setObjectName(u"next_btn")
        self.next_btn.setLayoutDirection(Qt.RightToLeft)
        self.next_btn.setStyleSheet(u"\n"
"color: rgb(255, 255, 255);")
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/next.png", QSize(), QIcon.Normal, QIcon.On)
        self.next_btn.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.next_btn)


        self.verticalLayout_2.addWidget(self.button_frame)


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
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/AI.png", QSize(), QIcon.Normal, QIcon.On)
        self.explanation_btn.setIcon(icon4)

        self.verticalLayout_3.addWidget(self.explanation_btn)

        self.explanation_edit = QTextEdit(self.explanation_frame)
        self.explanation_edit.setObjectName(u"explanation_edit")
        self.explanation_edit.setMouseTracking(False)
        self.explanation_edit.setAcceptDrops(False)
        self.explanation_edit.setTabChangesFocus(False)
        self.explanation_edit.setUndoRedoEnabled(False)
        self.explanation_edit.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.verticalLayout_3.addWidget(self.explanation_edit)

        self.show_answers_frame = QFrame(self.explanation_frame)
        self.show_answers_frame.setObjectName(u"show_answers_frame")
        self.show_answers_frame.setFrameShape(QFrame.StyledPanel)
        self.show_answers_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.show_answers_frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.show_answers_cb = QCheckBox(self.show_answers_frame)
        self.show_answers_cb.setObjectName(u"show_answers_cb")

        self.horizontalLayout_3.addWidget(self.show_answers_cb)

        self.show_answer_btn = QPushButton(self.show_answers_frame)
        self.show_answer_btn.setObjectName(u"show_answer_btn")
        icon5 = QIcon()
        icon5.addFile(u":/icons/images/correct.png", QSize(), QIcon.Normal, QIcon.On)
        self.show_answer_btn.setIcon(icon5)

        self.horizontalLayout_3.addWidget(self.show_answer_btn)


        self.verticalLayout_3.addWidget(self.show_answers_frame)

        self.show_answers_le = QLabel(self.explanation_frame)
        self.show_answers_le.setObjectName(u"show_answers_le")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.show_answers_le.sizePolicy().hasHeightForWidth())
        self.show_answers_le.setSizePolicy(sizePolicy4)

        self.verticalLayout_3.addWidget(self.show_answers_le)


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
        icon6 = QIcon()
        icon6.addFile(u":/icons/images/save.png", QSize(), QIcon.Normal, QIcon.On)
        self.save_notes_btn.setIcon(icon6)

        self.verticalLayout_5.addWidget(self.save_notes_btn)


        self.verticalLayout_6.addWidget(self.notes_frame)


        self.horizontalLayout.addWidget(self.frame_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1188, 22))
        self.filemenu = QMenu(self.menubar)
        self.filemenu.setObjectName(u"filemenu")
        self.filemenu.setStyleSheet(u"")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.filemenu.menuAction())
        self.filemenu.addSeparator()
        self.filemenu.addAction(self.actionUser_Login)
        self.filemenu.addAction(self.actionSearch_for_question)
        self.filemenu.addAction(self.actionStart_Quiz)
        self.filemenu.addAction(self.actionTake_Test)
        self.filemenu.addAction(self.actionTest_Manager)
        self.filemenu.addSeparator()
        self.filemenu.addAction(self.actionSet_Item_Correct)
        self.filemenu.addAction(self.actionRegenerate)
        self.filemenu.addAction(self.actionFind_Duplicates)
        self.filemenu.addAction(self.actionCreate_Q)
        self.filemenu.addAction(self.actionEdit_this_question)
        self.filemenu.addAction(self.actionDelete_Question)
        self.filemenu.addAction(self.actionLoad_csv)
        self.filemenu.addSeparator()
        self.filemenu.addAction(self.actionOpenai_opt)
        self.filemenu.addAction(self.actionQuit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionStart_Quiz.setText(QCoreApplication.translate("MainWindow", u"Start Quiz", None))
        self.actionUser_Login.setText(QCoreApplication.translate("MainWindow", u"User Login", None))
        self.actionSet_Item_Correct.setText(QCoreApplication.translate("MainWindow", u"Set Answer Correct", None))
#if QT_CONFIG(shortcut)
        self.actionSet_Item_Correct.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+K", None))
#endif // QT_CONFIG(shortcut)
        self.actionRegenerate.setText(QCoreApplication.translate("MainWindow", u"Regenerate gpt response", None))
#if QT_CONFIG(shortcut)
        self.actionRegenerate.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.actionFind_Duplicates.setText(QCoreApplication.translate("MainWindow", u"Find Duplicates", None))
#if QT_CONFIG(shortcut)
        self.actionFind_Duplicates.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+D", None))
#endif // QT_CONFIG(shortcut)
        self.actionCreate_Q.setText(QCoreApplication.translate("MainWindow", u"Create New Question", None))
        self.actionDelete_Question.setText(QCoreApplication.translate("MainWindow", u"Delete Current Question", None))
#if QT_CONFIG(shortcut)
        self.actionDelete_Question.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+D, Ctrl+D", None))
#endif // QT_CONFIG(shortcut)
        self.actionLoad_csv.setText(QCoreApplication.translate("MainWindow", u"Load Questions From csv", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
#if QT_CONFIG(shortcut)
        self.actionQuit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpenai_opt.setText(QCoreApplication.translate("MainWindow", u"Openai Options", None))
        self.actionSearch_for_question.setText(QCoreApplication.translate("MainWindow", u"Search for question", None))
#if QT_CONFIG(shortcut)
        self.actionSearch_for_question.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
        self.actionTest_Manager.setText(QCoreApplication.translate("MainWindow", u"Test Manager", None))
        self.actionEdit_this_question.setText(QCoreApplication.translate("MainWindow", u"Edit this question", None))
        self.actionTake_Test.setText(QCoreApplication.translate("MainWindow", u"Take Test", None))
        self.question_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:22pt; font-weight:700; color:#deddda;\">Question:</span></p><p><span style=\" color:#ffffff;\">This is not a question?</span></p></body></html>", None))
        self.answers_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:22pt; color:#deddda;\">Answers:</span></p></body></html>", None))
        self.submit_btn.setText(QCoreApplication.translate("MainWindow", u"Submit", None))
#if QT_CONFIG(shortcut)
        self.submit_btn.setShortcut(QCoreApplication.translate("MainWindow", u"Return", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.previous_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Use the left arrow <-", None))
#endif // QT_CONFIG(tooltip)
        self.previous_btn.setText(QCoreApplication.translate("MainWindow", u"Previous Question", None))
#if QT_CONFIG(shortcut)
        self.previous_btn.setShortcut(QCoreApplication.translate("MainWindow", u"Left", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.next_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Use the right arrow ->", None))
#endif // QT_CONFIG(tooltip)
        self.next_btn.setText(QCoreApplication.translate("MainWindow", u"Next Question", None))
#if QT_CONFIG(shortcut)
        self.next_btn.setShortcut(QCoreApplication.translate("MainWindow", u"Right", None))
#endif // QT_CONFIG(shortcut)
        self.explanation_btn.setText(QCoreApplication.translate("MainWindow", u"Show Explanation", None))
#if QT_CONFIG(shortcut)
        self.explanation_btn.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+E", None))
#endif // QT_CONFIG(shortcut)
        self.show_answers_cb.setText(QCoreApplication.translate("MainWindow", u"Show Correct Answers", None))
#if QT_CONFIG(tooltip)
        self.show_answer_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Use the menu command to set a correct answer", None))
#endif // QT_CONFIG(tooltip)
        self.show_answer_btn.setText(QCoreApplication.translate("MainWindow", u"Show This Correct Answer", None))
        self.show_answers_le.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Take notes", None))
#if QT_CONFIG(tooltip)
        self.save_notes_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Save current note to the database", None))
#endif // QT_CONFIG(tooltip)
        self.save_notes_btn.setText(QCoreApplication.translate("MainWindow", u"Save Notes", None))
#if QT_CONFIG(shortcut)
        self.save_notes_btn.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.filemenu.setTitle(QCoreApplication.translate("MainWindow", u"file", None))
    # retranslateUi

