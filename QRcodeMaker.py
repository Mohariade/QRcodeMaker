import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import qrcode



class Window(QStackedWidget):

    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.setGeometry(1000, 100, 500, 500)
        
        #geting stylesheet from css file
        with open('style.css', 'r') as f:
            self.stylesheet=f.read()

        #main_widget
        self.main_widget=QWidget()
        box=QVBoxLayout(self)
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

        #widget2: Desplaying QR code
        self.w2=QWidget()


    def CreatQrWindow(self, tmpfile):
        layout=QVBoxLayout()
        self.img_view=QLabel()
        pixmap = QPixmap(tmpfile)
        self.img_view.setPixmap(pixmap)
        self.img_view.setAlignment(Qt.AlignCenter)
        self.img_view.setStyleSheet(self.stylesheet)
        layout.addWidget(self.img_view)
       
        hbox=QHBoxLayout()
        back_btn=QPushButton("Back")
        next2_btn=QPushButton("Next")
        back_btn.clicked.connect(self.back)

        next2_btn.setStyleSheet(self.stylesheet)
        back_btn.setStyleSheet(self.stylesheet)
        self.IsSaveWindowCreated=False
        next2_btn.clicked.connect(self.CreatSaveWindow)
        hbox.addWidget(back_btn)
        hbox.addWidget(next2_btn)
        layout.addLayout(hbox)

        self.w2.setStyleSheet(self.stylesheet)
        self.w2.setLayout(layout)

    def CreatSaveWindow(self):
        if (self.IsSaveWindowCreated):
            self.setCurrentWidget(self.SaveWindow)
        else:
            self.SaveWindow=QWidget()
            self.name_field=QLineEdit()
            self.name_field.setPlaceholderText("Enter file name ")
            self.name_field.setStyleSheet(self.stylesheet)

            save_btn=QPushButton("Save")
            save_btn.setStyleSheet(self.stylesheet)
            save_btn.clicked.connect(self.save_qr)

            layout=QVBoxLayout()
            layout.addWidget(self.name_field)
            layout.addWidget(save_btn)
            
            self.SaveWindow.setLayout(layout)
            self.addWidget(self.SaveWindow)
            self.setCurrentWidget(self.SaveWindow)

            self.IsSaveWindowCreated=True

    def UpdateQrWindow(self, tmpfile):
        pixmap=QPixmap(tmpfile)
        self.img_view.setPixmap(pixmap)

    def back(self):
        self.setCurrentWidget(self.main_widget)

    def Generate_qr(self):
        tmpfile="qrcode.png"
        if (os.path.exists(tmpfile)):
            os.remove(tmpfile)
            print("file removed!")
        print("text: ", self.input_field.text())
        self.qr_img = qrcode.make(self.input_field.text())
        print("QR code created successfully! ")
        self.qr_img.save(tmpfile)

        if not (self.iscreated):
            print("Not created befor")
            self.CreatQrWindow(tmpfile)
            self.addWidget(self.w2)
            self.iscreated=True
            self.setCurrentWidget(self.w2)
            print("test")
        else:
            self.UpdateQrWindow(tmpfile)
            self.setCurrentWidget(self.w2)

        
    def save_qr(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)
        if folder_path:
            self.selected_folder = folder_path
            file_name=self.name_field.text()
            if  file_name:
                # Use the selected folder path and file name to save the image
                file_path = f"{folder_path}/{file_name}.png"  # Modify the file extension as needed
                self.qr_img.save(file_path)

    def show_next_window(self):
        next_window = Window2()
        self.animate_transition(next_window)

    def animate_transition(self, next_window):
        current_geometry = self.geometry()
        next_geometry = QRect(current_geometry.x() + 50, current_geometry.y(), current_geometry.width(), current_geometry.height())

        animation = QPropertyAnimation(self, b'geometry')
        animation.setDuration(500)
        animation.setStartValue(current_geometry)
        animation.setEndValue(next_geometry)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.finished.connect(next_window.show)
        animation.start(QPropertyAnimation.DeleteWhenStopped)

        
def main():
    app = QApplication(sys.argv)

    home=Window()
    home.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()




