import math

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_# or sprite_##. It returns a list of the images.
def load_sprite(sprite_folder_name, number_of_frames):
    frames = []
    padding = math.ceil(math.log(number_of_frames - 1, 10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding, '0') + ".png"
        frames.append(QPixmap(folder_and_file_name))

    return frames

class SpritePreview(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sprite Animation Preview")
        # This loads the provided sprite and would need to be changed for your own.
        self.num_frames = 21
        self.frames = load_sprite('spriteImages', self.num_frames)

        self.current_frame = 0
        self.is_playing = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)

        # Make the GUI in the setupUI method
        self.setupUI()

    def setupUI(self):
        # An application needs a central widget - often a QFrame
        frame = QFrame()
        main_layout = QVBoxLayout()

        # Sprite image display
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setPixmap(self.frames[self.current_frame])
        main_layout.addWidget(self.image_label)

        # FPS label
        fps_label = QLabel("Frames per second")
        fps_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(fps_label)

        # FPS slider (1–100, with tick marks)
        self.fps_slider = QSlider(Qt.Orientation.Horizontal)
        self.fps_slider.setMinimum(1)
        self.fps_slider.setMaximum(100)
        self.fps_slider.setValue(10)
        self.fps_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.fps_slider.setTickInterval(10)
        self.fps_slider.valueChanged.connect(self.on_fps_changed)
        main_layout.addWidget(self.fps_slider)

        # Current FPS value display
        self.fps_value_label = QLabel(str(self.fps_slider.value()))
        self.fps_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.fps_value_label)

        # Start/Stop button
        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.clicked.connect(self.toggle_animation)
        main_layout.addWidget(self.start_stop_button)

        frame.setLayout(main_layout)
        self.setCentralWidget(frame)

    def on_fps_changed(self, value):
        self.fps_value_label.setText(str(value))
        if self.is_playing:
            self.timer.setInterval(1000 // value)

    def toggle_animation(self):
        if self.is_playing:
            self.timer.stop()
            self.is_playing = False
            self.start_stop_button.setText("Start")
        else:
            fps = self.fps_slider.value()
            self.timer.start(1000 // fps)
            self.is_playing = True
            self.start_stop_button.setText("Stop")

    def next_frame(self):
        self.current_frame = (self.current_frame + 1) % self.num_frames
        self.image_label.setPixmap(self.frames[self.current_frame])


def main():
    app = QApplication([])
    # Create our custom application
    window = SpritePreview()
    # And show it
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
