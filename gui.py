import sys

from player.playlist_wrapper import PlaylistWrapper
from player.music_crawler import MusicCrawler

from PyQt5 import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import (QToolButton, QStyle, QHBoxLayout, QPushButton,
                             QVBoxLayout, QWidget, QFileDialog, QMessageBox,
                             QListWidget, QInputDialog)


class PlayerControls(QWidget):

    play = pyqtSignal()
    pause = pyqtSignal()
    stop = pyqtSignal()
    next = pyqtSignal()
    previous = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.playerState = QMediaPlayer.StoppedState

        self.playButton = QToolButton(clicked=self.playClicked)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        self.stopButton = QToolButton(clicked=self.stop)
        self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))

        self.pauseButton = QToolButton(clicked=self.pause)
        self.pauseButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))

        self.nextButton = QToolButton(clicked=self.next)
        self.nextButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaSkipForward))

        self.previousButton = QToolButton(clicked=self.previous)
        self.previousButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaSkipBackward))

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stopButton)
        layout.addWidget(self.previousButton)
        layout.addWidget(self.playButton)
        layout.addWidget(self.nextButton)
        layout.addWidget(self.pauseButton)
        self.setLayout(layout)

    def playClicked(self):
        if self.playerState in (QMediaPlayer.StoppedState,
                                QMediaPlayer.PausedState):
            self.play.emit()
        elif self.playerState == QMediaPlayer.PlayingState:
            self.pause.emit()


class Player(QWidget):
    def __init__(self, playlist=''):
        super().__init__()

        self.player = QMediaPlayer()
        self.wrapper = PlaylistWrapper("Untitled")
        self.playlist = self.wrapper.playlist
        self.player.setPlaylist(self.playlist)

        browseButton = QPushButton("Browse", clicked=self.crawl)
        saveButton = QPushButton("Save", clicked=self.save)
        loadButton = QPushButton("Load", clicked=self.load)
        addButton = QPushButton("Add song", clicked=self.add_song)
        nameButton = QPushButton("Name", clicked=self.name_playlist)

        controls = PlayerControls()

        controls.play.connect(self.player.play)
        controls.pause.connect(self.player.pause)
        controls.stop.connect(self.player.stop)
        controls.next.connect(self.playlist.next)
        controls.previous.connect(self.playlist.previous)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(browseButton)
        controlLayout.addWidget(saveButton)
        controlLayout.addWidget(loadButton)
        controlLayout.addWidget(addButton)
        controlLayout.addWidget(nameButton)
        controlLayout.addStretch(1)
        controlLayout.addWidget(controls)
        controlLayout.addStretch(1)

        self.displayLayout = QHBoxLayout()
        self.playlist_view = QListWidget()
        self.displayLayout.addWidget(self.playlist_view)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.displayLayout)
        self.layout.addLayout(controlLayout)
        self.layout.addLayout(self.displayLayout)
        self.setLayout(self.layout)
        self.setWindowTitle(
            "letTheMusicPlaY - {} Playlist".format(self.wrapper.name))

    def crawl(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Browse here")
        crawler = MusicCrawler(dir_name)
        crawler.generate_playlist(self.wrapper)

        for song in self.wrapper.songs:
            self.playlist_view .addItem(
                "{} - {}".format(song.artist, song.title))

    def save(self):
        if self.wrapper.is_empty():
            box = QMessageBox()
            box.setText("Your playlist is empty")
            box.setWindowTitle("Sorry")
            box.exec_()
        else:
            dir_name = QFileDialog.getExistingDirectory(self, "Save here")
            self.wrapper.save(dir_name)

    def load(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load from here")

        try:
            self.wrapper.load(file_name)
        except AssertionError:
            box = QMessageBox()
            box.setText("This is not a playlist")
            box.setWindowTitle("Sorry")
            box.exec_()

        for song in self.wrapper.songs:
            self.playlist_view .addItem(
                "{} - {}".format(song.artist, song.title))

    def add_song(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose a song")
        try:
            self.wrapper.add_song(file_path)
            added_song = self.wrapper.path_to_song(file_path)
            self.playlist_view.addItem(
                "{} - {}".format(added_song.artist, added_song.title))
        except AssertionError:
            box = QMessageBox()
            box.setText("This is not file that I can open")
            box.setWindowTitle("Sorry")
            box.exec_()

    def name_playlist(self):
        new_name, _ = QInputDialog.getText(self, "Give name", "Enter name:")
        self.wrapper.name = new_name
        self.setWindowTitle(
            "letTheMusicPlaY - {} Playlist".format(self.wrapper.name))


if __name__ == '__main__':
    app = Qt.QApplication(sys.argv)
    pl = Player()
    pl.show()
    app.exec_()
