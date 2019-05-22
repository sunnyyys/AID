'''
    ftp客户端
'''
from socket import *
import sys,time

HOST='127.0.0.1'
PORT=8888
ADDR=(HOST,PORT)
#具体功能封装成类
class FtpClient:
    def __init__(self,s):
        self.s=s

    def do_list(self):
        self.s.send(b'L')#发送请求
        data=self.s.recv(128).decode()
        if data =='OK':#表示请求成功
            data=self.s.recv(4096)
            print(data.decode())
        else:
            print('data')
    def do_quit(self):
        self.s.send(b'Q')
        self.s.close()
        sys.exit('谢谢使用')
    def do_get(self,filename):
        self.s.send(('G '+filename).encode())
        data=self.s.recv(128)
        if data=='OK':
            fd=open(filename,'wb')
            while True:
                data=self.s.recv(1024)
                if data==b'##':
                    break
                fd.write(data)
            fd.close()
        else:
            print(data)

    def do_put(self,filename):
        # self.s.send(('P '+filename).encode())
        # data=self.s.recv(128)
        # if data=='OK':
        try:
            fd=open(filename,'rb')
        except Exception:
            print('没有该文件')
            return
        filename = filename.split('/')[-1]
        self.s.send(('P ' + filename).encode())
        data = self.s.recv(128).decode()
        if data == 'OK':
            while True:
                d=fd.read(1024)
                if not d:
                    time.sleep(0.1)
                    self.s.send(b'##')
                    break
                self.s.send(d)
            fd.close()
        else:
            print(data)


#发起请求
def request(s):
    ftp=FtpClient(s)

    while True:
        print('\n-----------命令选项------------')
        print('\n----------- list ------------')
        print('\n-----------get file------------')
        print('\n-----------put file------------')
        print('\n------------ quit ------------')
        cmd=input('输入命令:')
        if cmd=='list':
            ftp.do_list()
        elif cmd.strip()=='quit':
            ftp.do_quit()
        elif cmd[:3]=='get':
            filename=cmd.strip().split(' ')[-1]
            ftp.do_get(filename)
        elif cmd[:3]=='put':
            filename=cmd.strip().split(' ')[-1]
            ftp.do_put(filename)
#网络连接
def main():
    s=socket()
    try:
        s.connect(ADDR)
    except Exception as e:
        print('连接服务器失败')
        return
    else:
        print('''*************************************
                    data  file  image
        ''')
        cls=input('请输入文件种类:')
        if cls not in ['data','file','image']:
            print('Sorry input Error!!')
            return
        else:
            s.send(cls.encode())
            request(s)
if __name__=='__main__':
    main()







