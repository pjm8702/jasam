import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Kiwoom import *

# Qt Designer UI 파일
form_class = uic.loadUiType("MyTrader.ui")[0]

class MyWindow(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.kiwoom = Kiwoom()
        self.kiwoom.Comm_Connect()  # 키움 접속
        self.kiwoom.Get_LoginInfo() # 로그인 정보 Get
        self.kiwoom.Make_StrDate()  # 오늘, 어제 날짜 처리
        
        # 접속정보 출력
        self.Print_TextBrowser()

        # Status Bar Timer Event 설정
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.Handle_Timeout)

        # 잔고 및 보유종목현황 조회 버튼 이벤트 설정
        self.pushButton.clicked.connect(self.Handle_pushButton)

        # 잔고 및 보유종목현황 실시간 조회 이벤트 설정
        self.timer2 = QTimer(self)
        self.timer2.start(1000*5)
        self.timer2.timeout.connect(self.Handle_Timeout2)

        # 보유종목 상승/하강률 조회 버튼 이벤트 설정
        self.pushButton_2.clicked.connect(self.Handle_pushButton2)

        # 보유종목 실시간 상승/하강률 조회 클릭 이벤트 설정
        self.timer3 = QTimer(self)
        self.timer3.start(1000*5)
        self.timer3.timeout.connect(self.Handle_Timeout3)

        # 종목 조회 버튼 이벤트 설정
        self.pushButton_3.clicked.connect(self.Handle_pushButton3)
        
        # 종목 조회 라디오 버튼 이벤트 설정
        self.radioButton.setChecked(True)
        self.market = self.kiwoom.MARKET_KOSPI
        self.radioButton.clicked.connect(self.Handle_radioButton1n2)
        self.radioButton_2.clicked.connect(self.Handle_radioButton1n2)

    # 접속정보 출력
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

    # 창 하단 Status Bar 시간 출력 Timeout
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

    # 잔고 및 보유종목현황 실시간 조회 이벤트 Timeout
    def Handle_Timeout2(self) :
        if self.checkBox.isChecked() :
            self.Print_TableWidget1n2()

    # 잔고 및 보유종목현황 실시간 조회 버튼 이벤트 처리
    def Handle_pushButton(self) :
        self.Print_TableWidget1n2()

    # 잔고 및 보유종목현황 출력
    def Print_TableWidget1n2(self) :
        self.kiwoom.Get_Opw00001()
        self.kiwoom.Get_Opw00018()
        self.Print_tableWidget()
        self.Print_tableWidget2()

    # 잔고 출력
    def Print_tableWidget(self) :
        # 예수금
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(6)
        for i in range(len(self.kiwoom.opw00001)) : 
            item = QTableWidgetItem(self.kiwoom.opw00001[i])
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.tableWidget.setItem(0, i, item)

        # 총매입금액 | 총평가금액 | 총평가손익금액 | 총수익률(%) | 추정자산
        for i in range(1, 6) :
            item = QTableWidgetItem(self.kiwoom.opw00018['accountData'][i - 1])
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.tableWidget.setItem(0, i, item)
        self.tableWidget.resizeRowsToContents()
        #self.tableWidget.resizeColumnsToContents()

    # 보유종목현황 출력
    def Print_tableWidget2(self) :
        # 종목코드 | 종목명 | 매입가 | 평가손익 | 수익률(%) | 보유수량 | 매매가능수량 | 현재가
        cnt = len(self.kiwoom.opw00018['buyStockData'])
        self.tableWidget_2.setRowCount(cnt)
        self.tableWidget_2.setColumnCount(8)
        for i in range(cnt) :
            row = self.kiwoom.opw00018['buyStockData'][i]
            for j in range(0, len(row)) :
                item = QTableWidgetItem(row[j])
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.tableWidget_2.setItem(i, j, item)
        self.tableWidget_2.resizeRowsToContents()
        #self.tableWidget_2.resizeColumnsToContents()

    # 보유종목 상승/하강률 실시간 조회 이벤트 timeout
    def Handle_Timeout3(self) :
        if self.checkBox_2.isChecked() :
            self.Print_TextBrowser_2()

    # 보유종목 상승/하강률 실시간 조회 버튼 클릭 이벤트 처리
    def Handle_pushButton2(self) :
        self.Print_TextBrowser_2()

    # 보유종목 상승/하강률 출력
    def Print_TextBrowser_2(self) :
        self.textBrowser_2.clear()
        for i in range(len(self.kiwoom.opw00018['buyStockData'])) :     
            code = str(self.kiwoom.opw00018['buyStockData'][i][0]).replace("A", "")
            #self.kiwoom.Get_Opt10081(code, kiwoom.yesterday, self.kiwoom.STOCK_DATA_ALL)
            self.kiwoom.Get_Opt10081(code, self.kiwoom.today, self.kiwoom.STOCK_DATA_ONLY)
            gap = self.kiwoom.Calc_UpDownRateToday(i)
            #self.kiwoom.Print_Opt10081(i)
            self.kiwoom.Clear_Opt10081()
            self.textBrowser_2.append(">> " + str(self.kiwoom.opw00018['buyStockData'][i][1]) + " 상승/하강률(%) : " + str(gap))      

    # 종목 조회 버튼 클릭 이벤트 처리
    def Handle_pushButton3(self) :
        self.kiwoom.Get_AllCodeName(self.market)
        self.Print_TableWideg3(self.market)

    # 종목 조회 라디오 버튼 클릭 이벤트 처리
    def Handle_radioButton1n2(self) :
        if self.radioButton.isChecked() :
            self.market = self.kiwoom.MARKET_KOSPI
        elif self.radioButton_2.isChecked() :
            self.market = self.kiwoom.MARKET_KOSDAQ

    # 코스피 or 코스닥 전체 종목정보 출력
    def Print_TableWideg3(self, market) :
        if market == self.kiwoom.MARKET_KOSPI :
            cnt = len(self.kiwoom.marketKospi['code'])
        elif market == self.kiwoom.MARKET_KOSDAQ :
            cnt = len(self.kiwoom.marketKosdaq['code'])
                
        self.tableWidget_3.setRowCount(cnt)
        self.tableWidget_3.setColumnCount(2)
        for i in range(cnt) :
            if market == self.kiwoom.MARKET_KOSPI :
                code = self.kiwoom.marketKospi['code'][i]
                name = self.kiwoom.marketKospi['name'][i]
            elif market == self.kiwoom.MARKET_KOSDAQ :
                code = self.kiwoom.marketKosdaq['code'][i]
                name = self.kiwoom.marketKosdaq['name'][i]
            item1 = QTableWidgetItem(code)
            item1.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.tableWidget_3.setItem(i, 0, item1)
            item2 = QTableWidgetItem(name)
            item2.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.tableWidget_3.setItem(i, 1, item2)
        self.tableWidget_3.resizeRowsToContents()
        #self.tableWidget_3.resizeColumnsToContents()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
