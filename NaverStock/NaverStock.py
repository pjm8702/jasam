import requests
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from urllib.parse import urlparse, unquote

# STOCK current price
def get_current_price(name, code) :
        
    URL = f"https://finance.naver.com/item/sise.naver?code={code}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer' : f'https://finance.naver.com/item/sise.naver?code={code}'
    }
    
    with requests.Session() as s :
        try:
            s.headers.update(headers)

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
            
            # HTML Parsing
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # strong tag include information
            price_element = soup.select_one('strong#_nowVal')
            diff_element = soup.select_one('strong#_diff') 
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


# STOCK Investor Trading data
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
            
            # read <table> tag and return DataFrame
            tables = pd.read_html(StringIO(response.text))

            # Next trading stock and Normal trading stock are different
            if len(tables) > 0:
                if name == "씨어스테크놀로지" or name == "카카오" or name == "한국전력": # Normal stock
                    trading_data = tables[2]
                else : # Next trading stock
                    trading_data = tables[3]

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


# STOCK Reprot
def get_research_reports(name, code) :

    URL = f"https://finance.naver.com/research/company_list.naver?keyword=&brokerCode=&writeFromDate=&writeToDate=&searchType=itemCode&itemName=%BB%EF%BC%BA%C0%FC%C0%DA&itemCode={code}&x=38&y=18&page=1"
    BASE_URL = "https://finance.naver.com/research/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer' : BASE_URL
    }
    
    reports_list = []

    with requests.Session() as s :
        try :
            s.headers.update(headers)
            response = s.get(URL, headers=headers, timeout=10)
            response.raise_for_status()
            time.sleep(1)

            soup = BeautifulSoup(response.text, 'html.parser')

            # Report List <table class="type_1">'s <tr> have not class
            report_rows = soup.select('table.type_1 tr:not([class])')

            if not report_rows:
                print(f"리포트를 찾지 못했습니다. (구조 변경 또는 마지막 페이지)")
                return None
            
            for row in report_rows:
                cells = row.find_all('td')
                #print(cells)
                
                # Title, Stock Company, Date
                if len(cells) < 3:
                    continue
                    
                # Title and link <a>
                link_tag = cells[1].find('a')
                if not link_tag:
                    continue
                    
                title = link_tag.get_text(strip=True)
                relative_link = link_tag['href']
                full_link = BASE_URL + relative_link # '/research/...' -> 'https://...'
                
                # Stock Company
                source = cells[2].get_text(strip=True)
                
                # Date
                date = cells[4].get_text(strip=True)
                
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


# STOCK Report link
def extract_pdf_download_url(report_detail_url):
   
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer' : 'https://finance.naver.com/research/'
    }
    
    with requests.Session() as s :
        try:
            s.headers.update(headers)
            response = s.get(report_detail_url, headers=headers, timeout=10)
            response.raise_for_status()
            time.sleep(1)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            pdf_link_tag = soup.find('a', href=lambda href: href and ('.pdf' in href.lower()))
            
            if pdf_link_tag:
                relative_link = pdf_link_tag['href']
                
                if relative_link.startswith('/'):
                    BASE_URL = "https://finance.naver.com"
                    full_pdf_url = BASE_URL + relative_link
                else:
                    full_pdf_url = relative_link
                    
                return full_pdf_url
            
            return None

        except requests.exceptions.RequestException as e:
            print(f"❌ 요청 오류 발생 ({report_detail_url}): {e}")
            return None
        except Exception as e:
            print(f"❌ 기타 오류 발생: {e}")
            return None


# STOCK Report download
def download_pdf_report(no, name, source, pdf_url, save_directory):
      
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer' : 'https://finance.naver.com/research/company_list.naver'
    }
    
    try:
        parsed_url = urlparse(pdf_url)
        file_name = f"{name}_{no}_{source}_{unquote(os.path.basename(parsed_url.path))}"
        if not file_name.endswith('.pdf'):
            file_name = file_name + ".pdf" 
    except Exception:
        file_name = f"{name}_{no}_{source}_default_report.pdf"
        
    save_path = os.path.join(save_directory, file_name)
        
    with requests.Session() as s :
        try:
            s.headers.update(headers)
            response = s.get(pdf_url, headers=headers, stream=True)
            response.raise_for_status()
            time.sleep(1)

            # Check Content-Type
            content_type = response.headers.get('Content-Type', '').lower()
            if 'application/pdf' not in content_type and 'application/octet-stream' not in content_type:
                print(f"❌ 다운로드 실패: Content-Type이 PDF 관련 유형이 아닙니다. Content-Type: {content_type}")
                print(f"   응답 시작 부분 (디버깅): {response.text[:100].strip()}...") 
                return None
            
            # Save binary file
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Check file size
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
    
    final_data = pd.DataFrame()
    for i in range(1, 3) :
        data = get_investor_trading_volume("삼성전자", "005930", i)
        final_data = pd.concat([final_data, data], ignore_index=True)
        time.sleep(1)
    print(final_data.loc[0:2, '외국인_순매매량'].sum())

    reports_list = get_research_reports("삼성전자", "005930")
    print(reports_list[1])

    pdf_url = extract_pdf_download_url(reports_list[1]['link'])
    
    download_pdf_report(1, "삼성전자", reports_list[1]['source'], pdf_url, ".")

    