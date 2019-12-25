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
            'Host':'jxdxfz.zj.chinamobile.com',
           'Origin':'http://jxdxfz.zj.chinamobile.com',
           'Referer':'http://jxdxfz.zj.chinamobile.com/login',
           'User-Agent': userAgent
        }

response = requests.get(getKeyMaps,headers=headers)
content = response.content.decode()

print("获取密钥:%s" % content)

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
print("加密后密码:%s" % encPwd)


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


headers['Origin']=''
headers['Referer']= 'http://jxdxfz.zj.chinamobile.com/home.html'


#查询用户信息
getInfo = 'http://jxdxfz.zj.chinamobile.com/public/@uspa_operatorAction/getLoginedOperInfo'
response = requests.get(getInfo,headers=headers)
content = response.content.decode()
print("查询用户信息:%s" % content)
parse = json.loads(content)
managerId  = parse['rows']['code']
orgnazieId = parse['rows']['organizeId']
districtId = parse['rows']['districtId']
staffId    = parse['rows']['staffId']
ext1       = parse['rows']['ext1']

#查询上级ID
getbossId = 'http://jxdxfz.zj.chinamobile.com/public/Sec_StaffHandler/queryBossOrgId'
postData = {}
postData['orgId'] = orgnazieId;
response = requests.post(getbossId,data=postData,headers=headers)
content = response.content.decode()
parse = json.loads(content)
strBossOrgId = parse['rows']
strList = strBossOrgId.split(',',-1)
strList2 = strList[0].split(':',-1)
bossOrgId = strList2[1].strip("'")
print(bossOrgId)
'''if parse['retMessage'] == 'success':
   bossOrgId = ext1
'''
print("查询bossId:%s" % response.content.decode())


#查询区域
queryAreaList = 'http://jxdxfz.zj.chinamobile.com/public/YyCallListConfigHandler/queryAreaList'
postData = {}
postData['areaCode'] = districtId
response = requests.post(queryAreaList,data=postData,headers=headers)
content = response.content.decode()
parse = json.loads(content)
areaCode = parse['rows'][0]['areaCode']
print("查询区域:%s" % response.content.decode())
#查询操作规则
queryOperatorRole = 'http://jxdxfz.zj.chinamobile.com/public/Sec_StaffHandler/queryOperatorRole'
postData = {}
postData['staffId'] = staffId
response = requests.post(queryOperatorRole,data=postData,headers=headers)
content = response.content.decode()
parse = json.loads(content)
roleId = parse['rows']['roleId']
print("查询操作规则%s:" % response.content.decode())


#获取TokenInfo
getTokenInfo = 'http://jxdxfz.zj.chinamobile.com/public/DxZhQryHandler/GetZhTokenInfo'
postData = {}
postData['managerId'] = managerId
postData['staffId'] = staffId
postData['roleId'] = roleId
postData['areaCode'] = areaCode
postData['bossOrgId'] = bossOrgId
response = requests.post(getTokenInfo,data=postData,headers=headers)

print("获取TokenInfo:%s" % response.content.decode())


searchUserInfo = 'http://jxdxfz.zj.chinamobile.com/public/DxZhQryHandler/getActiveByActiveAll'
postData = {}
postData['teleNum'] = '15157441444'
postData['pageUrl'] = 'zhywcx6.htm'

response = requests.get(searchUserInfo,params=postData,headers=headers)
#print(response.content.decode())
parse = json.loads(response.content.decode())
basicUserInfo1 = parse['rows']['message']['basicUserInfo0']
