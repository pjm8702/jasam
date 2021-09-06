import requests
import json
import time
from selenium import webdriver

response = None
tokens = None
authorize_code = None

def Get_KakaoToken() :
    kakaoTokenUrl = 'https://kauth.kakao.com/oauth/authorize?client_id=7b38b6fab1cbdbfda1d02061d673ca60&redirect_uri=https://example.com/oauth&response_type=code'
    
    f = open("kakaoInfo.txt", "r")
    id = f.readline().rstrip()
    pw = f.readline().rstrip()

    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(url=kakaoTokenUrl)
    time.sleep(1)

    driver.find_element_by_id('id_email_2').send_keys(id)
    driver.find_element_by_id('id_password_3').send_keys(pw)
    loginButton = driver.find_element_by_class_name('submit')
    loginButton.click()
    time.sleep(5)
    
    tokenUrl = driver.current_url
    token = tokenUrl.replace("https://example.com/oauth?code=", "")
    driver.quit()

    url = 'https://kauth.kakao.com/oauth/token'
    rest_api_key = '7b38b6fab1cbdbfda1d02061d673ca60'
    redirect_uri = 'https://example.com/oauth'
    authorize_code = token

    data = {
        'grant_type':'authorization_code',
        'client_id':rest_api_key,
        'redirect_uri':redirect_uri,
        'code': authorize_code,
        }

    response = requests.post(url, data=data)
    tokens = response.json()

    with open(r"C:\Users\pjm87\Documents\Coding\jasam\elephant\kakao_code.json","w") as fp:
        json.dump(tokens, fp)
    print(tokens)

def Send_KakaoMessage(msg) :
    with open(r"C:\Users\pjm87\Documents\Coding\jasam\elephant\kakao_code.json","r") as fp:
        tokens = json.load(fp)
    
    url="https://kapi.kakao.com/v2/api/talk/memo/default/send"

    # kapi.kakao.com/v2/api/talk/memo/default/send 

    headers={
        "Authorization" : "Bearer " + tokens["access_token"]
    }

    data={
        "template_object": json.dumps({
            "object_type":"text",
            "text":msg,
            "link":{
                "web_url":"https://developers.kakao.com"
            }
        })
   }

    response = requests.post(url, headers=headers, data=data)
    response.status_code


if __name__ == "__main__" :
    Get_KakaoToken()
    Send_KakaoMessage("Test Message to Me!!")
