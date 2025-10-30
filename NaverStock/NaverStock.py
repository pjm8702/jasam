import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

# 현재가
def get_current_price(name, code) :
    URL = f"https://finance.naver.com/item/sise.naver?code={code}"
    
    # 1. 'User-Agent' 설정 (네이버는 봇(Bot) 접근을 막을 수 있음)
    #    - 마치 일반적인 웹 브라우저(크롬 등)에서 접속하는 것처럼 속여주는 헤더
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer' : f'https://finance.naver.com/item/sise.naver?code={code}'
    }
    
    with requests.Session() as s :
        try:
            s.headers.update(headers)

            # 2. requests를 사용해 URL에 GET 요청 (헤더 포함)
            #   - response.status_code : 200 성공, 404 Not Found, 403 Forbidden, 500 Internal Server Error
            #   - response.ok : status_code가 성공 범위면 True, 오류 범위면 False
            #   - response.raise_for_status() : status_code가 4xx, 5xx 같은 오류 시 Exception 발생
            #   - response.text : 서버가 보낸 디코딩된 데이터
            #   - response.content : 서버가 보낸 raw bytes
            #   - response.json() : 응답 내용이 json일 경우 파싱하여 dict or list로 변환
            #   - response.headers : 응답 헤더 정보, ['Content-Type'], ['Set-Cookie'], ['Server']
            #response = s.get(URL, headers=headers)
            response = s.get(URL, headers=headers)
            response.raise_for_status() # 200 OK 상태 코드가 아니면 예외 발생
            
            # 3. BeautifulSoup을 사용해 HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 4. 원하는 정보(현재가)가 있는 HTML 요소를 선택 (CSS Selector)
            #    - 네이버 증권 페이지에서 현재가는 'strong' 태그와 'id'가 '_nowVal'인 요소에 있음
            #    - 이 선택자는 네이버가 웹사이트 구조를 바꾸면 변경될 수 있음음
            price_element = soup.select_one('strong#_nowVal')
            
            if price_element:
                current_price = price_element.get_text()
                current_price_text = f"<{name}> 현재가: {current_price}"
                print(f"✅ {current_price_text}")
                return current_price_text
            else:
                print("❌ 현재가 정보를 담고 있는 요소를 찾지 못했습니다.")
                print("    (네이버 증권 페이지의 HTML 구조가 변경되었을 수 있습니다.)")
                return ""

        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP 오류 발생: {e}")
        except requests.exceptions.RequestException as e:
            print(f"❌ 요청 오류 발생: {e}")
        except Exception as e:
            print(f"❌ 알 수 없는 오류 발생: {e}")
        return ""


# 투자자별 매매동향
def get_investor_trading_volume(name, code, page) :
    URL = f"https://finance.naver.com/item/frgn.naver?code={code}&page={page}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer' : f'https://finance.naver.com/item/sise.naver?code={code}'
    }

    trading_data = pd.DataFrame()
    with requests.Session() as s :
        try :
            s.headers.update(headers)
            s.get(f'https://finance.naver.com/item/sise.naver?code={code}')
            time.sleep(2)

            response = s.get(URL)
            response.raise_for_status()
            
            # 4. pandas의 read_html로 페이지의 모든 <table> 읽기
            #    - read_html은 HTML 텍스트에서 <table> 태그를 모두 찾아 DataFrame의 리스트(List)로 반환
            tables = pd.read_html(StringIO(response.text))

            # 5. 원하는 테이블 선택
            #    - 네이버 증권의 해당 페이지에는 여러 테이블이 있어 원하는 데이터 index 찾아야 함
            if len(tables) > 0:
                if name == "씨어스테크놀로지" :
                    trading_data = tables[2]
                else :
                    trading_data = tables[3]
                #print(trading_data)

                # 6. MultiIndex로 된 컬럼 정리
                #trading_data.columns = ['_'.join(col).strip() for col in trading_data.columns.values] # MultiIndex 정리
                trading_data.columns = ['날짜', '종가', '전일비', ' 등락률', '거래량', '기관_순매매량', '외국인_순매매량', '외국인_보유주수', '외국인_보유율']
                trading_data = trading_data.dropna(subset=['날짜'])
                
                print(f"✅ <{name}> 매매동향 {page}")
                print(trading_data.head())
                
            else:
                print("❌ 페이지에서 테이블을 찾지 못했습니다.")

        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP 오류 발생: {e}")
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
    return trading_data


# 종목 분석 리포트 목록
def get_research_reports(name, code) :
    URL = f"https://finance.naver.com/research/company_list.naver?keyword=&brokerCode=&writeFromDate=&writeToDate=&searchType=itemCode&itemName=%BB%EF%BC%BA%C0%FC%C0%DA&itemCode={code}&x=38&y=18&page=1"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer' : 'https://finance.naver.com/research/'
    }

    BASE_URL = "https://finance.naver.com/research/"
    reports_list = []

    with requests.Session() as s :
        try :
            s.headers.update(headers)
            response = s.get(URL)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 리포트 목록은 <table class="type_1"> 안의 <tr>(행)에 있습니다.
            # 'class'가 없는 <tr> 태그만 선택 (헤더/구분선 제외)
            report_rows = soup.select('table.type_1 tr:not([class])')

            if not report_rows:
                print(f"리포트를 찾지 못했습니다. (구조 변경 또는 마지막 페이지)")
                return None
            
            for row in report_rows:
                # 각 행(tr)에서 td(칸)들을 찾습니다.
                cells = row.find_all('td')
                #print(cells)
                
                # [제목, 증권사, (파일), 날짜] 구조를 가집니다.
                if len(cells) < 3: # 최소 3칸(제목, 증권사, 날짜)이 아니면 건너뛰기
                    continue
                    
                # 1. 제목 및 링크 추출 (첫 번째 칸)
                link_tag = cells[1].find('a')
                #print(link_tag)
                if not link_tag:
                    continue
                    
                title = link_tag.get_text(strip=True)
                relative_link = link_tag['href']
                full_link = BASE_URL + relative_link # '/research/...' -> 'https://...'
                
                # 2. 증권사 추출 (두 번째 칸)
                source = cells[2].get_text(strip=True)
                
                # 3. 날짜 추출 (마지막 칸)
                date = cells[4].get_text(strip=True)
                
                #print(title, relative_link, full_link, source, date)
                
                # 결과 리스트에 딕셔너리 형태로 저장
                reports_list.append({
                    'title': title,
                    'source': source,
                    'date': date,
                    'link': full_link
                })

            print(f"✅ <{name}> 리포트 페이지 크롤링 완료 (리포트 {len(reports_list)}개)")
            time.sleep(2) # 차단 방지
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP 오류 발생: {e}")
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        
        return reports_list


if __name__ == "__main__" :  
    current_price_text = get_current_price("삼성전자", "005930")
    print(current_price_text)
    time.sleep(2)
    
    final_data = pd.DataFrame()
    for i in range(1, 2) :
        data = get_investor_trading_volume("삼성전자", "005930", i)
        final_data = pd.concat([final_data, data], ignore_index=True)
        time.sleep(2)
    print(final_data.info())
    print(final_data)
    print(final_data.loc[0, '외국인_순매매량'])
    print(final_data.loc[0:2, '외국인_순매매량'].sum())

    reports_list = get_research_reports("삼성전자", "005930")
    print(reports_list[0]['link'])
    