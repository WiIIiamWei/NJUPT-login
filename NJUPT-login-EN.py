import time
import requests
    
def info_set():
    Bid = str(input("Please input your Student ID (e.g. B20010101): "))
    server = int(input("Please input your ISP (Enter a number) [1]Campus Network [2]CMCC [3]CHINANET): "))
    while server not in [1, 2, 3]:
        if server == 1:
            server = None
        elif server == 2:
            server = "cmcc"
        elif server == 3:
            server = "njxy"
        else:
            print("Invalid input!")
            server = int(input("Please input your ISP (Enter a number) [1]Campus Network [2]CMCC [3]CHINANET): "))
    password = str(input("Please input your password: "))
    config = [Bid, server, password]
    with open("config.bin", "wb") as f:
        f.write(str(config).encode("utf-8"))
        f.close()
    print("Your info has been saved! Proceeding to login...")
    return config

print("A messy NJUPT campus network login script by William Wei")
print("Please note: This script will generate a config.bin file in the current directory to store your login info")
print("Please do not delete or share this file, as it will lead to your password being leaked!")
try:
    with open("config.bin", "rb") as f:
        config = eval(f.read().decode("utf-8"))
        f.close()
except:
    print("You have not set your info!")
    config = info_set()

server_text = {None: "NJUPT", "cmcc": "NJUPT-CMCC", "njxy": "NJUPT-CHINANET"}
print("Logging in to {}...".format(server_text[config[1]]))

if config[1] == None:
    url = ("https://p.njupt.edu.cn:802/eportal/portal/login?callback=dr1003&"
           "login_method=1&"
           "user_account=%2C0%2C{}&"
           "user_password={}&".format(config[0], config[2]))
else:
    url = ("https://p.njupt.edu.cn:802/eportal/portal/login?callback=dr1003&"
           "login_method=1&"
           "user_account=%2C0%2C{}%40{}&"
           "user_password={}&".format(config[0], config[1], config[2]))

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46",
    "Accept": "*/*"}

while True:
    try:
        req = requests.get(url, headers = headers)
        if req.text == 'dr1003({"result":0,"msg":"AC999","ret_code":2});':
            print("Login failed! You are already logged in!")
            break
        elif req.text == 'dr1003({"result":0,"msg":"运营商账号在线数超出限制，请联系运营商处理(Rad:Limit Users Err)","ret_code":1});':
            print("Login failed! You have reached the maximum amount of devices! Please log out one device at the self-service platform!")
        elif req.text == 'dr1003({"result":0,"msg":"账号或密码错误(ldap校验)","ret_code":1});':
            print("Login failed! Username or password error!")
            print("Please re-set your info!")
            config = info_set()
        elif req.text == 'dr1003({"result":0,"msg":"账号错误(运营商登录请检查输入的账号和绑定的运营商账号是否有误)","ret_code":1});':
            print("Login failed! Incorrect ISP provided!")
            print("Please re-set your info!")
            config = info_set()
        elif req.text == 'dr1003({"result":0,"msg":"本账号费用超支，禁止使用","ret_code":1});':
            print("Login failed! Your account has reached max cost limit! Please change your cost limit at the self-service platform!")
        elif req.text == 'dr1003({"result":0,"msg":"运营商账号欠费或停机(Rad:Status_Err)","ret_code":1});':
            print("Login failed! Your ISP account has been suspended! Please recharge your account!")
        elif req.text == 'dr1003({"result":1,"msg":"Portal协议认证成功！"});':
            print("Login successful!")
            break
        else:
            print("Login failed! Unknown error! Error message:")
            print(req.text)
        input("Press Enter to try again, or Ctrl+C to exit...")
    except requests.exceptions.SSLError:
        print("Login failed! You are not connected to Wi-Fi or Ethernet!")
        input("Press Enter to try again, or Ctrl+C to exit...")

print("Exiting in 1s...")
time.sleep(1)