import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import qrcode
import png

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
       
        
        hbox=QHBoxLayout()
        next_btn=QPushButton("Next")
        self.iscreated=False
        next_btn.clicked.connect(self.Generate_qr)

        next_btn.setStyleSheet(self.stylesheet)

        cncl_btn=QPushButton("Cancel")
        hbox.addWidget(cncl_btn)
        hbox.addWidget(next_btn)

        box.addWidget(self.input_field)
        box.addLayout(hbox)

        self.main_widget.setLayout(box)
        self.main_widget.setStyleSheet(self.stylesheet)

        self.addWidget(self.main_widget)

        #widget2: Desplaying QR code
        self.w2=QWidget()

    
        
        



    def w2UI(self, path):
        layout=QVBoxLayout()
        img_view=QLabel()
        img=QPixmap(path)
        img_view.setPixmap(img)
        img_view.setStyleSheet(self.stylesheet)
        layout.addWidget(img_view)

        hbox=QHBoxLayout()
        back_btn=QPushButton("Back")
        save_btn=QPushButton("Save")
        back_btn.clicked.connect(self.back)

        save_btn.setStyleSheet(self.stylesheet)
        back_btn.setStyleSheet(self.stylesheet)

        hbox.addWidget(back_btn)
        hbox.addWidget(save_btn)
        layout.addLayout(hbox)

        self.w2.setStyleSheet(self.stylesheet)
        self.w2.setLayout(layout)

    def back(self):
        self.setCurrentWidget(self.main_widget)

    def Generate_qr(self):
        if not self.iscreated:
            self.iscreated=True
            img = qrcode.make(self.input_field.text)
            type(img)  # qrcode.image.pil.PilImage
            path="qrcode.png"
            img.save("qrcode.png")
            print("QR code created successfully! ")
            self.w2UI(path)
            self.addWidget(self.w2)
            self.setCurrentWidget(self.w2)
        else:
            self.setCurrentWidget(self.w2)


def main():
    app = QApplication(sys.argv)

    home=Window()
    home.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()




