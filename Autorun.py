from pywinauto import application
from pywinauto import timings
import time
import os

app = application.Application()
app.start("C:\\KiwoomFlash3\\Bin\\NKMiniStarter.exe")

title = "번개3 Login"
dlg = timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title=title))

pass_ctrl = dlg.Edit2
pass_ctrl.SetFocus()
pass_ctrl.TypeKeys('Kiwoom Login Password')

cert_ctrl = dlg.Edit3
cert_ctrl.SetFocus()
cert_ctrl.TypeKeys('공인인증서 Password')

btn_ctrl = dlg.Button0
btn_ctrl.Click()

time.sleep(300)
os.system("taskkill /f /im nkmini.exe")