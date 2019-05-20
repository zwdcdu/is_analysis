#!/usr/bin/env python
# coding=utf-8
"""
【Flask】前端RSA加密后端Python解密示例:
http://blog.csdn.net/yannanxiu/article/details/76436032
"""

# pip3 install pycrypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
import base64

#公钥和私钥对象:
public_key = ''
private_key = ''
#公钥和私钥字符串:
public_key_str = ''
private_key_str = ''
'''
创建公钥和私钥两个密钥文件，这两个文件永久存储起来,看作是配置文件
步骤说明：
1、从 Crypto.PublicKey 包中导入 RSA，创建一个密码
2、生成 1024/2048 位的 RSA 密钥
3、调用 RSA 密钥实例的 exportKey 方法，传入密码、使用的 PKCS 标准以及加密方案这三个参数。
4、将私钥写入磁盘的文件。
5、使用方法链调用 publickey 和 exportKey 方法生成公钥，写入磁盘上的文件。
'''

def create_rsa_key(password="123456"):
    key = RSA.generate(1024)
    encrypted_key = key.exportKey() #passphrase=password, pkcs=8,protection="scryptAndAES128-CBC")
    with open("my_rsa_private.pem", "wb") as f:
        f.write(encrypted_key)
    with open("my_rsa_public.pem", "wb") as f:
        f.write(key.publickey().exportKey())

# 从my_rsa_public.pem和my_rsa_private.pem文件中分别读取公钥和私钥字符串,之前必须运行create_rsa_key()创建两个密钥文件.
def ReadKeyStr(password="123456"):

    #指定以下4个变量为全局变量
    global  public_key,private_key,public_key_str,private_key_str

    public_key_str = open("my_rsa_public.pem").read()
    # 读取私钥字符串
    private_key_str = open("my_rsa_private.pem").read()

    #读取公钥对象
    public_key = RSA.importKey(public_key_str)

    # 读取私钥字符串
    password_bin = password.encode('utf-8')
    private_key = RSA.importKey(private_key_str, passphrase=password_bin)

# 加密,输入的password是普通字符串,输出是用公钥加密后的base64字符串
def encrypt(password):
    #生成公钥对象: cipher_rsa
    cipher_rsa = PKCS1_v1_5.new(public_key)

    #string=>bytes[]
    password_bin=password.encode('utf-8')
    #给密码加密,返回的en_data是二进制流bytes[]
    data = cipher_rsa.encrypt(password_bin)
    #bytes==>string(base64)
    data_base64 = base64.b64encode(data)
    #查看data的base64格式字符串  b64encode: bytes[]==>string
    #print(len(data), data_base64)
    return data_base64

#根据私钥,将base64格式字符串encrypt_base64_str解密为原始字符串
#通常encrypt_base64_str来自网页请求
def decrypt(encrypt_base64_str):
    # 生成私钥对象: cipher_rsa
    cipher_rsa = PKCS1_v1_5.new(private_key)

    #base64 string ==> bytes[]
    data_bin=base64.b64decode(encrypt_base64_str)
    # 解密,注意 en_data是bytes[]
    data_bin = cipher_rsa.decrypt(data_bin, None)

    #解密出的是bytes,byes==>string
    if data_bin:
        data=data_bin.decode('utf-8')
    else:
        print('data_bin is none!')
        data=''
    return data

#测试
def encrypt_and_decrypt_test(password):
    data = decrypt(encrypt(password))
    print('原始密码:{0},\n解密密码:{1}，\n结果：{2}'.format(password,data,('正确' if password==data else '错误')))

if __name__ == '__main__':
    create_rsa_key() #只运行一次，创建两个永远的密钥文件
    ReadKeyStr()
    enstr='bh51Q/m3cYhatFhYfzqmAIUYS54FEXqzoeAzSVg8SXhGuAz0wa0KJyr7CThINdlrnyhsesyFXn1ABQIyNI4qDyIWfVd21kckAvtpgi1xv27x0f2cFWLYr3AdFgNG0P4tgZ74/TnJf3Ea8Nz7sJnbFwcb/Z4RPWq/OmOggjZSEUU='
    print(decrypt(enstr))
    encrypt_and_decrypt_test('abc中国中华人民共和国中华人民共和国中华人民共和国中华人民共和国123  456//品++')