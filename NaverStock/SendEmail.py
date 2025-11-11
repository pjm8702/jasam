import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_gmail(sender_email, receiver_email, password, subject, body, file_path = "empty"):
    
    # E-Mail Message Object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    # E-Mail Text(MIMEText)
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # E-Mail Attachment(MIMEBase)
    if file_path != "empty" :
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                attachment_data = f.read()
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_data.encode('utf-8'))
            
            # encode Base64(E-Mail Standard)
            encoders.encode_base64(part)
            
            file_name = file_path.split('/')[-1].split('\\')[-1]
            part.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', file_name))
            
            msg.attach(part)
            
        except FileNotFoundError:
            print(f"❌ 첨부 파일 오류: '{file_path}' 파일을 찾을 수 없습니다.")
            return
        except Exception as e:
            print(f"❌ 파일 처리 중 오류: {e}")
            return

    # Gmail SMTP Server connect
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587  # TLS(Security Transport) Port
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()  # TLS Encryption
        
        server.login(sender_email, password)
        
        server.sendmail(sender_email, sender_email, msg.as_string())
        
        print(f"✅ 이메일 전송 성공: '{subject}' 제목의 메일을 {sender_email} (으)로 보냈습니다.")
        
    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP 인증 실패: SENDER_EMAIL 또는 SENDER_PASSWORD(앱 비밀번호)를 확인하세요.")
    except Exception as e:
        print(f"❌ 이메일 전송 실패: {e}")
    finally:
        if 'server' in locals():
            server.quit()


if __name__ == "__main__":
    try:
        with open("NaverStock.txt", "w", encoding="utf-8") as f:
            f.write("네이버 증권 매매동향 분석 결과입니다.\n")
        print("NaverStock.txt 파일 저장 완료.")
    except Exception as e:
        print(f"파일 저장 오류: {e}")

    sender_email = "xxx@gmail.com"
    receiver_email = "xxx@gmail.com"
    password = "xxx"     # 🔑 Google App Password
    subject = "테스트 이메일"
    body = "이메일 전송 테스트"
    file_path = "NaverStock.txt"
    
    send_gmail(sender_email, receiver_email, password, subject, body, file_path)