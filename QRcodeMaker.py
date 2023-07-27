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
        self.input_field.returnPressed.connect(self.Generate_qr)
        wlcm_lab=QLabel("QRCodeMaker")
        wlcm_lab.setAlignment(Qt.AlignCenter) 
        wlcm_lab.setStyleSheet(self.stylesheet)
        box.addWidget(wlcm_lab)
        box.addStretch()
        desc_lab=QLabel("A simple app to simplify getting Qrcode with additional \n features enjoy using it ")
        desc_lab.setAlignment(Qt.AlignCenter)
        desc_lab.setObjectName("Desc")

        box.addWidget(desc_lab)
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
            self.animate_transition()  # Trigger the animation after setting the current widget
        else:
            self.UpdateQrWindow()
            self.animate_transition()
    
    def ShowNextWindow(self):
        self.setCurrentWidget(self.w2)

    def animate_transition(self):
        self.anim=QPropertyAnimation(self.main_widget, b"pos")
        self.anim.setEndValue(QPoint(-500, 0))
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim.start()
        self.anim.finished.connect(self.ShowNextWindow)
        print("animation")


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

    def animate_transition(self):
        self.anim=QPropertyAnimation(self, b"pos")
        self.anim.setEndValue(QPoint(-500, 0))
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim.start()
        self.anim.finished.connect(self.ShowNextWindow)
    
    def ShowNextWindow(self):
        self.MainWindow.setCurrentWidget(self.w3)

    def next(self):
        self.w3=SaveWindow(self)
        self.MainWindow.addWidget(self.w3)
        self.animate_transition()
        
        
    
    def ShowPrevWindow(self):
        self.MainWindow.setCurrentWidget(self.MainWindow.main_widget)
    def back(self):
        self.anim=QPropertyAnimation(self, b"pos")
        self.anim.setEndValue(QPoint(500, 0))
        self.anim.setDuration(300)
        self.anim.start()
        self.anim.finished.connect(self.ShowPrevWindow)


class CustomMessageBox(QDialog):
    def __init__(self, parent=None, message="", timeout=2000):
        super().__init__(parent, flags=Qt.FramelessWindowHint)

        with open('style.css', 'r') as f:
            self.stylesheet=f.read()

        self.setObjectName("dialog")
        self.setGeometry(1250, 100, 200, 80)

        self.setStyleSheet(self.stylesheet)  # Set the background color
        layout = QVBoxLayout()
        label = QLabel(message)
        label.setObjectName("msg")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

        self.animation = QVariantAnimation()
        self.animation.setDuration(2000)  # Animation duration in milliseconds
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.InCubic)

        self.animation.valueChanged.connect(self.update_opacity)
        self.animation.finished.connect(self.close)
        self.animation.start()
    
    def update_opacity(self, value):
        self.setWindowOpacity(value)
        

class  SaveWindow(QWidget):
    def __init__(self, qrwindow):
        super().__init__()
        self.qrwindow=qrwindow

        self.name_field=QLineEdit()
        self.name_field.setPlaceholderText("Enter file name ")
        self.name_field.setStyleSheet(self.qrwindow.MainWindow.stylesheet)
        self.name_field.returnPressed.connect(self.save_qr)

        save_btn=QPushButton("Save")
        save_btn.setStyleSheet(self.qrwindow.MainWindow.stylesheet)
        save_btn.clicked.connect(self.save_qr)

        self.layout=QVBoxLayout()
        self.layout.addWidget(self.name_field)
        self.layout.addWidget(save_btn)
        
        self.setLayout(self.layout)

        self.IsSaveWindowCreated=True
    
    def show_message_box(self):
        message = "Saved Successfully!"
        msg_box = CustomMessageBox(self, message)
        msg_box.exec_()
    
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
                self.show_message_box()


def main():
    app = QApplication(sys.argv)

    home=MainWindow()
    home.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()




