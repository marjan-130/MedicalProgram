import os
from PyQt6 import QtCore

# Визначаємо абсолютний шлях до .qrc
qrc_file = os.path.abspath('resources.qrc')

# Вихідний файл
output_file = os.path.abspath('D:/універ/ргр/MedicalProgram/MedicalProgram/resources_rc.py')

# Для компіляції .qrc в .py, використаємо метод PyQt6 (хоча це не стандартний підхід)
try:
    QtCore.QResource.registerResource(qrc_file)  # Реєстрація ресурсів
    print(f"Файл {qrc_file} успішно скомпільовано в {output_file}.")
except Exception as e:
    print(f"Помилка: {e}")
