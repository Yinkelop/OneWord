#coding=utf-8
"""
灵感来自安卓端的一言

本脚本制作者:
耀星
一言1.5
"""
#导入
import requests,json,random,re,socket
#正则表达式
fenjson=re.compile(r'{.*}',re.S)

#定义全局变量
a=True
#文件地址
wengjian=".一言源.json"
#判断是否联网的网址
website="www.baidu.com",443
#函数
def main():
    q=isNetOK(website)
    if q:
         wjdata,jh=jiexi(wengjian)
         #随机源,由这个得到随机的yid
         sjy=random.randint(1,len(wjdata))
         try:
             data,sentence,author,resultType,name=request(wjdata,str(sjy),jh)
             sentence,author=jsonjx(data,sentence,author)
             show(sentence,author)
         except Exception as e:
             pass



#解析本地文件,返回字典
def jiexi(wengjian):
    try:
        jh=set()
        wjdata=json.load(open(wengjian))
        #print(type(wjdata))
        #print(type(wjdata[0]))
        for item in wjdata:
           jh.add(item.get("apiId"))
        return wjdata,jh
    except Exception as e:
        print('出错了:',e)
#发送请求，返回响应
def request(wjdata,sjy,jh):
    headers={
    	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
	           	}
    if sjy in jh:
       sjy=eval(sjy)-1
       url=wjdata[sjy]["apiAddress"]
       name=wjdata[sjy]["apiName"]
       sentence=wjdata[sjy]["apiHitokotoKey"]
       author=wjdata[sjy]["apiSourceKey"]
       resultType=wjdata[sjy]["resultType"]
       data=requests.get(url,headers=headers,timeout=5)
       data.encoding='utf-8'
       return data.text,sentence,author,resultType,name
    else:
        print('出错了,可能是.json文件出错了')
#解析json数据
def jsonjx(data,sentence,author):
    zd=json.loads(data)
    sentence=zd[sentence]
    author=zd.get(author)
    return sentence,author

#命令行显示
def show(sentence,author):
    if a==True and author!=None:
        print(sentence+'\n\t\t\t\t---'+author)
    else:
        print(sentence)




#判断是否联网
def isNetOK(testserver):
  s=socket.socket()
  s.settimeout(3)
  try:
    status = s.connect_ex(testserver)
    if status == 0:
      s.close()
      return True
    else:
      return False
  except Exception as e:
    return False
#入口
if __name__=="__main__":
    main()
