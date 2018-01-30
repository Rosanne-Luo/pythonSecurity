#全连接扫描器 
#调用方式: python3 tcp_scan.py host port1,port2

import socket
import re
import threading
import argparse

#扫描指定的端口
def connScan(ip, port):
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((ip,port))
		print("%s:%d is open" % (ip,port))
		#获取banner信息
		s.send(b"violentPython\r\n")
		result=s.recv(100)
		print("recv:",result)
		s.close()
	except Exception as e:
		print("%s:%d is closed, and happend error:" % (ip,port), e)

#扫描指定host的一组端口
def portScan(host, ports):
	pattern="[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"
	if re.match(pattern, host):
		print("this is a ip address..")
	else:
		print("this is a domain name...")
		try:
			host=gethostbyname(host)
		except Exception as e:
			print("[*] can't resolve this domain name...")
	
	#设置socket连接超时时间为1s
	socket.setdefaulttimeout(1)
	for port in ports:
		print("[*] scan %s for host..." % port)
		t=threading.Thread(target=connScan, args=(host,int(port)))
		t.start()

parser=argparse.ArgumentParser()
parser.add_argument("host",help="specipfy target host")
parser.add_argument("ports",help="specipfy target hosts, and seperate each port with ','")
args=parser.parse_args()

host=args.host
ports=args.ports.split(',')
portScan("127.0.0.1", ports)
print('thread %s ended.' % threading.current_thread().name)