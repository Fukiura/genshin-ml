from PyQt6.QtCore import (
    Qt, QEvent, QPropertyAnimation,
    QRect, QSize
)
from PyQt6.QtGui import (
    QEnterEvent, QFocusEvent, QMouseEvent, QContextMenuEvent,
    QFontDatabase
)
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsOpacityEffect,
    QLabel, QPushButton, QWidget, QLineEdit, QTextEdit,
    QStyle, QVBoxLayout, QHBoxLayout, QGridLayout
)

programTitle: str = "Focarina-ML"
programSize: QSize = QSize(300, 300)

controlPanelSize: QSize = QSize(277, 220)
controlInputSize: QSize = QSize(254, 33)

statusPanelSize: QSize = QSize(77, 64)
statusBoxSize: QSize = QSize(16, 16)

debugConsoleSize: QSize = QSize(257, 24)

class UI:
    def __init__(self):
        self.__app = QApplication([])

        with open("styles/main.qcss") as style:
            self.__app.setStyleSheet(style.read())

        QFontDatabase.addApplicationFont("assets/fonts/zhcn.ttf")

        self.__frame = QCustomMainWindow()
        self.__frame.show()

        self.inputOne: CustomLineEdit = self.__frame.input_LineEditOne
        self.inputTwo: CustomLineEdit = self.__frame.input_LineEditTwo
        self.consoleLog: QLabel = self.__frame.debugConsole_text
        self.launchButton: QSvgPlayButton = self.__frame.play_button
        self.genshinStatus: QWidget = self.__frame.status_conditionOne_box
        self.fpsurStatus: QWidget = self.__frame.status_conditionTwo_box
        self.mgtStatus: QWidget = self.__frame.status_conditionThree_box

    def exec(self) -> None:
        self.__app.exec()

    def toggleStatus(self, whichStatus: QLabel, value: bool) -> None:
        if whichStatus.objectName() != "statusBox":
            raise Exception(f"{whichStatus} is not defined as statusBox")

        if value:
            whichStatus.setStyleSheet("background-color: lime;")
        else:
            whichStatus.setStyleSheet(None)

    def modifyText(self, whichQWidget: QLabel | CustomLineEdit, value: str) -> None:
        whichQWidget.setText(value)

    def getText(self, whichQWidget: QLabel | CustomLineEdit, value: str) -> str:
        return whichQWidget.text()

class QSvgPlayButton(QSvgWidget):
    def __init__(self):
        super().__init__("assets/play_button.svg")
        self.renderer().setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        match a0.button():
            case Qt.MouseButton.LeftButton:
                print("banana")

class CustomInputWidget(QWidget):
    def __init__(self, size: QSize):
        super().__init__()
        self.setFixedSize(size)
        self.setObjectName("InputDirectory")
        
        self.lineEdit: QLineEdit = QLineEdit(self)
        self.lineEdit.setFixedSize(self.size())

class CustomLineEdit(QLineEdit):
    def __init__(self, size: QSize, text: str = "", parent: QWidget | None = None):
        super().__init__(parent)
        self.setFocus()
        self.setFixedSize(size)
        self.setObjectName("InputDirectory")
        self.setTextMargins(5, 0, 0, 0)

        self.label: QLabel = QLabel(text)

        self.containerLayout = QVBoxLayout(self)
        self.containerLayout.setContentsMargins(5, 0, 0, 0)
        self.containerLayout.addWidget(self.label)

        self.opacityFx = QGraphicsOpacityEffect(self.label)
        self.opacityFx.setOpacity(1.0)
        self.label.setGraphicsEffect(self.opacityFx)
        self.fadeAnim = QPropertyAnimation(self.opacityFx, b'opacity')

    def focusInEvent(self, a0: QFocusEvent | None) -> None:
        self.fadeAnim.setEndValue(0.0)
        self.fadeAnim.start()

        super().focusInEvent(a0)
        

    def focusOutEvent(self, a0: QFocusEvent | None) -> None:
        self.fadeAnim.setEndValue(1.0)
        self.fadeAnim.start()

        super().focusOutEvent(a0)
    
    def enterEvent(self, event: QEnterEvent | None) -> None:
        if not self.hasFocus():
            self.fadeAnim.setEndValue(0.0)
            self.fadeAnim.start()

    def leaveEvent(self, event: QEvent | None) -> None:
        if not self.hasFocus():
            self.fadeAnim.setEndValue(1.0)
            self.fadeAnim.start()

class QCustomMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(programTitle)
        self.setFixedSize(programSize)
        #self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.top_container: QWidget = QWidget()
        self.top_containerLayout: QVBoxLayout = QVBoxLayout(self.top_container)
        self.top_containerLayout.setContentsMargins(0, 0, 0, 0)
        self.top_containerLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_frame: QWidget = QWidget()
        self.main_frame.setFixedSize(controlPanelSize)
        self.main_frameLayout: QVBoxLayout = QVBoxLayout(self.main_frame)
        self.main_frameLayout.setContentsMargins(0, 0, 0, 0)
        self.main_frameLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.top_containerLayout.addWidget(self.main_frame)

        self.input_LineEditOne: CustomLineEdit = CustomLineEdit(controlInputSize, "3D Migoto")
        self.input_LineEditTwo: CustomLineEdit = CustomLineEdit(controlInputSize, "FPS Unlocker")

        self.middleContainer: QWidget = QWidget()
        self.middleContainerLayout: QHBoxLayout = QHBoxLayout(self.middleContainer)
        self.middleContainerLayout.setContentsMargins(0, 0, 0, 0)

        self.play_button: QSvgPlayButton = QSvgPlayButton()

        self.status_container: QWidget = QWidget()
        self.status_container.setObjectName("statusContainer")
        self.status_container.setFixedSize(statusPanelSize)
        self.status_containerLayout: QGridLayout = QGridLayout(self.status_container)
        self.status_containerLayout.setHorizontalSpacing(5)
        self.status_containerLayout.setContentsMargins(0, 0, 0, 0)
        self.status_containerLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_conditionOne_box: QWidget = QWidget()
        self.status_conditionOne_box.setObjectName("statusBox")
        self.status_conditionOne_box.setFixedSize(statusBoxSize)
        self.status_conditionOne_label: QLabel = QLabel("Genshin")

        self.status_conditionTwo_box: QWidget = QWidget()
        self.status_conditionTwo_box.setObjectName("statusBox")
        self.status_conditionTwo_box.setFixedSize(statusBoxSize)
        self.status_conditionTwo_label: QLabel = QLabel("FPS UR")
        
        self.status_conditionThree_box: QWidget = QWidget()
        self.status_conditionThree_box.setObjectName("statusBox")
        self.status_conditionThree_box.setFixedSize(statusBoxSize)
        self.status_conditionThree_label: QLabel = QLabel("Migoto")

        self.status_containerLayout.addWidget(self.status_conditionOne_box, 0, 0)
        self.status_containerLayout.addWidget(self.status_conditionOne_label, 0, 1)
        self.status_containerLayout.addWidget(self.status_conditionTwo_box, 1, 0)
        self.status_containerLayout.addWidget(self.status_conditionTwo_label, 1, 1)
        self.status_containerLayout.addWidget(self.status_conditionThree_box, 2, 0)
        self.status_containerLayout.addWidget(self.status_conditionThree_label, 2, 1)

        self.middleContainerLayout.addWidget(self.play_button)
        self.middleContainerLayout.addWidget(self.status_container)

        self.debugConsole_container: QWidget = QWidget()
        self.debugConsole_containerLayout: QVBoxLayout = QVBoxLayout(self.debugConsole_container)
        self.debugConsole_containerLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.debugConsole_containerLayout.setContentsMargins(0, 15, 0, 0)
        self.debugConsole_containerLayout.setSpacing(0)

        self.debugConsole_logLabel: QLabel = QLabel("debug console")
        self.debugConsole_logLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.debugConsole_log: QWidget = QWidget()
        self.debugConsole_log.setObjectName("debugLog")
        self.debugConsole_log.setFixedSize(debugConsoleSize)
        self.debugConsole_text: QLabel = QLabel("output newline one\noutput newline two", self.debugConsole_log)
        
        self.debugConsole_containerLayout.addWidget(self.debugConsole_logLabel)
        self.debugConsole_containerLayout.addWidget(self.debugConsole_log)

        self.main_frameLayout.addWidget(self.input_LineEditOne)
        self.main_frameLayout.addWidget(self.input_LineEditTwo)
        self.main_frameLayout.addWidget(self.middleContainer)
        self.main_frameLayout.addWidget(self.debugConsole_container)

        self.setCentralWidget(self.top_container)
