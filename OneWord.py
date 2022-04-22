#pylint:disable=W0123
#pylint:disable=W0105
#coding=utf-8

'''
灵感来自安卓端的一言
一言3.0重置版
本脚本制作者:
Yinkelop
'''
VERSION='3.0重置版'


#包导入
import os
import sys
import requests
from getopt import getopt
from random import randint
from json import load,loads



#全局变量
'''
FILENAME是一言源文件名称，更改一言源文件名称是请同时更改
FILEPATH会自动生成的一言源文件绝对路径，默认为源文件与当前python文件处于同一目录
注意:一言源文件需要与当前python文件处于同一目录才行
    否则执行时会出现找不到一言源文件的错误
但就是想把一言源文件放在其他目录，请把FILEPATH改成一言源文件的绝对路径
也可以使用-i参数指定
'''
FILENAME='.OneWord.json'
FILEPATH=(str(os.path.dirname(os.path.realpath(__file__)))+str(os.sep)+FILENAME)

CYCLE=1
SOURCE_ID=None
#终端宽度，用来排版的
SIZE=os.get_terminal_size().columns

#超时错误
X=0#为$true忽略，false提示

#定义函数
#主函数
def main():
    #获取终端传入的参数
    termux_param=termux_parameter()
    #解析终端传入的参数
    termux_param_jiexi(termux_param)
    #把一言源的json文件转换成python对象
    filedata=file_jiexi(FILEPATH)
    #解析上面的python对象，然后返回一个一言源，有指定返回指定，没指定随机返回
    yuan=object_jiexi(filedata,SOURCE_ID)
    #发出请求
    result=request(yuan,CYCLE)
    #终端显示
    show(result)

#获取终端的参数
def termux_parameter():
    #参数-h帮助，-v版本，-s循环数，-x忽略超时错误,-i指定源文件，-d指定源
    termux_param={'cycle':None,'source_file':None,'source_id':None}
    try:
        opts,args=getopt(sys.argv[1:],'vhxs:i:d:')
        del args
        error=''
        for op,value in opts:
            if op=='-s':
                try:
                    value=int(value)           
                    termux_param['cycle']=value
                except ValueError:
                    error+='-s,'
            elif op=='-i':
                if os.path.isfile(value):
                    termux_param['source_file']=value
                else:
                    error+='-i,'
            elif op=='-d':
                try:
                    value=int(value)            
                    termux_param['source_id']=value
                except ValueError:
                    error+='-d,'
            elif op=='-h':
                helper()
                os._exit(0)
            elif op=='-v':
                print('当前版本:',VERSION)
                os._exit(0)
            elif op=='-x':
                global X
                X=1
        if error!='':
            print('%s参数使用错误,已退出程序!使用-h查看帮助'%error)
            os._exit(0)
    except :
        print('错误，有参数无值,已退出程序!使用-h查看帮助')
        os._exit(0)
        
    return termux_param
#帮助
def helper():
    print('help'.center(SIZE,'-'))
    print('''
    参数说明:
        -s
        后面跟循环数，需要int类型
        -i
        指定一言源文件地址,后跟一言源文件地址，需要str类型
        -x
        忽略超时错误
        -d
        指定一言源文件中的源，由上到下按个数算，第一个是1，不是由apiId取得，apiId只是让你知道是第几个，没作用，现在只支持指定一个，需要int类型
        -h
        获取帮助，并关闭程序，不需要值
        -v
        获取版本号，并关闭程序,不需要值
    ''')
    print('end'.center(SIZE,'-'))
    
#终端参数解析
def termux_param_jiexi(termux_param):
    #声明全局变量
    global FILEPATH

    global CYCLE
    global SOURCE_ID
    
    #迭代termux_param
    for key,value in termux_param.items():
        if value != None:
            if key == 'source_file':
                FILEPATH=value
            elif key =='cycle':
                CYCLE=value
            elif key == 'source_id':
                SOURCE_ID=value
    
#一言源文件解析函数
def file_jiexi(filepath):
    file=open(filepath,'r')
    filedata=load(file)
    file.close()
    #返回一个列表，里面是字典
    return filedata
    
#解析一言源文件返回的对象
def object_jiexi(filedata,source_id):
    #判断是否超出
    if isinstance(source_id,int) and source_id<=len(filedata):
        if source_id<1:
            source_id=0
        else:
            source_id-=1
        idd=source_id
    else:
        idd=randint(0,len(filedata)-1)
    return filedata[idd]

#发出请求
def request(yuan,cycle):
    result={}
    for i in range(cycle):
        try:
            response=requests.get(url=yuan['apiAddress'],timeout=1)
            
            if yuan['resultType']=='json':
                response=loads(response.text)
                try:
                    source=response[yuan['apiSourceKey']]
                except:
                    source=None
                hitokoto=response[yuan['apiHitokotoKey']]
            elif yuan['resultType']=='text':
                try :
                    divide=yuan["apiSourceKey"]
                    source=(response.text).split(divide)[-1]
                    hitokoto=(response.text).split(divide)[:-1]
                except:
                    hitokoto=response.text
                    source=None
            result[hitokoto]=source
        except:
            if X:
                continue
            else:
                print('超时')
    return result

#终端显示
def show(result):
    for key,value in result.items():
        if value:
            print(key.ljust(SIZE))
            print(' '*(SIZE//3)+'--'+value)
        else:
            print(key.ljust(SIZE))
        if len(result)>1:
            print('-'*SIZE)


#程序执行
if __name__=='__main__':
    main()