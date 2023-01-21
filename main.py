# телефонный справочник
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QDialog, QTableView, QHeaderView, QGridLayout,
                             QLineEdit, QMessageBox, QLabel, QFileDialog)
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import Qt

import sqlite3, os, csv

class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        self.setMinimumHeight(300)
        self.setFixedWidth(500)
        self.setWindowTitle("Телефонный справочник")

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('config/call_number.db')
        self.db.open()

        self.table = self.table()
        self.table.setModel(self.model_table())
        self.table.hideColumn(0)

        b_add = QPushButton("Добавить")
        b_add.setStyleSheet("""QPushButton:!hover {background-color: rgba(0, 0, 0, 5);
                                                                  background-position: center;}
                                              QPushButton:hover  {border : 1px solid lightgreen;
                                                                  background-color: rgba(0, 0, 0, 5);
                                                                  background-position: center;}                    
                                              QPushButton:pressed{border : 1px solid dark;
                                                                  background-color: lightgreen;
                                                                  background-position: center;}
                                             """)
        b_add.clicked.connect(self.add_new_contact)

        b_import = QPushButton("Импортировать")
        b_import.setStyleSheet("""QPushButton:!hover {background-color: rgba(0, 0, 0, 5);
                                                                          background-position: center;}
                                                      QPushButton:hover  {border : 1px solid lightgreen;
                                                                          background-color: rgba(0, 0, 0, 5);
                                                                          background-position: center;}                    
                                                      QPushButton:pressed{border : 1px solid dark;
                                                                          background-color: lightgreen;
                                                                          background-position: center;}
                                                     """)
        b_import.clicked.connect(self.load_config_file)

        b_export = QPushButton("Экспортировать")
        b_export.setStyleSheet("""QPushButton:!hover {background-color: rgba(0, 0, 0, 5);
                                                                                  background-position: center;}
                                                              QPushButton:hover  {border : 1px solid lightgreen;
                                                                                  background-color: rgba(0, 0, 0, 5);
                                                                                  background-position: center;}                    
                                                              QPushButton:pressed{border : 1px solid dark;
                                                                                  background-color: lightgreen;
                                                                                  background-position: center;}
                                                             """)
        b_export.clicked.connect(self.save_config_file)

        b_del = QPushButton("Удалить")
        b_del.setStyleSheet("""QPushButton:!hover {background-color: rgba(0, 0, 0, 5);
                                                                  background-position: center;}
                                              QPushButton:hover  {border : 1px solid red;
                                                                  background-color: rgba(0, 0, 0, 5);
                                                                  background-position: center;}                    
                                              QPushButton:pressed{border : 1px solid dark;
                                                                  background-color: red;
                                                                  background-position: center;}
                                             """)
        b_del.clicked.connect(self.func_del_user)

        b_close = QPushButton("Закрыть")
        b_close.setStyleSheet("""QPushButton:!hover {background-color: rgba(0, 0, 0, 5);
                                                                  background-position: center;}
                                              QPushButton:hover  {border : 1px solid red;
                                                                  background-color: rgba(0, 0, 0, 5);
                                                                  background-position: center;}                    
                                              QPushButton:pressed{border : 1px solid dark;
                                                                  background-color: red;
                                                                  background-position: center;}
                                             """)
        b_close.clicked.connect(self.close_app)
        maket = QGridLayout()
        maket.addWidget(self.table, 0, 0, 1, 2)
        maket.addWidget(b_add, 1, 0)
        maket.addWidget(b_del, 1, 1)
        maket.addWidget(b_import, 2, 0)
        maket.addWidget(b_export, 2, 1)
        maket.addWidget(b_close, 3, 0, 1, 2)
        self.setLayout(maket)

        self.db.close()

    def model_table(self):
        self.model = QSqlTableModel()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setTable("call_number")
        self.model.select()
        self.model.setHeaderData(1, Qt.Horizontal, "Имя")
        self.model.setHeaderData(2, Qt.Horizontal, "Фамилия")
        self.model.setHeaderData(3, Qt.Horizontal, "Номер")
        self.model.setHeaderData(4, Qt.Horizontal, "Примечание")

        return self.model

    def table(self):
        self.tableView = QTableView()
        self.tableView.setMinimumSize(300, 200)
        self.tableView.installEventFilter(self)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        return self.tableView

    def close_app(self):
        message = QMessageBox()
        message.setWindowTitle('Внимание!')
        message.setText('<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Вы уверены, что хотите выйти?</b></center></FONT>')
        message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        but_yes = message.button(QMessageBox.Ok)
        but_yes.setText("Да")
        but_no = message.button(QMessageBox.Cancel)
        but_no.setText("Нет")
        close_message = message.exec_()
        if close_message == QMessageBox.StandardButton.Ok:
            self.close()

    def save_config_file(self):
        self.save_conf = QDialog(self)
        label = QLabel("Выберите, куда сохранить конфигурацию:")
        self.le_save_conf = QLineEdit()
        self.but_review = QPushButton("Обзор")
        self.but_review.clicked.connect(self.browse_file_save)
        but_save = QPushButton("Сохранить")
        but_save.clicked.connect(self.export_cont)
        but_cancel = QPushButton("Отмена")
        but_cancel.clicked.connect(self.close_save_conf)

        maket = QGridLayout()
        maket.addWidget(label, 0, 0, 1, 2)
        maket.addWidget(self.le_save_conf, 1, 0, 1, 1)
        maket.addWidget(self.but_review, 1, 1, 1, 1)
        maket.addWidget(but_save, 2, 0, 1, 1)
        maket.addWidget(but_cancel, 2, 1, 1, 1)

        self.save_conf.setLayout(maket)
        self.save_conf.show()

    def browse_file_save(self):
        browse_location_save = QFileDialog.getExistingDirectory(self, "Выбор папки для сохранения...")
        self.le_save_conf.setText(browse_location_save)

    def load_config_file(self):
        self.load_conf = QDialog(self)
        label = QLabel("Выберите, конфигурационный файл (.csv):")
        self.le_load_conf = QLineEdit()
        but_review = QPushButton("Обзор")
        but_review.clicked.connect(self.browse_file_load)
        but_load = QPushButton("Загрузить")
        but_load.clicked.connect(self.import_cont)
        but_cancel = QPushButton("Отмена")
        but_cancel.clicked.connect(self.close_load_conf)

        maket = QGridLayout()
        maket.addWidget(label, 0, 0, 1, 2)
        maket.addWidget(self.le_load_conf, 1, 0, 1, 1)
        maket.addWidget(but_review, 1, 1, 1, 1)
        maket.addWidget(but_load, 2, 0, 1, 1)
        maket.addWidget(but_cancel, 2, 1, 1, 1)

        self.load_conf.setLayout(maket)
        self.load_conf.show()

    def browse_file_load(self):
        browse_files_book_ost = QFileDialog.getOpenFileName(self, 'Выберите файл, содержащий тел. справочник...', '', 'csv files (*.csv)')
        self.le_load_conf.setText(browse_files_book_ost[0])

    def close_save_conf(self):
        self.save_conf.close()

    def close_load_conf(self):
        self.load_conf.close()

    def add_new_contact(self):
            self.add_new_user = QDialog()
            self.add_new_user.setWindowTitle("Добавить...")
            self.add_new_user.setFixedSize(300, 250)
            self.le_name = QLineEdit()
            self.le_name.setMinimumSize(100, 40)
            self.le_name.setPlaceholderText("Укажите имя")
            self.le_surname = QLineEdit()
            self.le_surname.setMinimumSize(100, 40)
            self.le_surname.setPlaceholderText("Укажите фамилию")
            self.le_call_num = QLineEdit()
            self.le_call_num.setMinimumSize(100, 40)
            self.le_call_num.setPlaceholderText("Укажите номер телефона")
            self.le_other = QLineEdit()
            self.le_other.setMinimumSize(100, 40)
            self.le_other.setPlaceholderText("Примечание")

            b_add = QPushButton("Добавить")
            b_add.clicked.connect(self.func_add_new_user)
            b_cancel = QPushButton("Отмена")
            b_cancel.clicked.connect(self.close_add_new_cont)

            maket = QGridLayout()
            maket.addWidget(self.le_name, 0, 0, 1, 2)
            maket.addWidget(self.le_surname, 1, 0, 1, 2)
            maket.addWidget(self.le_call_num, 2, 0, 1, 2)
            maket.addWidget(self.le_other, 3, 0, 1, 2)
            maket.addWidget(b_add, 4, 0)
            maket.addWidget(b_cancel, 4, 1)

            self.add_new_user.setLayout(maket)
            self.add_new_user.show()

    def close_add_new_cont(self):
        self.add_new_user.close()

    def message_box_attention(self, title, message, button):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(message)
        msgBox.setStandardButtons(button)
        msgBox.exec_()

    def func_add_new_user(self):
        self.base_line_edit = [self.le_name, self.le_surname, self.le_call_num]
        for line_edit in self.base_line_edit:
            if len(line_edit.text()) == 0:
                self.message_box_attention('Внимание!',
                                           '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Вы не заполнили поля</b></center></FONT>',
                                           QMessageBox.Ok)
                return
        else:
            if os.access('config/call_number.db', os.F_OK) == False:
                self.message_box_attention('Внимание!',
                                           '<center><b style=font-size:8pt><FONT FACE="Century Gothic">системная ошибка [0x000001]</b></center></FONT>'
                                           '<center><b style=font-size:8pt><FONT FACE="Century Gothic">свяжитесь с тех. поддержкой</b></center></FONT>',
                                           QMessageBox.Ok)
            else:
                con = sqlite3.connect('config/call_number.db')
                cur = con.cursor()
                cur.execute(f"INSERT INTO call_number (name, surname, number, other) VALUES ('{self.le_name.text()}','{self.le_surname.text()}','{self.le_call_num.text()}','{self.le_other.text()}')")
                con.commit()
                self.message_box_attention('Поздравляю!',
                                           '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Новый контакт добавлен!</b></center></FONT>',
                                           QMessageBox.Ok)
                self.add_new_user.close()
                cur.close()
                con.close()
                self.model_updadter()

    def func_del_user(self):
        if self.table.selectionModel().hasSelection():
            for index in self.table.selectedIndexes():
                message = QMessageBox()
                message.setWindowTitle('Внимание!')
                message.setText('<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Вы хотите удалить'
                               f'<br> контакт: {self.model_table().index(self.table.currentIndex().row(), 1).data()} ?</b></center></FONT>')
                message.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                but_yes = message.button(QMessageBox.Ok)
                but_yes.setText("Да")
                but_no = message.button(QMessageBox.Cancel)
                but_no.setText("Нет")
                close_message = message.exec_()
                if close_message == QMessageBox.StandardButton.Ok:
                    self.model.removeRow(index.row())
                    self.table.setModel(self.model_table())
        else:
            self.message_box_attention('Внимание!',
                                       '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Для удаления контакта, выделите его</b></center></FONT>',
                                       QMessageBox.Ok)

    def export_cont(self):
        with open(f"{self.le_save_conf.text()}/contact.csv", "w", newline='') as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.model.rowCount()):
                fields = [self.model.data(self.model.index(rowNumber, columnNumber), Qt.DisplayRole)
                    for columnNumber in range(self.model.columnCount())]
                writer.writerow(fields)
            self.message_box_attention('Внимание!',
                                           '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Файл с контактами успешно сохранен:</b></center></FONT>'
                                           f'<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Файл: contact.csv,сохранен: {self.le_save_conf.text()}</b></center></FONT>',
                                           QMessageBox.Ok)
            self.save_conf.close()

    def import_cont(self):
        con = sqlite3.connect('config/call_number.db')
        with open(f"{self.le_load_conf.text()}", "r") as fileInput:
            for row in csv.reader(fileInput):
                cur = con.cursor()
                cur.execute(f"INSERT INTO call_number (name, surname, number, other) VALUES ('{row[1]}','{row[2]}','{row[3]}','{row[4]}')")
                con.commit()
        self.message_box_attention('Поздравляем!',
                                   f'<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Файл: {self.le_load_conf.text()}, успешно импортирован.</b></center></FONT>',
                                   QMessageBox.Ok)
        cur.close()
        con.close()
        self.load_conf.close()
        self.model_updadter()

    def model_updadter(self):
        self.db.open()
        self.model.select()
        self.db.close()

if __name__ == ('__main__'):
    import sys
    App = QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(App.exec_())