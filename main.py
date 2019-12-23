import requests
import json
import rsa


def readUserPwd(fileName):
    """读取配置文件的账户名密码
    :param fileName: 文件路径
    """
    pass



def sendReuqst(user,pwd):
    pass

getKeyMaps = "http://jxdxfz.zj.chinamobile.com/public/LOGIN/keyMaps"

userAgent = "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"

headers = {
           'X-Requested-With':'XMLHttpRequest',
           'User-Agent':userAgent,
           'Origin':'http://jxdxfz.zj.chinamobile.com',
           'Referer':'http://jxdxfz.zj.chinamobile.com/login'}

response = requests.get(getKeyMaps,headers=headers)
content = response.content.decode()

print(content)

#解析json
parse = json.loads(content)
deskey = parse['desKey']
retMessage = parse['retMessage']
retCode = parse['retCode']
print(deskey)
print(retMessage)
print(retCode)


#解析session
response_header = response.headers
session = response_header['Set-Cookie']
sessionList = session.split(';')
print(sessionList[0])

#加密密码
userName = 'zhangshiqiang1'
pwd = 'Zx258258'

encPwd = rsa.encrypt(retMessage,pwd)
print(encPwd)


login = 'http://jxdxfz.zj.chinamobile.com/public/LOGIN/loginIn'
headers['Cookie'] = sessionList[0]


#登陆
postData = {}
postData['userCode'] = userName
postData['userPwd'] = encPwd
postData['verifyCode'] =''

response = requests.post(login,data=postData,headers=headers)
content = response.content.decode()
parse = json.loads(content)
print(parse['retMessage'])








