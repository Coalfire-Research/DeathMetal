#!/usr/bin/env python3

import socket
import ssl
import time
import hashlib
import random
import string

def hex_md5(data):
    return hashlib.md5(data.encode('utf-8')).hexdigest()

def itobl(i, c=1):
    return i.to_bytes(c, 'little')

def itobb(i, c=1):
    return i.to_bytes(c, 'big')

def btobl(i, c=1):
    return i + (b'\x00' * (c - len(i)))

def create_redir_session(hostname, port, username, password, service):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(True)
    sock.connect((hostname, int(port)))
    
    def send(data):
        sock.sendall(data)

    def recv(count=1024):
        return sock.recv(count)

    send(b'\x10\x00\x00\x00' + service.encode())
    time.sleep(0.005) # Seems to fix 'random' rst issue
    rv = recv()

    if chr(rv[0]) != '\x11': # StartRedirectionSessionReply
        raise Exception('auth', 'did not receive StartRedirectionSessionReply code')

    if chr(rv[1]) != '\x00':
        raise Exception('auth', 'StartRedirectionSessionReply returned non-zero status code')

    send(b'\x13\x00\x00\x00\x00\x00\x00\x00\x00') # Query authentication support
    rv = recv()

    if chr(rv[0]) != '\x14': # AuthenticateSessionReply
        raise Exception('auth', 'did not receive AuthenticateSessionReply code')

    auth_type = chr(rv[4])
    status = chr(rv[1])
    if auth_type != '\x00' or status != '\x00':
        raise Exception('auth', 'unhandled authentication protocol in AuthenticateSessionReply')

    auth_target = b'/RedirectionService'
    data = b'\x13\x00\x00\x00\x04\x20\x00\x00\x00' + bytes([len(username)]) + username.encode() + b'\x00\x00'
    data += itobl(len(auth_target)) + auth_target + b'\x00\x00\x00\x00'
    send(data)
 
    rv = recv()
    
    # TODO (12_17_18-pancho) clean up offset arithmetic and pretty much all from here to return
    realm_len = int(rv[9])
    realm = rv[10:10+realm_len]

    nonce_len = int(rv[10+realm_len])
    nonce = rv[11+realm_len:11+realm_len+nonce_len] # eww, I got lazy with this one
    
    cnonce = ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
        
    p1 = username + ':' + realm.decode() + ':' + password
    p2 = nonce.decode() + ':' + '00000002' + ':' + cnonce + ':' + 'auth' # not sure what the 00000002 thing is about
    p3 = 'POST' + ':' + auth_target.decode()
    cr = hex_md5(hex_md5(p1) + ':' + p2 + ':' + hex_md5(p3)) 
    print('Challenge answer is: ' + cr) 
    
    auth_data =  itobl(len(username))+ username.encode()
    auth_data += itobl(realm_len) + realm
    auth_data += itobl(nonce_len) + nonce
    auth_data += itobl(len(auth_target)) + auth_target
    auth_data += itobl(len(cnonce)) + cnonce.encode()
    auth_data += b'\x08' + b'00000002'
    auth_data += itobl(len(cr)) + cr.encode()
    auth_data += b'\x04' + b'auth'
    
    data = b'\x13\x00\x00\x00\x04'
    data += itobl(len(auth_data), 4)
    data += auth_data
    send(data)
    rv = recv()

    if (rv != b'\x14\x00\x00\x00\x04\x00\x00\x00\x00'):
        print('authentication failed, check creds')
        return

    return sock


