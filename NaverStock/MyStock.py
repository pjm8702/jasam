import pandas as pd
import datetime
import os
import shutil
import NaverStock as ns
import SendEmail as se
import MyZip as mz
import TradeGraph as tg

# MY STOCK
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


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
RESULT_FILE = CURRENT_PATH + "\\NaverStock.txt"
REPORT_DIR = CURRENT_PATH + '\\reports'
ZIP_FILE = CURRENT_PATH + '\\reports.zip'

INVERSER_TRADING_MAX_PAGE = 3
PDF_MAX_NUM = 3


# delete and make reports folder to save Stock PDF
def clear_directory(save_directory):
    print(f"--- {save_directory} 폴더 삭제 ---")

    if not os.path.exists(save_directory):
        print(f"⚠️ 경고: '{save_directory}' 폴더가 존재하지 않습니다.")
        return

    try:
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

    clear_directory(REPORT_DIR)

    foreign_data_list = []
    institution_data_list = []

    with open(RESULT_FILE, 'w', encoding="utf-8") as f :
        # Get current price of STOCK
        print_str = f"1. 종목별 종가({datetime.date.today()})\n"
        f.write(print_str)
        body = print_str
        for key, value in STOCK.items() :
            current_price_text = ns.get_current_price(key, value)
            f.write(current_price_text + '\n')
            body += current_price_text + '\n'
        print(f"--- 현재가 크롤링 세션 종료 ---\n")

        # Get Foreign/Institution's amount of buy
        print_str = f"\n2. 종목별 매매동향 분석\n"
        f.write(print_str)
        body += print_str
        for key, value in STOCK.items() :
            final_data = pd.DataFrame()
            f.write(f"<{key}> 매매동향\n")
            body += f"<{key}> 매매동향\n"
            for i in range(1, INVERSER_TRADING_MAX_PAGE) :
                data = ns.get_investor_trading_volume(key, value, i)
                final_data = pd.concat([final_data, data], ignore_index=True)

            days = [1, 3, 5, 10, 30, 60]
            for d in days :
                end_idx = d - 1
                foreign_sum = final_data.loc[0:end_idx, '외국인_순매매량'].sum()
                foreign_data_list.append(foreign_sum)
                institution_sum = final_data.loc[0:end_idx, '기관_순매매량'].sum()
                institution_data_list.append(institution_sum)
            
                f.write(f"{d}일간 외국인 / 기관 순매매량 : {foreign_sum} / {institution_sum}\n")
                body += f"{d}일간 외국인 / 기관 순매매량 : {foreign_sum} / {institution_sum}\n"
        f.write('\n')
        body += '\n'
        print(f"--- 매매동향 크롤링 세션 종료 ---\n")

        # Download STOCK's Report
        print_str = f"3. 종목별 리포트({datetime.date.today()})\n"
        f.write(print_str)
        body += print_str
        for name, code in STOCK.items() :
            reports_list = ns.get_research_reports(name, code)
            print_str = f"<{name}> 종목분석 리포트\n"
            f.write(print_str)
            body += print_str
            for i in range(0, PDF_MAX_NUM) :
                f.write(f"{reports_list[i]['date']} / {reports_list[i]['source']} / {reports_list[i]['link']}\n")
                body += f"{reports_list[i]['date']} / {reports_list[i]['source']} / {reports_list[i]['link']}\n"
            f.write('\n')
            body += '\n'

            for i in range(0, PDF_MAX_NUM) :
                pdf_link = ns.extract_pdf_download_url(reports_list[i]['link'])
                if pdf_link == None :
                    continue
                ns.download_pdf_report(i, name, reports_list[i]['source'], pdf_link, REPORT_DIR)
            print(f"--- {name} 종목 리포트 다운로드 완료 ---\n")
        
    # reports to zip
    mz.folder_to_zip(REPORT_DIR, ZIP_FILE)

    # Send E-Mail
    sender_email = "pjm8702@gmail.com"
    receiver_email = "pjm8702@gmail.com"
    password = "wlntofwdzhbtwldr"     # 🔑 Google App Password
    subject = f"[보고서] 네이버 증권 데이터({datetime.date.today()})"
    file_path = ZIP_FILE
    se.send_gmail(sender_email, receiver_email, password, subject, body, file_path)
        