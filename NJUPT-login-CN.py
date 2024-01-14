import time
import requests
    
def info_set():
    Bid = str(input("请输入您的学号（如：B20010101）："))
    server = int(input("请输入您的运营商（输入序号）[1]校园网 [2]中国移动 [3]中国电信: "))
    while server not in [1, 2, 3]:
        print("输入无效！")
        server = int(input("请输入您的运营商（输入序号）[1]校园网 [2]中国移动 [3]中国电信: "))
    if server == 1:
        server = None
    elif server == 2:
        server = "cmcc"
    elif server == 3:
        server = "njxy"
    password = str(input("请输入您的密码："))
    config = [Bid, server, password]
    with open("config.bin", "wb") as f:
        f.write(str(config).encode("utf-8"))
        f.close()
    print("您的信息已保存！准备登录...")
    return config

print("乱写的南京邮电大学校园网登录脚本by William Wei")
print("请注意：本脚本会在当前文件夹生成config.bin储存你的登录信息")
print("请不要随意删除或传播该文件，此举会导致你的密码泄露！")
try:
    with open("config.bin", "rb") as f:
        config = eval(f.read().decode("utf-8"))
        f.close()
except:
    print("您还没有设置登录信息！")
    config = info_set()

server_text = {None: "NJUPT", "cmcc": "NJUPT-CMCC", "njxy": "NJUPT-CHINANET"}
print("正在登录到{}...".format(server_text[config[1]]))

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
            print("登录失败！您已经登录到校园网！")
            break
        elif req.text == 'dr1003({"result":0,"msg":"运营商账号在线数超出限制，请联系运营商处理(Rad:Limit Users Err)","ret_code":1});':
            print("登录失败！您已经达到最大设备数，请至自助服务平台登出一个设备！")
        elif req.text == 'dr1003({"result":0,"msg":"账号或密码错误(ldap校验)","ret_code":1});':
            print("登录失败！用户名或密码错误！")
            print("请重新设置您的信息！")
            config = info_set()
        elif req.text == 'dr1003({"result":0,"msg":"账号错误(运营商登录请检查输入的账号和绑定的运营商账号是否有误)","ret_code":1});':
            print("登录失败！您输入的运营商错误！")
            print("请重新设置您的信息！")
            config = info_set()
        elif req.text == 'dr1003({"result":0,"msg":"本账号费用超支，禁止使用","ret_code":1});':
            print("登录失败！您的校园网账户费用超支，请至自助服务平台重设消费保护！")
        elif req.text == 'dr1003({"result":0,"msg":"运营商账号欠费或停机(Rad:Status_Err)","ret_code":1});':
            print("登录失败！您的校园卡欠费或停机，请充值您的校园卡！")
        elif req.text == 'dr1003({"result":1,"msg":"Portal协议认证成功！"});':
            print("登录成功！")
            break
        else:
            print("登录失败！未知错误！原始请求信息：")
            print(req.text)
        input("按Enter键重试，或按Ctrl+C退出...")
    except requests.exceptions.SSLError:
        print("登录失败！请检查您的网络连接！")
        input("按Enter键重试，或按Ctrl+C退出...")

print("程序将在1s后退出...")
time.sleep(1)