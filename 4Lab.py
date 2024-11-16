import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableView, QVBoxLayout, QPushButton,
    QLineEdit, QDialog, QFormLayout, QDialogButtonBox, QWidget, QMessageBox
)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            body TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_record(self, user_id, title, body):
        query = "INSERT INTO posts (user_id, title, body) VALUES (?, ?, ?)"
        self.conn.execute(query, (user_id, title, body))
        self.conn.commit()

    def delete_record(self, record_id):
        query = "DELETE FROM posts WHERE id = ?"
        self.conn.execute(query, (record_id,))
        self.conn.commit()


class AddRecordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Record")
        self.layout = QFormLayout(self)
        self.user_id_input = QLineEdit(self)
        self.title_input = QLineEdit(self)
        self.body_input = QLineEdit(self)

        self.layout.addRow("User ID:", self.user_id_input)
        self.layout.addRow("Title:", self.title_input)
        self.layout.addRow("Body:", self.body_input)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            self
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Database Manager")
        self.setGeometry(100, 100, 800, 600)

        self.database_manager = DatabaseManager("posts.db")

        # Set up the layout
        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search by title...")
        self.search_bar.textChanged.connect(self.filter_records)
        self.layout.addWidget(self.search_bar)

        # Table view
        self.table_view = QTableView(self)
        self.layout.addWidget(self.table_view)

        # Buttons
        self.refresh_button = QPushButton("Refresh", self)
        self.refresh_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.refresh_button)

        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.add_record)
        self.layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Delete", self)
        self.delete_button.clicked.connect(self.delete_record)
        self.layout.addWidget(self.delete_button)

        # Database connection
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("posts.db")
        if not self.db.open():
            QMessageBox.critical(self, "Database Error", self.db.lastError().text())
            sys.exit(1)

        # Table model
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable("posts")
        self.model.select()

        self.table_view.setModel(self.model)
        self.load_data()

    def load_data(self):
        self.model.select()

    def filter_records(self):
        filter_text = self.search_bar.text()
        self.model.setFilter(f"title LIKE '%{filter_text}%'")

    def add_record(self):
        dialog = AddRecordDialog(self)
        if dialog.exec_():
            user_id = dialog.user_id_input.text()
            title = dialog.title_input.text()
            body = dialog.body_input.text()
            self.database_manager.add_record(user_id, title, body)
            self.load_data()

    def delete_record(self):
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if selected_indexes:
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                "Are you sure you want to delete the selected record(s)?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                for index in selected_indexes:
                    record_id = self.model.data(self.model.index(index.row(), 0))
                    self.database_manager.delete_record(record_id)
                self.load_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
