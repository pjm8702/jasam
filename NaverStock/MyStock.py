import time
import pandas as pd
from NaverStock import get_current_price
from NaverStock import get_investor_trading_volume
from NaverStock import get_research_reports
from SendEmail import send_gmail_with_txt

# 분석하고 싶은 종목
CODE = {
    "삼성전자" : "005930", 
    "SK하이닉스" : "000660", 
    "NAVER" : "035420", 
    "카카오" : "035720",
    "씨어스테크놀로지" : "458870",
    "한국전력" : "015760",
    "LG전자" : "066570",
    "현대차" : "005380",
    }

# 결과 txt 파일일
RESULT_FILE = "NaverStock.txt"

# 메일 받을 주소
MY_RECEIVER_EMAIL = "xxx@gmail.com" 


with open(RESULT_FILE, 'w', encoding="UTF-8") as f :
    # 1. 종목별 현재가(종가) 확인
    f.write("1. 종목별 현재가\n")
    body = "1. 종목별 현재가\n"
    for key, value in CODE.items() :
        current_price_text = get_current_price(key, value)
        f.write(current_price_text + '\n')
        body += current_price_text + '\n'
        time.sleep(2)
    print(f"✅ 현재가 크롤링 세션이 종료되었습니다.\n")

    # 2. 외국인/기관 순매매량을 기간별로 총합하여 추세 확인
    f.write("\n2. 종목별 매매동향 분석\n")
    body += "\n2. 종목별 매매동향 분석\n"
    for key, value in CODE.items() :
        final_data = pd.DataFrame()
        f.write(f"<{key}> 매매동향\n")
        body += f"<{key}> 매매동향\n"
        for i in range(1, 7) :
            data = get_investor_trading_volume(key, value, i)
            final_data = pd.concat([final_data, data], ignore_index=True)
            time.sleep(2)
        
        f.write(f"1일간 외국인 / 기관 순매매량 : {final_data.loc[0, '외국인_순매매량']} / {final_data.loc[0, '기관_순매매량']}\n")
        body += f"1일간 외국인 / 기관 순매매량 : {final_data.loc[0, '외국인_순매매량']} / {final_data.loc[0, '기관_순매매량']}\n"
        f.write(f"3일간 외국인 / 기관 순매매량 : {final_data.loc[0:2, '외국인_순매매량'].sum()} / {final_data.loc[0:2, '기관_순매매량'].sum()}\n")
        body += f"3일간 외국인 / 기관 순매매량 : {final_data.loc[0:2, '외국인_순매매량'].sum()} / {final_data.loc[0:2, '기관_순매매량'].sum()}\n"
        f.write(f"5일간 외국인 / 기관 순매매량 : {final_data.loc[0:4, '외국인_순매매량'].sum()} / {final_data.loc[0:4, '기관_순매매량'].sum()}\n")
        body += f"5일간 외국인 / 기관 순매매량 : {final_data.loc[0:4, '외국인_순매매량'].sum()} / {final_data.loc[0:4, '기관_순매매량'].sum()}\n"
        f.write(f"10일간 외국인 / 기관 순매매량 : {final_data.loc[0:9, '외국인_순매매량'].sum()} / {final_data.loc[0:9, '기관_순매매량'].sum()}\n")
        body += f"10일간 외국인 / 기관 순매매량 : {final_data.loc[0:9, '외국인_순매매량'].sum()} / {final_data.loc[0:9, '기관_순매매량'].sum()}\n"
        f.write(f"30일간 외국인 / 기관 순매매량 : {final_data.loc[0:29, '외국인_순매매량'].sum()} / {final_data.loc[0:29, '기관_순매매량'].sum()}\n")
        body += f"30일간 외국인 / 기관 순매매량 : {final_data.loc[0:29, '외국인_순매매량'].sum()} / {final_data.loc[0:29, '기관_순매매량'].sum()}\n"
        f.write(f"60일간 외국인 / 기관 순매매량 : {final_data.loc[0:59, '외국인_순매매량'].sum()} / {final_data.loc[0:59, '기관_순매매량'].sum()}\n")
        body += f"60일간 외국인 / 기관 순매매량 : {final_data.loc[0:59, '외국인_순매매량'].sum()} / {final_data.loc[0:59, '기관_순매매량'].sum()}\n"
        f.write(f"120일간 외국인 / 기관 순매매량 : {final_data.loc[0:119, '외국인_순매매량'].sum()} / {final_data.loc[0:119, '기관_순매매량'].sum()}\n\n")
        body += f"120일간 외국인 / 기관 순매매량 : {final_data.loc[0:119, '외국인_순매매량'].sum()} / {final_data.loc[0:119, '기관_순매매량'].sum()}\n\n"

        #f.write(final_data.to_string() + '\n')
    print(f"✅ 매매동향 크롤링 세션이 종료되었습니다.")

    # 3. 관심 종목 리포트 링크
    for key, value in CODE.items() :
        reports_list = get_research_reports(key, value)
        f.write(f"<{key}> 종목분석 리포트\n")
        body += f"<{key}> 종목분석 리포트\n"
        for i in range(len(reports_list)) :
            f.write(f"{reports_list[i]['date']} / {reports_list[i]['source']} / {reports_list[i]['link']}\n")
            body += f"{reports_list[i]['date']} / {reports_list[i]['source']} / {reports_list[i]['link']}\n"
        f.write('\n')
        body += '\n'

    # 4. 메일 전송
    subject = "[자동 보고서] 네이버 증권 데이터 크롤링"
    #body = "오늘의 분석 결과를 TXT 파일로 첨부합니다."
    file_to_send = RESULT_FILE
    send_gmail_with_txt(MY_RECEIVER_EMAIL, subject, body, file_to_send)
