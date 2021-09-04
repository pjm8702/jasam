import requests
import json


response = None
tokens = None
authorize_code = None

def Get_KakaoToken() :
    url = 'https://kauth.kakao.com/oauth/token'
    rest_api_key = '7b38b6fab1cbdbfda1d02061d673ca60'
    redirect_uri = 'https://example.com/oauth'
    authorize_code = '9qkVmay8W-qgl1XXarCxa4koRHMkxq91RMcW_ePt1yEqgrl65gq2yT9osWTfNaenAs_QSQo9c-sAAAF7sJzElg'
    # authorize_code 만료 시 아래 접속 후 코드 갱신 필요
    #webUrl = 'https://kauth.kakao.com/oauth/authorize?client_id=7b38b6fab1cbdbfda1d02061d673ca60&redirect_uri=https://example.com/oauth&response_type=code'

    data = {
        'grant_type':'authorization_code',
        'client_id':rest_api_key,
        'redirect_uri':redirect_uri,
        'code': authorize_code,
        }

    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)

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
    #Get_KakaoToken()
    Send_KakaoMessage("Test Message to Me!!")
