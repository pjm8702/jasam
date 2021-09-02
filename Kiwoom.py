import sys
import time
#import sqlite3
import pandas as pd
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *


class Kiwoom(QAxWidget) :
    # Constructor
    def __init__(self) :
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

        self.TQ_REQ_TIME_INTERVAL = 0.2 # 요청 주기
        self.STOCK_DATA_ALL = 0 # 전체 데이터 요청
        self.STOCK_DATA_ONLY = 1    # 1회 데이터 요청
        self.MARKET_KOSPI = 0   # 코스피
        self.MARKET_KOSDAQ = 10 # 코스닥

        self.passwd = None  # 비밀번호
        self.accountCnt = ''  # 계좌개수
        self.accNo = ''  # 계좌번호
        self.userId = ''  # 사용자ID
        self.userName = ''  # 사용자이름
        self.keybSecurity = ''  # 키보드보안
        self.firewallSet = ''  # 방화벽설정
        self.marketKospi = ''  # KOSPI 종목코드/이름 정보
        self.marketKosdaq = '' # KOSDAQ 종목코드/이름 정보
        self.today = ''
        self.yesterday = ''
        self.opw00001 = []  # 예수금
        # single : 총매입금액, 총평가금액, 총평가손익금액, 총수익률, 추정자산
        # multi : 종목코드, 종목명, 평가손익, 수익률, 매입가, 보유수량, 매매가능수량, 현재가 
        self.opw00018 = {'single' : [], 'multi' : []}
        self.opt10081 = {'date' : [], 'open' : [], 'high' : [], 'low' : [], 'close' : [], 'volume' : []}    # 일자, 시가, 고가, 저가, 현재가, 거래량
        # single : 총매수금액, 총매도금액, 실현손익, 매매수수료, 매매세금
        # multi : 일자, 매수금액, 매도금액, 당일매도손익, 당일매매수수료, 당일매매세금
        self.opt10074 = {'single' : [], 'multi' : []}

    @staticmethod   # 금액 정보 타입 처리
    def change_format1(data) :
        stripData = data.lstrip('-0')
        if stripData == '' or stripData == '.00' :
            stripData = 0
        
        try :
            formatData = format(int(stripData), ',d')
        except :
            formatData = format(int(stripData))
        
        if data.startswith('-') :
            formatData = '-' + formatData
        
        return formatData
    
    @staticmethod   # 수익률 정보 타입 처리
    def change_format2(data) :
        stripData = data.lstrip('-0')

        if stripData == '' :
            stripData = 0

        if stripData.startswith('.') :
            stripData = '0' + stripData
        
        if data.startswith('-') :
            stripData = '-' + stripData
        
        return stripData
    
    # 키움 API 연결
    def _create_kiwoom_instance(self) :
        self.setControl("KHOPENAPI.KHOPenAPICtrl.1")

    # 키움 이벤트 핸들러 연결
    def _set_signal_slots(self) :
        self.OnEventConnect.connect(self.Handle_Event_Connect)
        self.OnReceiveTrData.connect(self.Handle_Event_TrData)

    # 키움 Rq 요청을 위한 입력값 설정
    def _set_input_value(self, id, value) :
        self.dynamicCall("SetInputValue(QString, QStirng)", id, value)

    # 키움 Rq 데이터 요청
    def _comm_rq_data(self, rqName, trCode, prevNext, screenNo) :
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqName, trCode, prevNext, screenNo)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    # 키움 Rq 데이터 반복 횟수
    def _get_repeat_cnt(self, trCode, rqName) :
        return self.dynamicCall("GetRepeatCnt(QString, QString)", trCode, rqName)
    
    # 키움 Rq 데이터 획득
    def _get_comm_data(self, trCode, rqName, idx, itemName) :
        ret = self.dynamicCall("GetCommData(QString, QString, int, QString)", trCode, rqName, idx, itemName)
        return ret.strip()

    # 키움 서버 접속
    def Comm_Connect(self) :
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    # 키움 서버 접속 이벤트 처리
    def Handle_Event_Connect(self, errCode) :
        if errCode < 0 :
            print(">> Login fail.")
        else :
            print(">> Login Success.")
            if __name__ == "__main__" :
                self.passwd = input(">> Input password : ")
        self.login_event_loop.exit()
    
    # 키움 Rq 데이터 이벤트 처리
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
        elif rqName == '일자별실현손익요청' :
            print("왜 동작안해....")
            self.Handle_Opt10074(rqName, trCode)    # TODO
            
        try :
            self.tr_event_loop.exit()
        except AttributeError :
            pass
    
    # 키움 서버 연결 상태 획득
    def Get_ConnectState(self) :
        return self.dynamicCall("GetConnectState()")

    # 로그인 정보 처리(ACCOUNT_CNT : 전체 계좌 개수, ACCNO : 전체 계좌, USER_ID : 사용자 ID, USER_NAME : 사용자 이름, KEY_BSECGB : 키보드보안 해지 여부, FIREW_SECGB : 방화벽 설정 여부)
    def Get_LoginInfo(self):
        self.accountCnt = self.dynamicCall("GetLoginInfo(QString)", "ACCOUNT_CNT")
        self.accNo = self.dynamicCall("GetLoginInfo(QString)", "ACCNO")
        self.accNo = self.accNo.split(';')
        self.userId = self.dynamicCall("GetLoginInfo(QString)", "USER_ID")
        self.userName = self.dynamicCall("GetLoginInfo(QString)", "USER_NAME")
        self.keybSecurity = self.dynamicCall("GetLoginInfo(QString)", "KEY_BSECGB")
        self.firewallSet = self.dynamicCall("GetLoginInfo(QString)", "FIREW_SECGB")

        if __name__ == "__main__" :
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
            self.marketKospi = pd.DataFrame({'code' : codeList, 'name' : nameList})
            if __name__ == "__main__" :
                self.marketKospi.to_csv("Market_Kospi.csv", index=False, encoding="UTF-8")
                print(">> Market_Kospi.csv is made")
        else :
            self.marketKosdaq = pd.DataFrame({'code' : codeList, 'name' : nameList})
            if __name__ == "__main__" :
                self.marketKosdaq.to_csv("Market_Kosdaq.csv", index=False, encoding="UTF-8")
                print(">> Market_Kosdaq.csv is made")

    # Opw00001 예수금상세현황요청
    def Get_Opw00001(self) :
        self._set_input_value("계좌번호", self.accNo[0])
        self._set_input_value("비밀번호", str(self.passwd))
        self._set_input_value("비밀번호입력매체구분", "00")
        self._set_input_value("조회구분", "2")
        self._comm_rq_data("예수금상세현황요청", "opw00001", 0, "1000")

    # Opw0001 예수금상세현황요청 Rq 데이터 이벤트 처리
    def Handle_Opw00001(self, rqName, trCode) :
        tmp = self._get_comm_data(trCode, rqName, 0, "예수금")
        self.opw00001.append(Kiwoom.change_format1(tmp))
        
        if __name__ == "__main__" :
            print(f">> 예수금 : {self.opw00001[0]}")
        
    # Opw00018 계좌평가잔고내역요청
    def Get_Opw00018(self) :
        self._set_input_value("계좌번호", self.accNo[0])
        self._set_input_value("비밀번호", str(self.passwd))
        self._set_input_value("비밀번호입력매체구분", "00")
        self._set_input_value("조회구분", "1")
        self._comm_rq_data("계좌평가잔고내역요청", "opw00018", 0, "1001")
        
        while self.remained_data == True :
            time.sleep(self.TQ_REQ_TIME_INTERVAL)
            self._set_input_value("계좌번호", self.accNo[0])
            self._set_input_value("비밀번호", str(self.passwd))
            self._set_input_value("비밀번호입력매체구분", "00")
            self._set_input_value("조회구분", "1")
            self._comm_rq_data("계좌평가잔고내역요청", "opw00018", 2, "1001")
    
    # Opw00018 계좌평가잔고내역요청 Rq 데이터 이벤트 처리
    def Handle_Opw00018(self, rqName, trCode) :
        self.opw00018['single'] = []
        self.opw00018['multi'] = []

        tmp = self._get_comm_data(trCode, rqName, 0, "총매입금액")
        totBuyMoney = Kiwoom.change_format1(tmp)
        self.opw00018['single'].append(totBuyMoney)

        tmp = self._get_comm_data(trCode, rqName, 0, "총평가금액")
        totEstMoney = Kiwoom.change_format1(tmp)
        self.opw00018['single'].append(totEstMoney)

        tmp = self._get_comm_data(trCode, rqName, 0, "총평가손익금액")
        totGnLssMoney = Kiwoom.change_format1(tmp)
        self.opw00018['single'].append(totGnLssMoney)

        tmp = self._get_comm_data(trCode, rqName, 0, "총수익률(%)")
        totEarnRate = float(tmp) / 100.0
        self.opw00018['single'].append(str(totEarnRate))

        tmp = self._get_comm_data(trCode, rqName, 0, "추정예탁자산")
        estTotDeposit = Kiwoom.change_format1(tmp)
        self.opw00018['single'].append(estTotDeposit)

        if __name__ == "__main__" :
            print(">> 계좌정보 (총매입금액, 총평가금액, 총평가손익금액, 총수익률(%), 추정예착자산)")
            print(self.opw00018['single'])
            tmpDf = pd.DataFrame({'예수금' : [self.opw00001[0]], '총매입금액' : [self.opw00018['single'][0]], '총평가금액' : [self.opw00018['single'][1]], '총평가손익금액' : [self.opw00018['single'][2]], '총수익률' :[self.opw00018['single'][3]], '추정예탁자산' : [self.opw00018['single'][4]]})
            tmpDf.to_csv("AccountInfo.csv", index=False, encoding="UTF-8")
            print(">> AccountInfo.csv is made")

        tmpDf = pd.DataFrame({'종목번호' : [], '종목명' : [], '매입가' : [], '평가손익' : [], '수익률(%)' : [], '보유수량' : [], '매매가능수량' : [], '현재가' : []})
        cnt = self._get_repeat_cnt(trCode, rqName)
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
            
            self.opw00018['multi'].append([no, name, gain, rate, avgPrice, count, sellCount, curPrice])
            tmpDf = tmpDf.append({'종목번호' : no, '종목명' : name, '매입가' : avgPrice, '평가손익' : gain, '수익률(%)' : rate, '보유수량' : count, '매매가능수량' : sellCount, '현재가' : curPrice}, ignore_index=True)
            
        if __name__ == "__main__" :
            print(">> 보유주식정보 (종목번호, 종목명, 평가손익, 수익률(%), 매입가, 보유수량, 매매가능수량, 현재가)")
            print(self.opw00018['multi'])
            tmpDf.to_csv("MyStockInfo.csv", index=False, encoding="UTF-8")
            print(">> MyStockInfo.csv is made")
    
    # Opt10081 주식일봉차트조회요청
    def Get_Opt10081(self, code, date, type) :
        self._set_input_value("종목코드", code)
        self._set_input_value("기준일자", date)
        self._set_input_value("수정주가구분", 1)
        self._set_input_value("조회구분", "1")
        self._comm_rq_data("주식일봉차트조회요청", "opt10081", 0, "1002")

        while self.remained_data == True and type == self.STOCK_DATA_ALL :
            time.sleep(self.TQ_REQ_TIME_INTERVAL)
            self._set_input_value("종목코드", code)
            self._set_input_value("기준일자", date)
            self._set_input_value("수정주가구분", 1)
            self._set_input_value("조회구분", "1")
            self._comm_rq_data("주식일봉차트조회요청", "opt10081", 2, "1002")

    # Opt10081 주식일봉차트조회요청 Rq 데이터 이벤트 처리
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

    # Opt10081 주식일봉차트조회요청 Rq 데이터 삭제
    def Clear_Opt10081(self) :
        self.opt10081['date'].clear()
        self.opt10081['open'].clear()
        self.opt10081['high'].clear()
        self.opt10081['low'].clear()
        self.opt10081['close'].clear()
        self.opt10081['volume'].clear()

    # Opt10081 주식일봉차트조회요청 Rq 데이터 출력
    def Print_Opt10081(self, idx) :
        csvFileName = str(self.opw00018['multi'][idx][0]) + '_' + str(self.opw00018['multi'][idx][1]) + str('_Info.csv')
        tmpDf = pd.DataFrame({'일자' : self.opt10081['date'], '시가' : self.opt10081['open'], '고가' : self.opt10081['high'], '저가' : self.opt10081['low'], '현재가' : self.opt10081['close'], '거래량' : self.opt10081['volume']})
        tmpDf.to_csv(csvFileName, index=False, encoding="UTF-8")
        print('>> ' + csvFileName + ' is made')

    # 금일 시가 기준 상승/하강률 계산
    def Calc_UpDownRateToday(self, idx) :
        gap = ((int(self.opt10081['close'][0]) - int(self.opt10081['close'][1])) / int(self.opt10081['close'][1])) * 100.0
        gap = round(gap, 2)

        if __name__ == "__main__" :
            print(">> " + str(self.opw00018['multi'][idx][1]) + " 상승/하강률(%) : " + str(gap))
        
        return gap
    
    # 오늘, 어제 날짜 처리
    def Make_StrDate(self) :
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(1)
        self.today = (str(self.today)).replace("-", "")
        self.yesterday = (str(self.yesterday)).replace("-", "")

        if __name__ == "__main__" :
            print(self.yesterday)
            print(self.today)

    # Opt10074 일자별실현손익요청
    def Get_Opt10074(self) :
        self._set_input_value("계좌번호", self.accNo[0])
        self._set_input_value("시작일자", "20160101")
        self._set_input_value("종료일자", self.today)
        self._comm_rq_data("일자별실현손익요청", "opt10074", 0, "1003") #이벤트가 왜 안들어오지?

        print("11111111111111")
        while self.remained_data == True :
            time.sleep(self.TQ_REQ_TIME_INTERVAL)
            self._set_input_value("계좌번호", self.accNo[0])
            self._set_input_value("시작일자", "20160101")
            self._set_input_value("종료일자", self.today)
            self._comm_rq_data("일자별실현손익요청", "opt10074", 2, "1003")

    # Opt10074 일자별실현손익요청 Rq 데이터 이벤트 처리
    def Handle_Opt10074(self, rqName, trCode) :
        tmp = self._get_comm_data(trCode, rqName, 0, "총매수금액")
        totBuyCost = Kiwoom.change_format1(tmp)
        tmp = self._get_comm_data(trCode, rqName, 0, "총매도금액")
        totSellCost = Kiwoom.change_format1(tmp)
        tmp = self._get_comm_data(trCode, rqName, 0, "실현손익")
        profit = Kiwoom.change_format1(tmp)
        tmp = self._get_comm_data(trCode, rqName, 0, "매매수수료")
        sellCommission = Kiwoom.change_format1(tmp)
        tmp = self._get_comm_data(trCode, rqName, 0, "매매세금")
        sellTax = Kiwoom.change_format1(tmp)

        print("22222222222222")
        
        self.opt10074['single'].append(totBuyCost)
        self.opt10074['single'].append(totSellCost)
        self.opt10074['single'].append(profit)
        self.opt10074['single'].append(sellCommission)
        self.opt10074['single'].append(sellTax)

        if __name__ == "__main__" :
            print(">> 실현손익 (총매수금액, 총매도금액, 실현손익, 매매수수료, 매매세금)")
            print(self.opt10074['single'])
            tmpDf = pd.DataFrame({'총매수금액' : [self.opt10074[0]], '총매도금액' : [self.opt10074['single'][1]], '실현손익' : [self.opt10074['single'][2]], '매매수수료' : [self.opt10074['single'][3]], '매매세금' :[self.opt10074['single'][4]]})
            tmpDf.to_csv("RealProfit.csv", index=False, encoding="UTF-8")
            print(">> RealProfit.csv is made")

        tmpDf = pd.DataFrame({'일자' : [], '매수금액' : [], '매도금액' : [], '당일매도손익' : [], '당일매매수수료' :[], '당일매매세금' : []})
        cnt = self._get_repeat_cnt(trCode, rqName)
        for i in range(cnt) :
            date = self._get_comm_data(trCode, rqName, i, "일자")
            tmp = self._get_comm_data(trCode, rqName, i, "매수금액")
            buyCost = Kiwoom.change_format1(tmp)
            tmp = self._get_comm_data(trCode, rqName, i, "매도금액")
            sellCost = Kiwoom.change_format1(tmp)
            tmp = self._get_comm_data(trCode, rqName, i, "당일매도손익")
            sellProfit = Kiwoom.change_format1(tmp)
            tmp = self._get_comm_data(trCode, rqName, i, "당일매매수수료")
            commission = Kiwoom.change_format1(tmp)
            tmp = self._get_comm_data(trCode, rqName, i, "당일매매세금")
            tax = Kiwoom.change_format1(tmp)


            print("33333333333333333")
            self.opt10074['multi'].append([date, buyCost, sellCost, sellProfit, commission, tax])
        
        if __name__ == "__main__" :
            print(">> 일자별 실현손익 (일자, 매수금액, 매도금액, 당일매도손익, 당일매매수수료, 당일매매세금)")
            print(self.opt10074['multi'])
            tmpDf = tmpDf.append({'일자' : date, '매수금액' : buyCost, '매도금액' : sellCost, '당일매도손익' : sellProfit, '당일매매수수료' : commission, '당일매매세금' : tax}, ignore_index=True)
            tmpDf.to_csv("RealProfitPerDate.csv", index=False, encoding="UTF-8")
            print(">> RealProfitPerDate.csv is made")

# Main
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()

    kiwoom.Make_StrDate()   # 오늘, 어제 날짜 처리

    kiwoom.Comm_Connect()   # 키움 접속
    kiwoom.Get_LoginInfo()  # 로그인 정보
    kiwoom.Get_AllCodeName(kiwoom.MARKET_KOSPI) # 코스피 종목코드 및 종목명
    kiwoom.Get_AllCodeName(kiwoom.MARKET_KOSDAQ)    # 코스닥 종목코드 및 종목명
    kiwoom.Get_Opw00001()   # 예수금상세현황요청
    kiwoom.Get_Opw00018()   # 계좌평가잔고내역요청

    # 보유주식 주식일봉차트조회요청
    for i in range(len(kiwoom.opw00018['multi'])) :     
        code = str(kiwoom.opw00018['multi'][i][0]).replace("A", "")
        #kiwoom.Get_Opt10081(code, kiwoom.yesterday, kiwoom.STOCK_DATA_ALL)
        kiwoom.Get_Opt10081(code, kiwoom.today, kiwoom.STOCK_DATA_ONLY)
        kiwoom.Calc_UpDownRateToday(i)
        kiwoom.Print_Opt10081(i)
        kiwoom.Clear_Opt10081()

    #kiwoom.Get_Opt10074()   # 일자별실현손익요청

    # OPT10074 처리(실현손익정보)
    # 상승/하강률 정보 기반 3%, 5%, 7%, 10%, 15%, 20%, 25%, 29% 도달 체크(몇 분 단위로 실시간 체크할 지)
    # 카톡 메시지 송신 기능 구현