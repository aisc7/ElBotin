# main.py
from view.View import MainWindow
import sys
from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.main()
    sys.exit(app.exec())