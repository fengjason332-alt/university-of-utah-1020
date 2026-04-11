# GitHub repo: https://github.com/fengjason332-alt/university-of-utah-1020

import sys
import glob
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                             QHBoxLayout, QSlider, QPushButton, QFrame, QMenuBar)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer


class SpritePreviewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sprite Preview")

        # Load all sprite images
        self.sprites = sorted(glob.glob("spriteImages/sprite_*.png"))
        self.current_frame = 0

        # Main layout
        main_layout = QVBoxLayout()

        # Menu bar
        menu_bar = QMenuBar()
        file_menu = menu_bar.addMenu("File")
        pause_action = file_menu.addAction("Pause")
        pause_action.triggered.connect(self.pause)
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        main_layout.setMenuBar(menu_bar)

        # Top area: sprite + slider side by side
        top_layout = QHBoxLayout()

        self.sprite_label = QLabel()
        pixmap = QPixmap(self.sprites[0])
        self.sprite_label.setPixmap(pixmap)
        self.sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(self.sprite_label)

        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setValue(1)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.slider.setTickInterval(20)
        self.slider.valueChanged.connect(self.update_fps)
        top_layout.addWidget(self.slider)

        main_layout.addLayout(top_layout)

        # FPS label
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("Frames per second"))
        self.fps_value_label = QLabel("1")
        fps_layout.addWidget(self.fps_value_label)
        main_layout.addLayout(fps_layout)

        # Start/Stop button
        self.button = QPushButton("Start")
        self.button.clicked.connect(self.toggle_animation)
        main_layout.addWidget(self.button)

        self.setLayout(main_layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)

    def update_fps(self, fps):
        self.fps_value_label.setText(str(fps))
        if self.timer.isActive():
            self.timer.setInterval(int(1000 / fps))

    def next_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.sprites)
        pixmap = QPixmap(self.sprites[self.current_frame])
        self.sprite_label.setPixmap(pixmap)

    def toggle_animation(self):
        if self.timer.isActive():
            self.timer.stop()
            self.button.setText("Start")
        else:
            fps = self.slider.value()
            self.timer.start(int(1000 / fps))
            self.button.setText("Stop")

    def pause(self):
        self.timer.stop()
        self.button.setText("Start")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpritePreviewer()
    window.show()
    sys.exit(app.exec())