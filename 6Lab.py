import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QComboBox, QLabel, QLineEdit, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class DataAnalysisApp(QWidget):
    def __init__(self):
        super().__init__()

        # Инициализация интерфейса
        self.initUI()

        # Переменная для хранения данных
        self.data = None

    def initUI(self):
        # Основной layout
        layout = QVBoxLayout()

        # Кнопка загрузки данных
        self.load_button = QPushButton('Загрузить данные', self)
        self.load_button.clicked.connect(self.load_data)
        layout.addWidget(self.load_button)

        # Метка для отображения статистики
        self.stats_label = QLabel('Статистика данных', self)
        layout.addWidget(self.stats_label)

        # Комбо-бокс для выбора типа графика
        self.chart_type = QComboBox(self)
        self.chart_type.addItem('Линейный график')
        self.chart_type.addItem('Гистограмма')
        self.chart_type.addItem('Круговая диаграмма')
        self.chart_type.currentIndexChanged.connect(self.plot_data)  # Обновляем график при изменении выбора
        layout.addWidget(self.chart_type)

        # Поле для отображения графиков
        self.canvas = FigureCanvas(Figure(figsize=(8, 6)))
        layout.addWidget(self.canvas)

        # Добавление нового значения
        input_layout = QHBoxLayout()
        self.new_value_input = QLineEdit(self)
        self.new_value_input.setPlaceholderText('Введите новое значение (Date, Value1, Value2)')
        input_layout.addWidget(self.new_value_input)

        self.add_button = QPushButton('Добавить новое значение', self)
        self.add_button.clicked.connect(self.add_new_value)
        input_layout.addWidget(self.add_button)

        layout.addLayout(input_layout)

        # Установка главного layout
        self.setLayout(layout)
        self.setWindowTitle('Анализ данных')

    def load_data(self):
        # Загрузка CSV файла
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Загрузить CSV", "", "CSV Files (*.csv)", options=options)

        if file_path:
            self.data = pd.read_csv(file_path)

            # Отображаем статистику по данным
            stats = self.get_data_stats()
            self.stats_label.setText(stats)

            # Визуализируем данные
            self.plot_data()

    def get_data_stats(self):
        # Статистика: количество строк и столбцов, минимальные и максимальные значения
        if self.data is not None:
            stats = f'Строк: {len(self.data)}\nСтолбцов: {len(self.data.columns)}\n'
            stats += f'Минимальные значения:\n{self.data.min()}\n'
            stats += f'Максимальные значения:\n{self.data.max()}'
            return stats
        return 'Данные не загружены'

    def plot_data(self):
        if self.data is not None:
            # Очистка предыдущего графика
            self.canvas.figure.clf()

            # Получаем тип графика
            chart_type = self.chart_type.currentText()

            # Создаем новый график
            ax = self.canvas.figure.add_subplot(111)

            if chart_type == 'Линейный график':
                # Убедимся, что столбцы 'Date' и 'Value1' существуют
                if 'Date' in self.data.columns and 'Value1' in self.data.columns:
                    ax.plot(self.data['Date'], self.data['Value1'])
                    ax.set_title('Линейный график')
                    ax.set_xlabel('Date')
                    ax.set_ylabel('Value1')

                    # Уменьшаем частоту отображения меток оси X
                    date_labels = self.data['Date']
                    step = len(date_labels) // 6  # Показываем 6 меток на оси X
                    ax.set_xticks(date_labels[::step])  # Отображаем метки через 'step'

                    # Поворот меток оси X для улучшения читаемости
                    plt.xticks(rotation=45)

            elif chart_type == 'Гистограмма':
                # Убедимся, что столбец 'Value2' существует
                if 'Value2' in self.data.columns:
                    ax.hist(self.data['Value2'], bins=20)
                    ax.set_title('Гистограмма')
                    ax.set_xlabel('Value2')
                    ax.set_ylabel('Частота')

            elif chart_type == 'Круговая диаграмма':
                # Убедимся, что столбец 'Category' существует
                if 'Category' in self.data.columns:
                    category_counts = self.data['Category'].value_counts()
                    ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%')
                    ax.set_title('Круговая диаграмма')

            # Обновляем отображение
            self.canvas.draw()

    def add_new_value(self):
        # Получаем ввод от пользователя
        new_value = self.new_value_input.text()

        if new_value:
            # Преобразуем ввод в список значений
            values = new_value.split(',')

            if len(values) == 3:  # Ожидаем 3 значения для Date, Value1 и Value2
                new_data = {
                    'Date': [values[0].strip()],
                    'Value1': [float(values[1].strip())],
                    'Value2': [float(values[2].strip())]
                }

                new_df = pd.DataFrame(new_data)

                # Добавляем новые данные в существующий DataFrame
                self.data = pd.concat([self.data, new_df], ignore_index=True)

                # Обновляем график
                self.plot_data()

                # Очищаем поле ввода
                self.new_value_input.clear()

            else:
                self.stats_label.setText('Введите данные в формате: Date, Value1, Value2')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DataAnalysisApp()
    ex.show()
    sys.exit(app.exec_())
