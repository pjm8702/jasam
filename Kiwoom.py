import sys
import time
#import sqlite3
import pandas as pd
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

TQ_REQ_TIME_INTERVAL = 0.2
MARKET_KOSPI = 0
MARKET_KOSDAQ = 10


class Kiwoom(QAxWidget) :
    # Constructor
    def __init__(self) :
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

        self.passwd = ''  # 비밀번호
        self.accountCnt = ''  # 계좌개수
        self.accNo = ''  # 계좌번호
        self.userId = ''  # 사용자ID
        self.userName = ''  # 사용자이름
        self.keybSecurity = ''  # 키보드보안
        self.firewallSet = ''  # 방화벽설정
        self.marketKospi = ''  # KOSPI 종목코드/이름 정보
        self.marketKosdaq = '' # KOSDAQ 종목코드/이름 정보
        self.opw00001 = []  # 예수금, D+2추정에수금
        self.today = ''
        self.yesterday = ''
        # accountData : 총매입금액, 총평가금액, 총평가손익금액, 총수익률, 추정자산
        # buyStockData : 종목코드, 종목명, 평가손익, 수익률, 매입가, 보유수량, 매매가능수량, 현재가
        self.opw00018 = {'accountData' : [], 'buyStockData' : []}
        self.opt10081 = {'date' : [], 'open' : [], 'high' : [], 'low' : [], 'close' : [], 'volume' : []}    # 일자, 시가, 고가, 저가, 현재가, 거래량

    @staticmethod
    def change_format1(data) :
        stripData = data.lstrip('-0')
        if stripData == '' or stripData == '.00' :
            stripData = 0
        
        try :
            formatData = format(int(stripData), ',d')
        except :
            formatData = format(int(stripData))
        
        if data.startswith('-') :
            foramtData = '-' + formatData
        
        return formatData
    
    @staticmethod
    def change_format2(data) :
        stripData = data.lstrip('0')
        if stripData == '' :
            stripData = 0

        if stripData.startswith('.') :
            stripData = '0' + stripData
        
        if data.startswith('-') :
            foramtData = '-' + stripData
        
        return stripData
    
    def _create_kiwoom_instance(self) :
        self.setControl("KHOPENAPI.KHOPenAPICtrl.1")

    def _set_signal_slots(self) :
        self.OnEventConnect.connect(self.Handle_Event_Connect)
        self.OnReceiveTrData.connect(self.Handle_Event_TrData)

    def _set_input_value(self, id, value) :
        self.dynamicCall("SetInputValue(QString, QStirng)", id, value)

    def _comm_rq_data(self, rqName, trCode, prevNext, screenNo) :
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqName, trCode, prevNext, screenNo)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _get_repeat_cnt(self, trCode, rqName) :
        return self.dynamicCall("GetRepeatCnt(QString, QString)", trCode, rqName)
    
    def _get_comm_data(self, code, recordName, index, itemName) :
        ret = self.dynamicCall("GetCommData(QString, QString, int, QString)", code, recordName, index, itemName)
        return ret.strip()

    def Comm_Connect(self) :
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def Handle_Event_Connect(self, errCode) :
        if errCode < 0 :
            print(">> Login fail.")
        else :
            print(">> Login Success.")
            self.passwd = input(">> Input password : ")
        self.login_event_loop.exit()
    
    def Handle_Event_TrData(self, screenNo, rqName, trCode, recordName, preNext, unused1, unused2, unused3, unused4) :
        if preNext == '2' :
            self.remained_data = True
        else :
            self.remained_data = False
        
        if rqName == '예수금상세현황요청' :
            self.Handle_Opw00001(rqName, trCode)
        elif rqName == '계좌평가잔고내역요청' :
            self.Handle_Opw00018(rqName, trCode)
        elif rqName == '주식일봉차트조회요청' :
            self.Handle_Opt10081(rqName, trCode)
            
        try :
            self.tr_event_loop.exit()
        except AttributeError :
            pass
    
    def Get_ConnectState(self) :
        return self.dynamicCall("GetConnectState()")

    # 로그인 정보 처리
    # ACCOUNT_CNT : 전체 계좌 개수, ACCNO : 전체 계좌, USER_ID : 사용자 ID, USER_NAME : 사용자 이름, KEY_BSECGB : 키보드보안 해지 여부, FIREW_SECGB : 방화벽 설정 여부
    def Get_LoginInfo(self):
        self.accountCnt = self.dynamicCall("GetLoginInfo(QString)", "ACCOUNT_CNT")
        self.accNo = self.dynamicCall("GetLoginInfo(QString)", "ACCNO")
        self.accNo = self.accNo.split(';')
        self.userId = self.dynamicCall("GetLoginInfo(QString)", "USER_ID")
        self.userName = self.dynamicCall("GetLoginInfo(QString)", "USER_NAME")
        self.keybSecurity = self.dynamicCall("GetLoginInfo(QString)", "KEY_BSECGB")
        self.firewallSet = self.dynamicCall("GetLoginInfo(QString)", "FIREW_SECGB")

        print(">> 계좌개수 : " + self.accountCnt)
        print(">> 계좌번호 : " + self.accNo[0])
        print(">> 사용자ID : " + self.userId)
        print(">> 사용자이름 : " + self.userName)

        if self.keybSecurity == '0' :
            print(">> 키보드보안 : 정상")
        else :
            print(">> 키보드보안 : 해지")

        if self.firewallSet == '0' :
            print(">> 방화벽설정 : 미설정")
        elif self.firewallSet == '1' :
            print(">> 방화벽설정 : 설정")
        else :
            print(">> 방화벽설정 : 해지")
    
    # 전체 종목 코드, 종목명 리스트 생성
    def Get_AllCodeName(self, market) :
        codeList = self.dynamicCall("GetCodeListByMarket(QString)", str(market))
        codeList = codeList.split(';')[:-1]
        nameList = []
        for code in codeList :
            name = self.dynamicCall("GetMasterCodeName(QString)", code)
            nameList.append(name)
        if market == 0 :
            self.marketKospi = pd.DataFrame({'종목코드' : codeList, '종목명' : nameList})
            self.marketKospi.to_csv("Market_Kospi.csv", index=False, encoding="UTF-8")
            print(">> Market_Kospi.csv is made")
        else :
            self.marketKosdaq = pd.DataFrame({'종목코드' : codeList, '종목명' : nameList})
            self.marketKosdaq.to_csv("Market_Kosdaq.csv", index=False, encoding="UTF-8")
            print(">> Market_Kosdaq.csv is made")

    # Opw00001 예수금상세현황요청
    def Get_Opw00001(self) :
        self._set_input_value("계좌번호", self.accNo[0])
        self._set_input_value("비밀번호", str(self.passwd))
        self._set_input_value("비밀번호입력매체구분", "00")
        self._set_input_value("조회구분", "2")
        self._comm_rq_data("예수금상세현황요청", "opw00001", 0, "1000")

    # Opw0001 예수금상세현황요청 Event Handler
    def Handle_Opw00001(self, rqName, trCode) :
        tmp = self._get_comm_data(trCode, rqName, 0, "예수금")
        self.opw00001.append(Kiwoom.change_format1(tmp))
        tmp = self._get_comm_data(trCode, rqName, 0, "d+2추정예수금")
        self.opw00001.append(Kiwoom.change_format1(tmp))
        print(f">> 예수금 : {self.opw00001[0]}")
        print(f">> D+2 추정예수금 : {self.opw00001[1]}")
        
    # Opw00018 계좌평가잔고내역요청
    def Get_Opw00018(self) :
        self._set_input_value("계좌번호", self.accNo[0])
        self._set_input_value("비밀번호", str(self.passwd))
        self._set_input_value("비밀번호입력매체구분", "00")
        self._set_input_value("조회구분", "1")
        self._comm_rq_data("계좌평가잔고내역요청", "opw00018", 0, "1001")
        
        while self.remained_data == True :
            time.sleep(TQ_REQ_TIME_INTERVAL)
            self._set_input_value("계좌번호", self.accNo[0])
            self._set_input_value("비밀번호", str(self.passwd))
            self._set_input_value("비밀번호입력매체구분", "00")
            self._set_input_value("조회구분", "1")
            self._comm_rq_data("계좌평가잔고내역요청", "opw00018", 2, "1001")
    
    # Opw00018 계좌평가잔고내역요청 Event Handler
    def Handle_Opw00018(self, rqName, trCode) :
        self.opw00018['accountData'] = []
        self.opw00018['buyStockData'] = []

        tmp = self._get_comm_data(trCode, rqName, 0, "총매입금액")
        totBuyMoney = Kiwoom.change_format1(tmp)
        self.opw00018['accountData'].append(totBuyMoney)

        tmp = self._get_comm_data(trCode, rqName, 0, "총평가금액")
        totEstMoney = Kiwoom.change_format1(tmp)
        self.opw00018['accountData'].append(totEstMoney)

        tmp = self._get_comm_data(trCode, rqName, 0, "총평가손익금액")
        totGnLssMoney = Kiwoom.change_format1(tmp)
        self.opw00018['accountData'].append(totGnLssMoney)

        tmp = self._get_comm_data(trCode, rqName, 0, "총수익률(%)")
        totEarnRate = float(tmp) / 100.0
        self.opw00018['accountData'].append(str(totEarnRate))

        tmp = self._get_comm_data(trCode, rqName, 0, "추정예탁자산")
        estTotDeposit = Kiwoom.change_format1(tmp)
        self.opw00018['accountData'].append(estTotDeposit)

        print(">> 계좌정보 (총매입금액, 총평가금액, 총평가손익금액, 총수익률(%), 추정예착자산)")
        print(self.opw00018['accountData'])
        tmpDf = pd.DataFrame({'예수금' : [self.opw00001[0]], '예수금(D+2)' : [self.opw00001[1]], '총매입금액' : [self.opw00018['accountData'][0]], '총평가금액' : [self.opw00018['accountData'][1]], '총평가손익금액' : [self.opw00018['accountData'][2]], '총수익률' :[self.opw00018['accountData'][3]], '추정예탁자산' : [self.opw00018['accountData'][4]]})
        tmpDf.to_csv("AccountInfo.csv", index=False, encoding="UTF-8")
        print(">> AccountInfo.csv is made")

        cnt = self._get_repeat_cnt(trCode, rqName)
        tmpDf = pd.DataFrame({'종목번호' : [], '종목명' : [], '평가손익' : [], '수익률(%)' : [], '매입가' : [], '보유수량' : [], '매매가능수량' : [], '현재가' : []})
        for i in range(cnt) :
            no = self._get_comm_data(trCode, rqName, i, "종목번호")
            name = self._get_comm_data(trCode, rqName, i, "종목명")
            tmp = self._get_comm_data(trCode, rqName, i, "평가손익")
            gain = Kiwoom.change_format1(tmp)
            tmp = self._get_comm_data(trCode, rqName, i, "수익률(%)")
            tmp2 = float(tmp) / 100.0
            rate = Kiwoom.change_format2(str(tmp2))
            tmp = self._get_comm_data(trCode, rqName, i, "매입가")
            avgPrice = Kiwoom.change_format1(tmp)
            tmp = self._get_comm_data(trCode, rqName, i, "보유수량")
            count = Kiwoom.change_format1(tmp)
            tmp = self._get_comm_data(trCode, rqName, i, "매매가능수량")
            sellCount = Kiwoom.change_format1(tmp)
            tmp = self._get_comm_data(trCode, rqName, i, "현재가")
            curPrice = Kiwoom.change_format1(tmp)
            
            self.opw00018['buyStockData'].append([no, name, gain, rate, avgPrice, count, sellCount, curPrice])
            tmpDf = tmpDf.append({'종목번호' : no, '종목명' : name, '평가손익' : gain, '수익률(%)' : rate, '매입가' : avgPrice, '보유수량' : count, '매매가능수량' : sellCount, '현재가' : curPrice}, ignore_index=True)
        print(">> 보유주식정보 (종목번호, 종목명, 평가손익, 수익률(%), 매입가, 보유수량, 매매가능수량, 현재가)")
        print(self.opw00018['buyStockData'])
        tmpDf.to_csv("MyStockInfo.csv", index=False, encoding="UTF-8")
        print(">> MyStockInfo.csv is made")
    
    def Get_Opt10081(self, stockCode, date) :
        self._set_input_value("종목코드", stockCode)
        self._set_input_value("기준일자", date)
        self._set_input_value("수정주가구분", 1)
        self._set_input_value("조회구분", "1")
        self._comm_rq_data("주식일봉차트조회요청", "opt10081", 0, "1002")

        while self.remained_data == True :
            time.sleep(TQ_REQ_TIME_INTERVAL)
            self._set_input_value("종목코드", stockCode)
            self._set_input_value("기준일자", date)
            self._set_input_value("수정주가구분", 1)
            self._set_input_value("조회구분", "1")
            self._comm_rq_data("주식일봉차트조회요청", "opt10081", 2, "1002")

    def Handle_Opt10081(self, rqName, trCode) :
        cnt = self._get_repeat_cnt(trCode, rqName)
        for i in range(cnt) :
            date = self._get_comm_data(trCode, rqName, i, "일자")
            open = self._get_comm_data(trCode, rqName, i, "시가")
            high = self._get_comm_data(trCode, rqName, i, "고가")
            low = self._get_comm_data(trCode, rqName, i, "저가")
            close = self._get_comm_data(trCode, rqName, i, "현재가")
            volume = self._get_comm_data(trCode, rqName, i, "거래량")
            
            self.opt10081['date'].append(date)
            self.opt10081['open'].append(open)
            self.opt10081['high'].append(high)
            self.opt10081['low'].append(low)
            self.opt10081['close'].append(close)
            self.opt10081['volume'].append(volume)

    def Clear_Opt10081(self) :
        self.opt10081['date'].clear()
        self.opt10081['open'].clear()
        self.opt10081['high'].clear()
        self.opt10081['low'].clear()
        self.opt10081['close'].clear()
        self.opt10081['volume'].clear()

    def Print_Opt10081(self, idx) :
        csvFileName = str(self.opw00018['buyStockData'][idx][0]) + '_' + str(self.opw00018['buyStockData'][idx][1]) + str('_Info.csv')
        tmpDf = pd.DataFrame({'일자' : self.opt10081['date'], '시가' : self.opt10081['open'], '고가' : self.opt10081['high'], '저가' : self.opt10081['low'], '현재가' : self.opt10081['close'], '거래량' : self.opt10081['volume']})
        tmpDf.to_csv(csvFileName, index=False, encoding="UTF-8")
        print('>> ' + csvFileName + ' is made')

    def Make_StrDate(self) :
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(1)
        self.today = (str(self.today)).replace("-", "")
        self.yesterday = (str(self.yesterday)).replace("-", "")

# Main
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()

    kiwoom.Comm_Connect()
    kiwoom.Get_LoginInfo()
    kiwoom.Get_AllCodeName(MARKET_KOSPI)
    kiwoom.Get_AllCodeName(MARKET_KOSDAQ)
    kiwoom.Get_Opw00001()
    kiwoom.Get_Opw00018()

    kiwoom.Make_StrDate()
    for i in range(len(kiwoom.opw00018['buyStockData'])) :     
        code = str(kiwoom.opw00018['buyStockData'][i][0]).replace("A", "")
        kiwoom.Get_Opt10081(code, kiwoom.yesterday)
        kiwoom.Print_Opt10081(i)
        kiwoom.Clear_Opt10081()

    # 총평가손익금액, 평가손익 정보 마이너스값이 안나옴
    # 보유주식정보로 만들어낼 정보와 이론? 카톡으로 메시지 보내는 기능 구현 필요