import pandas as pd
import datetime
import os
import shutil
import NaverStock as ns
import SendEmail as se

# 분석하고 싶은 종목
STOCK = {
    "삼성전자" : "005930", 
    "SK하이닉스" : "000660", 
    "NAVER" : "035420", 
    "LG전자" : "066570",
    "현대차" : "005380",
    "카카오" : "035720",
    "씨어스테크놀로지" : "458870",
    "한국전력" : "015760"
    }

RESULT_FILE = "NaverStock.txt"
PDF_SAVE_DIR = "reports"

MY_RECEIVER_EMAIL = "xxx@gmail.com"


# PDF 저장 폴더 초기화
def clear_directory(save_directory):
    print(f"--- {save_directory} 폴더 삭제 ---")

    if not os.path.exists(save_directory):
        print(f"⚠️ 경고: '{save_directory}' 폴더가 존재하지 않습니다.")
        return

    try:
        # shutil.rmtree()를 사용하여 폴더와 모든 내용물을 삭제
        shutil.rmtree(save_directory)
        print(f"🎉 성공: '{save_directory}' 폴더와 내용물 전체가 삭제되었습니다.")

    except OSError as e:
        print(f"❌ 오류: 폴더 삭제 권한 오류 또는 기타 문제 발생: {e}")
    except Exception as e:
        print(f"❌ 알 수 없는 오류 발생: {e}")

    print(f"--- {save_directory} 폴더 생성 ---")
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
        print(f"📁 디렉토리 생성: {save_directory}")


if __name__ == "__main__" :
    
    clear_directory(PDF_SAVE_DIR)

    with open(RESULT_FILE, 'w', encoding="UTF-8") as f :
        # 1. 종목별 현재가(종가) 확인
        print_str = f"1. 종목별 종가({datetime.date.today()})\n"
        f.write(print_str)
        body = print_str
        for key, value in STOCK.items() :
            current_price_text = ns.get_current_price(key, value)
            f.write(current_price_text + '\n')
            body += current_price_text + '\n'
        print(f"--- 현재가 크롤링 세션 종료 ---\n")

        # 2. 외국인/기관 순매매량을 기간별로 총합하여 추세 확인
        print_str = f"\n2. 종목별 매매동향 분석\n"
        f.write(print_str)
        body += print_str
        for key, value in STOCK.items() :
            final_data = pd.DataFrame()
            f.write(f"<{key}> 매매동향\n")
            body += f"<{key}> 매매동향\n"
            for i in range(1, 7) :
                data = ns.get_investor_trading_volume(key, value, i)
                final_data = pd.concat([final_data, data], ignore_index=True)
            
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
        
        print(f"--- 매매동향 크롤링 세션 종료 ---\n")

        # 3. 관심 종목 리포트 링크 및 리포트 다운로드
        print_str = f"3. 종목별 리포트({datetime.date.today()})\n"
        f.write(print_str)
        body += print_str
        for name, code in STOCK.items() :
            reports_list = ns.get_research_reports(name, code)
            print_str = f"<{name}> 종목분석 리포트\n"
            f.write(print_str)
            body += print_str
            for i in range(0, 5) :
                f.write(f"{reports_list[i]['date']} / {reports_list[i]['source']} / {reports_list[i]['link']}\n")
                body += f"{reports_list[i]['date']} / {reports_list[i]['source']} / {reports_list[i]['link']}\n"
            f.write('\n')
            body += '\n'

            for i in range(0, 5) :
                pdf_link = ns.extract_pdf_download_url(reports_list[i]['link'])
                if pdf_link == None :
                    continue
                ns.download_pdf_report(name, reports_list[i]['source'], pdf_link, PDF_SAVE_DIR)
            print(f"--- {name} 종목 리포트 다운로드 완료 ---\n")

    # 4. 메일 전송
    subject = "[자동 보고서] 네이버 증권 데이터 크롤링"
    file_to_send = RESULT_FILE
    se.send_gmail_with_txt(MY_RECEIVER_EMAIL, subject, body, file_to_send)
        