import sys
import random
from functools import partial
from PySide6.QtWidgets import QMessageBox, QFileDialog
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtUiTools import QUiLoader

import urllib.request


class DownloadManager(QWidget):
    def __init__(self):
        super(DownloadManager, self).__init__()

        loader = QUiLoader()
        self.ui = loader.load('form.ui')
        self.setFocus()

        self.ui.btn_download.clicked.connect(self.download)
        self.ui.btn_browse.clicked.connect(self.browse_file)

        self.ui.show()

    def browse_file(self):
        save_file = QFileDialog.getSaveFileName(self, caption='Save File as', dir=".", filter="All Files (*.*)")
        print(save_file)

        self.ui.tb_dir.setText(save_file[0])

    def download(self):
        self.url = self.ui.tb_url.text()
        self.save_location = self.ui.tb_dir.text()
        print(self.save_location)
        print(self.ui.tb_url.text())

        try:
            urllib.request.urlretrieve(self.url, self.save_location, self.report)
        except Exception:
            QMessageBox.warning(self, 'Warning', 'Download Failed')
            return

        msg_box = QMessageBox()
        msg_box.setText("Download Completed")
        msg_box.exec()
        #msg_box.windowTitle('Report')
        self.reset()


    def report(self, blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 100 / totalsize
            self.ui.p_bar.setValue(int(percent))

    def reset(self):
        self.ui.p_bar.setValue(0)
        self.ui.tb_url.setText('')
        self.ui.tb_dir.setText('')



if __name__ == "__main__":
    app = QApplication([])
    window = DownloadManager()
    sys.exit(app.exec())
