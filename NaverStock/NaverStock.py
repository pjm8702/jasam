import requests
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from urllib.parse import urlparse, unquote

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
            response = s.get(URL, headers=headers, timeout=10)
            response.raise_for_status() # 200 OK 상태 코드가 아니면 예외 발생
            time.sleep(1)
            
            # 3. BeautifulSoup을 사용해 HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 4. 원하는 정보(현재가)가 있는 HTML 요소를 선택 (CSS Selector)
            #    - 네이버 증권 페이지에서 현재가는 'strong' 태그와 'id'가 '_nowVal'인 요소에 있음
            #    - 이 선택자는 네이버가 웹사이트 구조를 바꾸면 변경될 수 있음
            price_element = soup.select_one('strong#_nowVal')

            # 5. 전일대비 등락액 요소 선택 (클래스나 ID는 네이버 구조에 따라 다를 수 있음)
            # 네이버 시세 페이지에서 전일대비 등락액은 보통 '_diff'나 '_dltp' ID를 사용합니다.
            diff_element = soup.select_one('strong#_diff') 
            
            # 6. 전일대비 등락률 요소 선택
            # 등락률은 보통 '_rate' ID를 사용합니다.
            rate_element = soup.select_one('strong#_rate')
            
            if price_element:
                current_price = price_element.get_text().strip()
                diff_price = diff_element.get_text().strip()
                diff_price = "".join(diff_price.split())
                diff_rate = rate_element.get_text().strip()
                current_price_text = f"<{name}> 현재가: {current_price} {diff_price}({diff_rate})"
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
            s.get(f'https://finance.naver.com/item/sise.naver?code={code}', headers=headers, timeout=10)
            time.sleep(1)

            response = s.get(URL)
            response.raise_for_status()
            
            # 4. pandas의 read_html로 페이지의 모든 <table> 읽기
            #    - read_html은 HTML 텍스트에서 <table> 태그를 모두 찾아 DataFrame의 리스트(List)로 반환
            tables = pd.read_html(StringIO(response.text))

            # 5. 원하는 테이블 선택
            #    - 네이버 증권의 해당 페이지에는 여러 테이블이 있어 원하는 데이터 index 찾아야 함
            #    - NXT 탭이 없는 종목은 예외 처리 필요
            if len(tables) > 0:
                if name == "씨어스테크놀로지" or name == "카카오" or name == "한국전력":
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
            response = s.get(URL, headers=headers, timeout=10)
            response.raise_for_status()
            time.sleep(1)

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

            print(f"✅ <{name}> 리포트 페이지 크롤링 완료")
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP 오류 발생: {e}")
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        
        return reports_list


# 종목 리포트 페이지에서 PDF 링크 URL 추출
def extract_pdf_download_url(report_detail_url):
   
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer' : 'https://finance.naver.com/research/'
    }
    
    with requests.Session() as s :
        try:
            s.headers.update(headers) # 세션에 기본 헤더 업데이트
            response = s.get(report_detail_url, headers=headers, timeout=10)
            response.raise_for_status()
            time.sleep(1)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. PDF 링크가 위치할 가능성이 높은 특정 영역을 검색 (예: table.view tbody)
            # 네이버 증권의 리포트 상세 페이지는 보통 첨부파일 링크를 <a> 태그로 제공합니다.
            
            # 2. 'pdf' 또는 '다운로드' 문구가 포함된 링크를 찾습니다.
            # 가장 흔한 구조: <a> 태그의 href가 .pdf로 끝나는 경우를 찾습니다.
            pdf_link_tag = soup.find('a', href=lambda href: href and ('.pdf' in href.lower()))
            
            if pdf_link_tag:
                relative_link = pdf_link_tag['href']
                #print(relative_link)
                
                # 링크가 상대 경로일 경우 (예: /imgstock/upload/...)
                if relative_link.startswith('/'):
                    BASE_URL = "https://finance.naver.com"
                    full_pdf_url = BASE_URL + relative_link
                else:
                    full_pdf_url = relative_link
                    
                return full_pdf_url
            
            return None # PDF 링크를 찾지 못함

        except requests.exceptions.RequestException as e:
            print(f"❌ 요청 오류 발생 ({report_detail_url}): {e}")
            return None
        except Exception as e:
            print(f"❌ 기타 오류 발생: {e}")
            return None


# 종목 분석 리포트 다운로드
def download_pdf_report(name, source, pdf_url, save_directory):
      
    # 1. User-Agent 설정 (서버 차단 방지)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer' : 'https://finance.naver.com/research/company_list.naver'
    }
    
    # 2. 파일명 결정
    try:
        # URL에서 파일명을 추출 (경로의 마지막 부분)
        parsed_url = urlparse(pdf_url)
        # URL 디코딩 (한글 파일명 처리) 후, 경로의 마지막 부분(파일명)만 추출
        file_name = f"{name}_{source}_{unquote(os.path.basename(parsed_url.path))}"
        if not file_name.endswith('.pdf'):
            # 파일 확장자가 .pdf가 아니거나 이상하면 기본 파일명 지정
            file_name = file_name + ".pdf" 

    except Exception:
        file_name = f"{name}_{source}_default_report.pdf"

    # 3. 저장 경로 생성
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
        print(f"📁 디렉토리 생성: {save_directory}")
        
    save_path = os.path.join(save_directory, file_name)
        
    with requests.Session() as s :
        # 4. 파일 다운로드 요청
        try:
            s.headers.update(headers) # 세션에 기본 헤더 업데이트
            response = s.get(pdf_url, headers=headers, stream=True)
            response.raise_for_status() # HTTP 오류 시 예외 발생
            time.sleep(1)

            # 5. Content-Type 헤더 검증 (응답이 PDF인지 확인)
            content_type = response.headers.get('Content-Type', '').lower()
            if 'application/pdf' not in content_type and 'application/octet-stream' not in content_type:
                # Content-Type이 'text/html'이면서 PDF 내용이 없는 경우를 포착
                print(f"❌ 다운로드 실패: Content-Type이 PDF 관련 유형이 아닙니다. Content-Type: {content_type}")
                print(f"   응답 시작 부분 (디버깅): {response.text[:100].strip()}...") 
                return None
            
            # 6. 바이너리 파일로 저장 (wb: write binary)
            with open(save_path, 'wb') as f:
                # response.iter_content(chunk_size=8192) : 데이터를 8KB씩 끊어서 저장
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk: # 필터링 (간혹 keep-alive 청크가 있을 수 있음)
                        f.write(chunk)
            
            # 7. 저장 후 파일 크기 검증 (0KB 파일 방지)
            if os.path.getsize(save_path) == 0:
                print(f"❌ 다운로드 실패: 파일 크기가 0KB입니다. 파일을 삭제합니다.")
                os.remove(save_path)
                return None
            
            print(f"✅ 다운로드 성공: '{file_name}' 저장 완료")
            return save_path
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP 오류 발생 (URL: {pdf_url}): 서버 응답 오류 {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ 요청 오류 발생 (URL: {pdf_url}): {e}")
            return None
        except Exception as e:
            print(f"❌ 기타 오류 발생: {e}")
            return None


if __name__ == "__main__" :  
    get_current_price("삼성전자", "005930")
    exit()
    final_data = pd.DataFrame()
    for i in range(1, 3) :
        data = get_investor_trading_volume("삼성전자", "005930", i)
        final_data = pd.concat([final_data, data], ignore_index=True)
        time.sleep(2)
    print(final_data.loc[0:2, '외국인_순매매량'].sum())

    reports_list = get_research_reports("삼성전자", "005930")
    print(reports_list[1]['link'])

    pdf_url = extract_pdf_download_url(reports_list[1]['link'])
    
    download_pdf_report("삼성전자", 1, pdf_url)
    