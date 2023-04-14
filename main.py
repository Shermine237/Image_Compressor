from packages.ui.DesignUI import Application
from packages.windows.windows import Windows

app = Application()

windows = Windows()
windows.show()

app.exec()
