import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_gmail_with_txt(to_email, sender_email, sender_password, subject, body, file_path):
        
    # 1. 이메일 메시지 객체 생성 (MIMEMultipart)
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # 2. 본문 추가 (MIMEText)
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # 3. 파일 첨부 (MIMEBase)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 텍스트 파일의 내용을 읽습니다.
            attachment_data = f.read()
        
        # 텍스트 파일을 MIMEBase 객체로 만듭니다. 
        # (TXT의 경우 MIMEText로도 가능하지만, 범용성을 위해 MIMEBase 사용)
        part = MIMEBase('application', 'octet-stream')
        
        # TXT 파일 내용을 UTF-8 바이트로 인코딩하여 페이로드로 설정
        part.set_payload(attachment_data.encode('utf-8'))
        
        # Base64로 인코딩 (이메일 전송 표준)
        encoders.encode_base64(part)
        
        # 파일명 지정 (ASCII가 아닌 파일명도 처리되도록 인코딩)
        file_name = file_path.split('/')[-1].split('\\')[-1]
        part.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', file_name))
        
        msg.attach(part)
        
    except FileNotFoundError:
        print(f"❌ 첨부 파일 오류: '{file_path}' 파일을 찾을 수 없습니다.")
        return
    except Exception as e:
        print(f"❌ 파일 처리 중 오류: {e}")
        return

    # 4. Gmail SMTP 서버에 연결 및 전송
    try:
        # Gmail SMTP 서버 주소 및 포트
        smtp_server = "smtp.gmail.com"
        smtp_port = 587  # TLS(보안 연결) 포트
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()      # 서버에 인사
        server.starttls()  # TLS 암호화 시작
        
        # 앱 비밀번호로 로그인
        server.login(sender_email, sender_password)
        
        # 메일 전송
        server.sendmail(sender_email, to_email, msg.as_string())
        
        print(f"✅ 이메일 전송 성공: '{subject}' 제목의 메일을 {to_email} (으)로 보냈습니다.")
        
    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP 인증 실패: SENDER_EMAIL 또는 SENDER_PASSWORD(앱 비밀번호)를 확인하세요.")
    except Exception as e:
        print(f"❌ 이메일 전송 실패: {e}")
    finally:
        if 'server' in locals():
            server.quit() # 서버 연결 종료


if __name__ == "__main__":
    # 1. 분석 결과를 TXT 파일로 저장
    try:
        with open("NaverStock.txt", "w", encoding="utf-8") as f:
            f.write("네이버 증권 매매동향 분석 결과입니다.\n")
        print("NaverStock.txt 파일 저장 완료.")
    except Exception as e:
        print(f"파일 저장 오류: {e}")

    # 2. 메일 전송
    MY_RECEIVER_EMAIL = "pjm8702@gmail.com" # 📥 메일을 받을 주소
    
    subject = "[자동 보고서] 네이버 증권 매매동향"
    body = "오늘의 매매동향 분석 결과를 TXT 파일로 첨부합니다."
    file_to_send = "NaverStock.txt"
    
    send_gmail_with_txt(MY_RECEIVER_EMAIL, subject, body, file_to_send)