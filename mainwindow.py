# This Python file uses the following encoding: utf-8

import sys
import numpy as np

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import pyqtSlot, QTimer
from PyQt6 import uic
from scorebar import ScoreBar

STATUS = {"RUNNING": 0, "IDLE": 1, "PAUSED": 3, "FINISHED": 4}

MAXPOWER = 100
THRESHOLD = 80
MAXTIME = 20# s
MAX_LEADERBOARD_ENTRIES = 7


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("form.ui", self)

        self.status = STATUS["IDLE"]

        self.maxpower = 0
        self.threshold = THRESHOLD

        self.scoreBar = ScoreBar()
        self.scoreBar.setGeometry(0,0,200,800)
        self.scoreBar.show()
        self.horizontalLayout_4.addWidget(self.scoreBar)
        self.scoreBar.update_bar(0)

        self.movie = QMovie('image.imageformat.fullwidth.84826694.gif')
        self.logoLabel.setMovie(self.movie)
        self.movie.start()

        #self.powerSlider.setMaximum(MAXPOWER)

        self.clockTimer = QTimer(self)
        self.max_time = MAXTIME
        self.time = self.max_time
        self.clockTimer.setInterval(1000)
        self.clockTimer.timeout.connect(self.updateClock)
        self.resetTimer()

        self.powerTimer = QTimer(self)
        self.powerTimer.setInterval(100)
        self.powerTimer.timeout.connect(self.updatePowerMeter)

        try:
            self.leaderBoard = np.load("leaderboard.npy").tolist()
            self.updateLeaderBoard()
        except FileNotFoundError:
            self.leaderBoard = []

    @pyqtSlot()
    def startButtonPressed(self):
        if self.status == STATUS["IDLE"] or self.status == STATUS["PAUSED"]:
            self.startButton.setText("Pause")
            self.status = STATUS["RUNNING"]
            self.clockTimer.start()
            self.powerTimer.start()
        elif self.status == STATUS["RUNNING"]:
            self.startButton.setText("Continue")
            self.status = STATUS["PAUSED"]
            self.clockTimer.stop()

        if self.status != STATUS["IDLE"]:
            self.nameInput.setEnabled(False)

    @pyqtSlot()
    def resetButtonPressed(self):
        self.startButton.setText("Start")
        self.startButton.setEnabled(True)
        self.resetTimer()
        self.nameInput.setEnabled(True)
        self.status = STATUS["IDLE"]
        self.maxpower = 0
        self.maxPowerSlider.setValue(0)

    def resetTimer(self):
        self.clockTimer.stop()
        self.time = self.max_time
        self.timerLabel.setText(f"{self.time//60:02}:{self.time%60:02}")

    def updateClock(self):
        self.time -= 1
        self.timerLabel.setText(f"{self.time//60:02}:{self.time%60:02}")
        if self.time <= 10:
            # 10 s left, red timer!
            self.timerLabel.setStyleSheet('color: red;')

        if self.time <= 0:
            self.status = STATUS["FINISHED"]
            self.timesup()

    def timesup(self):
        self.startButton.setEnabled(False)
        self.clockTimer.stop()
        self.updateLeaderBoard()

    def updateLeaderBoard(self):
        if len(self.nameInput.text()) > 0:
            self.leaderBoard.append([self.nameInput.text(), self.maxpower, self.time])
            np.save("leaderboard.npy", self.leaderBoard)
        lb_arr = np.array(self.leaderBoard)
        times = lb_arr[:, 2].astype(float)
        isort = np.argsort(times)
        lb_arr = lb_arr[isort, :]

        i_timeout = np.where(times[isort] == 0)[0]

        timeout_arr = lb_arr[i_timeout,:]

        isort_timeout = np.argsort(timeout_arr[:, 1].astype(float))

        lb_arr[i_timeout, :] = lb_arr[i_timeout, :][isort_timeout]
        lb_arr = lb_arr[::-1,:]

        # Now lib_arr has been sorted according to (1) time to finish and (2) max power achieved.

        self.label_3.setText(self.generateLeaderboardTxt(lb_arr))

        print(lb_arr)

    def generateLeaderboardTxt(self, lb_array):

        text = f"{'rank' : <5}{'name' : <20}{'score' : <7}{'time' : <4}\n"
        for i in range(min(MAX_LEADERBOARD_ENTRIES, len(lb_array))):
            row = lb_array[i]
            elapsed = MAXTIME - int(row[2])
            text += f"{str(i+1)+'.': <5}{row[0] : <20}{float(row[1]): <8.2f}{int(elapsed)//60:02}:{int(elapsed)%60:02}\n"
        
        return text

    def updatePowerMeter(self):

        power = self.getCurrentPower()

        #.setValue(int(power))

        self.scoreBar.update_bar(int(power))

        if power > self.maxpower and self.status == STATUS["RUNNING"]:
            self.maxpower = power
            self.maxPowerSlider.setValue(int(power))
            self.powerLabel.setText(str(int(power)))

            if power >= self.threshold:
                self.status = STATUS["FINISHED"]
                self.timesup()

    def getCurrentPower(self):
        # Insert code connecting to power meter here!
        return np.random.random()*100*(1+self.max_time - self.time)/(self.max_time+1)


if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
