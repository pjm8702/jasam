import sys
from Kakao import *
from Kiwoom import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

TIMER2_INTERVAL = 1000*300   # 잔고 및 보유종목현황 실시간 인터벌
TIMER3_INTERVAL = 1000*300   # 보유종목 등락 실시간 인터벌

# Qt Designer UI 파일
form_class = uic.loadUiType("MyTrader.ui")[0]

class MyWindow(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.lineEditStartDate = ''
        self.lineEdit_2EndDate = ''

        # 매일 오전 실행 시 카톡 메시지 전송을 위해 토큰 Get
        curTime = MyWindow.Get_CurTimeInt()
        #if curTime >= 70000 and curTime <= 90000 :
        #    Kakao.Get_KakaoToken()

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
        self.timer2.start(TIMER2_INTERVAL)
        self.timer2.timeout.connect(self.Handle_Timeout2)

        # 보유종목 등락 조회 버튼 이벤트 설정
        self.pushButton_2.clicked.connect(self.Handle_pushButton2)

        # 보유종목 실시간 등락 조회 클릭 이벤트 설정
        self.timer3 = QTimer(self)
        self.timer3.start(TIMER3_INTERVAL)
        self.timer3.timeout.connect(self.Handle_Timeout3)

        # 종목 조회 버튼 이벤트 설정
        self.pushButton_3.clicked.connect(self.Handle_pushButton3)
        
        # 종목 조회 라디오 버튼 이벤트 설정
        self.radioButton.setChecked(True)
        self.market = self.kiwoom.MARKET_KOSPI
        self.radioButton.clicked.connect(self.Handle_radioButton1n2)
        self.radioButton_2.clicked.connect(self.Handle_radioButton1n2)

        # 실현손익 조회 버튼 이벤트 설정
        self.pushButton_4.clicked.connect(self.Handle_pushButton4)

        # 실현손익 조회 시작/종료 날짜 설정
        self.lineEdit.setText("20160101")
        self.lineEditStartDate = self.lineEdit.text()
        self.lineEdit.textChanged.connect(self.Handle_lineEdit1n2)
        self.lineEdit_2.setText(self.kiwoom.today)
        self.lineEdit_2.textChanged.connect(self.Handle_lineEdit1n2)
        self.lineEdit_2EndDate = self.lineEdit_2.text()

        # 보유종목 일봉차트 자료 조회
        self.pushButton_5.clicked.connect(self.Handle_pushButton5)

    @staticmethod
    def Get_CurTimeInt() :
        curTime = QTime.currentTime()
        curTime = int(curTime.toString("hhmmss"))
        return curTime
        
    # 계좌비밀번호 입력 다이얼로그 출력
    def Print_PasswdDialog(self) :
        if self.kiwoom.passwd == None :
            passwd, ok = QInputDialog.getText(self, "비밀번호 입력", "계좌 비밀번호를 입력하세요.")
            if ok :
                self.kiwoom.passwd = passwd
            else :
                self.kiwoom.passwd = None

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
            self.Print_PasswdDialog()
            self.Print_TableWidget1n2()

    # 잔고 및 보유종목현황 실시간 조회 버튼 이벤트 처리
    def Handle_pushButton(self) :
        self.Print_PasswdDialog()
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
            item = QTableWidgetItem(self.kiwoom.opw00018['single'][i - 1])
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.tableWidget.setItem(0, i, item)
        self.tableWidget.resizeRowsToContents()
        #self.tableWidget.resizeColumnsToContents()

    # 보유종목현황 출력
    def Print_tableWidget2(self) :
        # 종목코드 | 종목명 | 매입가 | 평가손익 | 수익률(%) | 보유수량 | 매매가능수량 | 현재가
        cntRow = len(self.kiwoom.opw00018['multi'])
        cntCol = len(self.kiwoom.opw00018['multi'][0])
        self.tableWidget_2.setRowCount(cntRow)
        self.tableWidget_2.setColumnCount(cntCol)
        for i in range(cntRow) :
            row = self.kiwoom.opw00018['multi'][i]
            for j in range(cntCol) :
                item = QTableWidgetItem(row[j])
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.tableWidget_2.setItem(i, j, item)
        self.tableWidget_2.resizeRowsToContents()
        #self.tableWidget_2.resizeColumnsToContents()

    # 보유종목 등락 실시간 조회 이벤트 timeout
    def Handle_Timeout3(self) :
        curTime = MyWindow.Get_CurTimeInt()
        if self.checkBox_2.isChecked() and curTime >= 90000 and curTime <= 153000 :
            self.Print_TextBrowser_2()

    # 보유종목 등락 실시간 조회 버튼 클릭 이벤트 처리
    def Handle_pushButton2(self) :
        self.Print_TextBrowser_2()

    # 보유종목 등락 출력
    def Print_TextBrowser_2(self) :
        if len(self.kiwoom.opw00018['multi']) == 0 :
            self.kiwoom.Get_Opw00001()
            self.kiwoom.Get_Opw00018()

        self.textBrowser_2.clear()
        msg = ''
        for i in range(len(self.kiwoom.opw00018['multi'])) :
            code = str(self.kiwoom.opw00018['multi'][i][0])
            name = str(self.kiwoom.opw00018['multi'][i][1])
            self.kiwoom.Get_Opt10001(code)
            gap = self.kiwoom.opt10001[i][10]
            self.textBrowser_2.append(str(i + 1) + ". " + name + "(%) : " + gap)

            if float(gap) >= 3.0 or float(gap) <= -3.0 :
                msg = msg + name + ':' + gap + '%\n'

        if msg != '' :
            Kakao.Send_KakaoMessage(msg)


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
        self.tableWidget_3.setColumnCount(self.kiwoom.marketKospi.shape[1])
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

    # 실현손익 조회 버튼 클릭 이벤트 처리
    def Handle_pushButton4(self) :
        if int(self.lineEdit_2EndDate) - int(self.lineEditStartDate) >= 0 :
            self.kiwoom.Get_Opt10074(self.lineEditStartDate, self.lineEdit_2EndDate)
            self.tableWidget_4.setRowCount(1)
            self.tableWidget_4.setColumnCount(len(self.kiwoom.opt10074['single']))
            for i in range(len(self.kiwoom.opt10074['single'])) : 
                item = QTableWidgetItem(self.kiwoom.opt10074['single'][i])
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.tableWidget_4.setItem(0, i, item)
            self.tableWidget_4.resizeRowsToContents()
            
            cntCol = len(self.kiwoom.opt10074['multi'])
            cntRow = len(self.kiwoom.opt10074['multi'][0])
            self.tableWidget_5.setRowCount(cntCol)
            self.tableWidget_5.setColumnCount(cntRow)
            for i in range(cntCol) :
                row = self.kiwoom.opt10074['multi'][i]
                for j in range(cntRow) :
                    item = QTableWidgetItem(row[j])
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    self.tableWidget_5.setItem(i, j, item)
            self.tableWidget_5.resizeRowsToContents()

    # 실현손익 조회를 위한 날짜 처리
    def Handle_lineEdit1n2(self) :
        self.lineEditStartDate = self.lineEdit.text()
        self.lineEdit_2EndDate = self.lineEdit_2.text()

    # 보유주식 일봉차트 자료 조회 버튼 클릭 이벤트 처리
    def Handle_pushButton5(self) :
        if len(self.kiwoom.opw00018['multi']) == 0 :
            self.kiwoom.Get_Opw00001()
            self.kiwoom.Get_Opw00018()

        bar = 0
        self.progressBar.setValue(bar)
        upStep = self.progressBar.maximum() / len(self.kiwoom.opw00018['multi'])
        for i in range(len(self.kiwoom.opw00018['multi'])) :     
            code = self.kiwoom.opw00018['multi'][i][0]
            self.kiwoom.Get_Opt10081(code, self.kiwoom.today, self.kiwoom.MULTI_ALL)
            self.kiwoom.Print_Opt10081(i)
            self.kiwoom.Clear_Opt10081()
            bar = bar + upStep
            self.progressBar.setValue(bar)
        
        tmp, ok = QInputDialog.getText(self, "보유주식 일봉차트 자료 조회", "완료...csv 파일을 확인하세요.")


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
