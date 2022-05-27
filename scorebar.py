# importing libraries
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import * 
from PyQt6.QtCore import * 
import matplotlib.pyplot as plt
import matplotlib as mpl


class ScoreBar(QProgressBar):

    def __init__(self):

        super(ScoreBar, self).__init__()

        # Creating color map for progress bar
        self.cmap0 = plt.get_cmap('hot')
        self.cmap = plt.get_cmap('hot')

        # creating progress bar
        #self.bar = QProgressBar(self)

        # setting geometry to progress bar
        #self.setGeometry(0, 0, 200, 800)
        self.setTextVisible(0)

        # set value to progress bar
        self.maxval = 100
        self.setValue(self.maxval)

        # setting alignment to center
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setOrientation(Qt.Orientation.Vertical)

        #setting gradient color to progress bar
        self.cmapmax = .75#.99
        aa = str(mpl.colors.to_hex(self.cmap(self.cmapmax)))
        ab = str(mpl.colors.to_hex(self.cmap(self.cmapmax/2)))

        self.setStyleSheet("QProgressBar::chunk "
                    "{"
                    "background: QLinearGradient( x1: 0, y1: 0,"
                                                "x2: 0, y2: 1,"
                                            "stop: 0 "+aa+","
                                            "stop: 1 "+ab+" );"
                    "}"
                    "QProgressBar "
                    "{"
                    "border : none;"
                #   "background: QLinearGradient( x1: 0, y1: 0,"
                #                                 "x2: 1, y2: 0,"
                #                             "stop: 0 #00ffff,"
                #                             "stop: 1 #ff000f );"
                    "}")


    def update_bar(self, value):

        # set value to progress bar
        self.setValue(value)

        #setting gradient color to progress bar
        cmapval = self.cmapmax*(value/self.maxval)
        aa = str(mpl.colors.to_hex(self.cmap(cmapval)))
        ab = str(mpl.colors.to_hex(self.cmap(cmapval/2)))
        self.setStyleSheet("QProgressBar::chunk "
                    "{"
                    "background: QLinearGradient( x1: 0, y1: 0,"
                                                "x2: 0, y2: 1,"
                                            "stop: 0 "+aa+","
                                            "stop: 1 "+ab+" );"
                    "}"
                    "QProgressBar "
                    "{"
                    "border : none;"
                #   "background: QLinearGradient( x1: 0, y1: 0,"
                #                                 "x2: 1, y2: 0,"
                #                             "stop: 0 #00ffff,"
                #                             "stop: 1 #ff000f );"
                    "}")