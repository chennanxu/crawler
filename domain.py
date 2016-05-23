import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from lxml import html


class Render(QWebPage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()


url = "http://wh.lianjia.com/ershoufang/104100075180.html"
r = Render(url)
result = r.frame.toHtml()
formatted_result = str(result.toAscii())
tree = html.fromstring(formatted_result)
getting = tree.xpath('/html/body/div[4]/div[2]/div[1]/div[1]/div[1]/span')
print(getting[0].text)
