import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import qrcode



class MainWindow(QStackedWidget):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(1000, 100, 500, 500)
        
        #geting stylesheet from css file
        with open('style.css', 'r') as f:
            self.stylesheet=f.read()

        #main_widget
        self.main_widget=QWidget()
        box=QVBoxLayout(self)

        #field to enter text that will be encoded in QR
        self.input_field=QLineEdit()
        self.input_field.setPlaceholderText("Enter your text ")

        wlcm_lab=QLabel("Creat QR Codes \nWith Infinity Styles")
        wlcm_lab.setAlignment(Qt.AlignCenter) 
        wlcm_lab.setStyleSheet(self.stylesheet)
        box.addWidget(wlcm_lab)

        box.addStretch()

        hbox=QHBoxLayout()

        next1_btn=QPushButton("Next")
        self.iscreated=False
        next1_btn.clicked.connect(self.Generate_qr)
        next1_btn.setStyleSheet(self.stylesheet)

        cncl_btn=QPushButton("Cancel")
        hbox.addWidget(cncl_btn)
        hbox.addWidget(next1_btn)

        box.addWidget(self.input_field)
        box.addStretch()
        box.addLayout(hbox)

        self.main_widget.setLayout(box)
        self.main_widget.setStyleSheet(self.stylesheet)

        self.addWidget(self.main_widget)


    def UpdateQrWindow(self):
        pixmap=QPixmap(self.tmpfile)
        self.w2.img_view.setPixmap(pixmap)

    def Generate_qr(self):
        self.tmpfile = "qrcode.png"
        if os.path.exists(self.tmpfile):
            os.remove(self.tmpfile)
            print("file removed!")
        print("text: ", self.input_field.text())
        self.qr_img = qrcode.make(self.input_field.text())
        print("QR code created successfully! ")
        self.qr_img.save(self.tmpfile)

        if not self.iscreated:
            print("Not created before")
            self.w2 = QrWindow(self)

            self.addWidget(self.w2)
            self.iscreated = True
            self.setCurrentWidget(self.w2)  # Set the QrWindow as the current widget
            self.show_next_window()  # Trigger the animation after setting the current widget
        else:
            self.UpdateQrWindow()
            self.setCurrentWidget(self.w2)
            self.show_next_window()

    def show_next_window(self):
        next_window =self.w2
        self.animate_transition(next_window)

    def animate_transition(self, next_window):
        current_geometry = self.geometry()
        next_geometry = QRect(current_geometry.x() + 200, current_geometry.y(), current_geometry.width(), current_geometry.height())

        animation = QPropertyAnimation(self, b'geometry')
        animation.setDuration(1000)  # Increase the duration to 1000 milliseconds (1 second)
        animation.setStartValue(current_geometry)
        animation.setEndValue(next_geometry)
        animation.setEasingCurve(QEasingCurve.OutElastic)  # Change the easing curve to OutElastic
        animation.finished.connect(next_window.show)
        animation.start(QPropertyAnimation.DeleteWhenStopped)


class QrWindow(QWidget):
    def __init__(self, MainWindow):
        super().__init__()
        self.MainWindow=MainWindow

        self.setGeometry(1000, 100, 500, 500)

        layout=QVBoxLayout()
        self.img_view=QLabel()
        self.tmpfile=self.MainWindow.tmpfile
        pixmap = QPixmap(self.MainWindow.tmpfile)
        self.img_view.setPixmap(pixmap)
        self.img_view.setAlignment(Qt.AlignCenter)
        self.img_view.setStyleSheet(self.MainWindow.stylesheet)
        layout.addWidget(self.img_view)
       
        hbox=QHBoxLayout()
        back_btn=QPushButton("Back")
        next2_btn=QPushButton("Next")
        back_btn.clicked.connect(self.back)

        next2_btn.setStyleSheet(self.MainWindow.stylesheet)
        back_btn.setStyleSheet(self.MainWindow.stylesheet)
        self.IsSaveWindowCreated=False
        next2_btn.clicked.connect(self.next)
        hbox.addWidget(back_btn)
        hbox.addWidget(next2_btn)
        layout.addLayout(hbox)

        self.setStyleSheet(self.MainWindow.stylesheet)
        self.setLayout(layout)

    def next(self):
        self.w3=SaveWindow(self)
        self.MainWindow.addWidget(self.w3)
        self.MainWindow.setCurrentWidget(self.w3)

    def back(self):
        self.MainWindow.setCurrentWidget(self.MainWindow.main_widget)


class  SaveWindow(QWidget):
    def __init__(self, qrwindow):
        super().__init__()
        self.qrwindow=qrwindow

        self.name_field=QLineEdit()
        self.name_field.setPlaceholderText("Enter file name ")
        self.name_field.setStyleSheet(self.qrwindow.MainWindow.stylesheet)

        save_btn=QPushButton("Save")
        save_btn.setStyleSheet(self.qrwindow.MainWindow.stylesheet)
        save_btn.clicked.connect(self.save_qr)

        layout=QVBoxLayout()
        layout.addWidget(self.name_field)
        layout.addWidget(save_btn)
        
        self.setLayout(layout)

        self.IsSaveWindowCreated=True
    
    def save_qr(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)
        if folder_path:
            self.selected_folder = folder_path
            file_name=self.name_field.text()
            if  file_name:
                # Use the selected folder path and file name to save the image
                file_path = f"{folder_path}/{file_name}.png"  # Modify the file extension as needed
                self.qrwindow.MainWindow.qr_img.save(file_path)


def main():
    app = QApplication(sys.argv)

    home=MainWindow()
    home.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()




