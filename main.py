import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem


class AddForm(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.setFixedSize(340, 270)
        self.addBtn.clicked.connect(self.add_coffee)

    def add_coffee(self):
        con = self.parent().cur.cursor()
        res = con.execute(f"SELECT * FROM Coffee").fetchall()
        last_ID = int(res[-1][0])
        con.execute(f"INSERT INTO Coffee "
                    f"VALUES ({last_ID + 1}, '{self.sortEdit.text()}', '{self.roastingBox.currentText()}', "
                    f"'{self.beansBox.currentText()}', '{self.tasteEdit.text()}', "
                    f"{self.priceEdit.text()}, {self.sizeEdit.text()})")
        self.parent().cur.commit()
        self.close()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.setFixedSize(760, 385)
        self.cur = sqlite3.connect("coffee.db")
        self.title = ["ID", "sort", "roasting", "ground_or_beans", "taste", "price", "size"]
        self.updateBtn.clicked.connect(self.update_table)
        self.addBtn.clicked.connect(self.add_window)
        self.saveBtn.clicked.connect(self.save_result)

    def update_table(self):
        con = self.cur.cursor()
        res = con.execute(f"SELECT * FROM Coffee").fetchall()
        self.tableWidget.setColumnCount(len(self.title))
        self.tableWidget.setHorizontalHeaderLabels(self.title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

    def save_result(self):
        con = self.cur.cursor()
        i = 0
        while True:
            try:
                ver = [self.tableWidget.item(i, j).text() for j in range(len(self.title))]
                con.execute(f"UPDATE Coffee "
                            f"SET sort = '{ver[1]}', "
                            f"roasting = '{ver[2]}', "
                            f"ground_or_beans = '{ver[3]}', "
                            f"taste = '{ver[4]}', "
                            f"price = {ver[5]}, "
                            f"size = {ver[6]} "
                            f"WHERE ID = {i + 1}")
            except AttributeError:
                break
            i += 1
        self.cur.commit()

    def add_window(self):
        new_form = AddForm(self)
        new_form.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
