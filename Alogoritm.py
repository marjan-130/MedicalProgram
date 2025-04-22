from PyQt6.QtWidgets import QMessageBox, QApplication

def handle_button_click(text: str, window):
    if text in ["Enter", "Login"]:
        QMessageBox.information(window, "Info", "Please wait to update")
    elif text == "Exit":
        QApplication.quit()

