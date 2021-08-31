import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Kiwoom import *

form_class = uic.loadUiType("MyTrader.ui")[0]

class MyWindow(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.kiwoom = Kiwoom()
        self.kiwoom.Comm_Connect()
        self.kiwoom.Get_LoginInfo()
        
        # 접속정보
        self.Print_TextBrowser()

        # Status Bar Timer Event 설정
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.Handle_Timeout)

        # 조회 버튼 이벤트 설정
        self.pushButton.clicked.connect(self.Handle_pushButton)

        # 실시간 조회 이벤트 설정
        self.timer2 = QTimer(self)
        self.timer2.start(1000*10)
        self.timer2.timeout.connect(self.Handle_Timeout2)

    def Print_TextBrowser(self) :
        self.textBrowser.append("계좌개수 : " + self.kiwoom.accountCnt)
        self.textBrowser.append("계좌번호 : " + self.kiwoom.accNo[0])
        self.textBrowser.append("사용자ID : " + self.kiwoom.userId)
        self.textBrowser.append("사용자이름 : " + self.kiwoom.userName)

        if self.kiwoom.keybSecurity == '0' :
            self.textBrowser.append("키보드보안 : 정상")
        else :
            self.textBrowser.append("키보드보안 : 해지")

        if self.kiwoom.firewallSet == '0' :
            self.textBrowser.append("방화벽설정 : 미설정")
        elif self.kiwoom.firewallSet == '1' :
            self.textBrowser.append("방화벽설정 : 설정")
        else :
            self.textBrowser.append("방화벽설정 : 해지")

    def Handle_Timeout(self) :
        curTime = QTime.currentTime()
        txtTime = curTime.toString("hh:mm:ss")
        timeMsg = "현재시간 : " + txtTime

        state = self.kiwoom.Get_ConnectState()
        if state == 1 :
            stateMsg = "서버 연결 중"
        else :
            stateMsg = "서버 연결 끊김"

        self.statusbar.showMessage(stateMsg + " | " + timeMsg)

    def Handle_Timeout2(self) :
        if self.checkBox.isChecked() :
            self.kiwoom.Get_Opw00001()
            self.kiwoom.Get_Opw00018()
            self.Print_tableWidget()
            self.Print_tableWidget2()

    def Handle_pushButton(self) :
        self.kiwoom.Get_Opw00001()
        self.kiwoom.Get_Opw00018()
        self.Print_tableWidget()
        self.Print_tableWidget2()

    def Print_tableWidget(self) :
        # 예수금 ~ 예수금(D+2)
        for i in range(len(self.kiwoom.opw00001)) : 
            item = QTableWidgetItem(self.kiwoom.opw00001[i])
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.tableWidget.setItem(0, i, item)

        # 총매입금액 | 총평가금액 | 총평가손익금액 | 총수익률(%) | 추정자산
        for i in range(2, 7) :
            item = QTableWidgetItem(self.kiwoom.opw00018['accountData'][i - 2])
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.tableWidget.setItem(0, i, item)
        self.tableWidget.resizeRowsToContents()

    def Print_tableWidget2(self) :
        # 종목명 | 평가손익 | 수익률(%) | 매입가 | 보유수량 | 매매가능수량 | 현재가
        cnt = len(self.kiwoom.opw00018['buyStockData'])
        self.tableWidget_2.setRowCount(cnt)
        for i in range(cnt) :
            row = self.kiwoom.opw00018['buyStockData'][i]
            for j in range(1, len(row)) :
                item = QTableWidgetItem(row[j])
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.tableWidget_2.setItem(i, j-1, item)
        self.tableWidget_2.resizeRowsToContents()


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
