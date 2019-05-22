'''
ftp文件传输器
'''
from threading import *
from socket import *
import sys,os
import time

HOST='0.0.0.0'
PORT=8888
ADDR=(HOST,PORT)
FTP='/home/tarena/FTP/'#文件库路径
#全局变量
#将请求功能封装为类
class FtpServer:
    def __init__(self,c,FTP_PATH):
        self.c=c
        self.FTP_PATH=FTP_PATH
    def do_list(self):
        files=os.listdir(self.FTP_PATH)
        if not files:
            self.c.send('该文件类别为我空'.encode())
            return
        else:
            self.c.send(b'OK')
            time.sleep(0.1)

        fs=''
        for file in files:
            if file[0]!='.'and os.path.isfile(self.FTP_PATH+file):
                fs+=file+'\n'
        self.c.send(fs.encode())
        # self.c.send(b'##')

    def do_get(self,filename):
        try:
            fd=open(self.FTP_PATH+filename,'rb')
        except Exception:
            self.c.send('文件不存在'.encode())
            return
        else:
            self.c.send(b'OK')
            time.sleep(0.1)
        while True:
            data=fd.read(1024)
            if not data:
                time.sleep(0.1)
                self.c.send(b'##')
                break
            self.c.send(data)

    def do_put(self,filename):
        if os.path.exists(self.FTP_PATH+filename):
                self.c.send('文件已存在'.encode())
                return
        self.c.send(b'OK')
        fd2=open(self.FTP_PATH+filename,'wb')
        while True:
            data=self.c.recv(1024)
            if data==b'##':
                break
            fd2.write(data)
        fd2.close()

#客户端请求处理函数
def handle(c):
    cls=c.recv(1024).decode()
    FTP_PATH=FTP+cls+'/'
    ftp = FtpServer(c, FTP_PATH)
    while True:
        #接收客户端应用请求
        data=c.recv(1024).decode()
        print(FTP_PATH,':',data)
        #如果客户端断开返回data为空
        if not data or data[0]=='Q':
            return
        elif data[0]=='L':
            ftp.do_list()
        elif data[0]=='G':
            filename=data.split(' ')[-1]
            ftp.do_get(filename)
        elif data[0]=='P':
            filename=data.split(' ')[-1]
            ftp.do_put(filename)
#网络搭建通过函数完成
def main():
    s=socket()
    s.bind(ADDR)
    s.listen(8)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    print('listen the port 8888...')
    while True:
        try:
            c, addr = s.accept()
        except KeyboardInterrupt:
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue
        print('连接的客户端:',addr)
        #创建线程处理请求
        client =Thread(target=handle, args=(c,))
        client.setDaemon(True)
        client.start()

if __name__=='__main__':
    main()




