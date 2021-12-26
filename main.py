import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import QtWebEngineWidgets
from browser import *
from browser_auth import *


class auth(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth = Ui_Form()
        self.auth.setupUi(self)
        self.setWindowModality(2)
        self.auth.lE_enterPassword.setPlaceholderText('Введите пароль: ')
        self.valid_flag = False

        #Убираем рамки
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.auth.btn_enter.clicked.connect(self.check_password)

    def check_password(self):
        possible_password = self.auth.lE_enterPassword.text()

        if len(possible_password) > 0:
            with open('qt designer\\password.txt') as file:
                password = file.read()

            if possible_password == password:
                self.valid_flag = True
                self.close()
            else:
                QtWidgets.QMessageBox.information(self, 'Ошибка доступа', 'Вы ввели неправильный пароль')
                raise SystemExit

class GUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Обработчики кнопок
        self.ui.tBtn_home.clicked.connect(self.home)
        self.ui.tBtn_reload.clicked.connect(self.reload)
        self.ui.tBtn_back.clicked.connect(self.back)
        self.ui.tBtn_search.clicked.connect(self.search)
        self.ui.tBtn_changeTheme.clicked.connect(self.change_themes)
        self.ui.tBtn_openCloseFullWindow.clicked.connect(self.openCloseFullWindow)
        self.ui.tBtn_minimaze.clicked.connect(self.minimizeWindow)
        self.ui.tBtn_closeWindow.clicked.connect(self.closeWindow)

        #Иницилизация WebView
        self.web = QtWebEngineWidgets.QWebEngineView()
        self.ui.gridLayout.addWidget(self.web, 1, 0, 1, 10)

        #Текущая тема
        self.white_theme = True

        #Окно открыто на полную
        self.fullScreen = False

        #Подсказки к кнопкам
        self.ui.tBtn_changeTheme.setToolTip('Изменить тему')
        self.ui.tBtn_back.setToolTip('Назад')
        self.ui.tBtn_home.setToolTip('Домой')
        self.ui.tBtn_reload.setToolTip('Обновить')
        self.ui.tBtn_search.setToolTip('Искать')
        self.ui.tBtn_openCloseFullWindow.setToolTip('Открыть на полный экран')

        #Убираем рамки
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)


    def home(self):
        home_page = QtCore.QUrl('https://google.com')
        self.web.load(home_page)
        self.ui.lE_searchLine.setText('https://google.com')

    def reload(self):
        self.web.reload()

    def back(self):
        self.web.back()

    def search(self):
        textFromSearchLine = self.ui.lE_searchLine.text()
        text = ''
        if len(textFromSearchLine) > 0:
            if not textFromSearchLine.startswith('http'):
                text = f'https://www.google.com/search?q={textFromSearchLine}'
                textFromSearchLine = QtCore.QUrl('https://www.google.com/search?q=' + textFromSearchLine)
            else:
                text = textFromSearchLine
                textFromSearchLine = QtCore.QUrl(textFromSearchLine)

            self.web.load(textFromSearchLine)
            self.ui.lE_searchLine.setText(text)

    def change_themes(self):
        default_style = '''
            QMainWindow {
            }
        '''

        style = '''
            QMainWindow {
                background-color: #3B3B3B;
            }
        '''

        if self.white_theme:
            self.white_theme = False
            self.setStyleSheet(style)
        else:
            self.white_theme = True
            self.setStyleSheet(default_style)

    def openCloseFullWindow(self):
        if not self.fullScreen:
            self.showMaximized()
            self.fullScreen = True
        else:
            self.showNormal()
            self.fullScreen = False

    def minimizeWindow(self):
        self.showNormal()
        self.showMinimized()

    def closeWindow(self):
        if QtWidgets.QMessageBox.warning(self, 'Выход', 'Вы действительно хотите выйти?',
                                          QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            raise SystemExit
        else:
            return


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    browser = GUI()
    browser.show()
    auth = auth()
    auth.show()
    sys.exit(app.exec_())