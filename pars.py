#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import configparser
import csv
import os
import sys
import time

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"



cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    banner()
    print(re+"[!] run python3 setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    banner()
    client.sign_in(phone, input(gr+'[+] Enter the code: '+re))

os.system('clear')
banner()
chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup:
            groups.append(chat)
    except:
        continue

print(gr+'[+] Choose a group to scrape members:'+re)
i = 0
for g in groups:
    print(gr+'['+cy+str(i)+gr+']'+cy+' - '+ g.title)
    i += 1

print('')
g_index = input(gr+"[+] Enter a Number: "+re)
try:
    target_group = groups[int(g_index)]
except (IndexError, ValueError):
    print(re+"[!] Invalid group number.")
    sys.exit(1)

print(gr+'[+] Fetching Members...')
time.sleep(1)
all_participants = client.get_participants(target_group, aggressive=True)

print(gr+'[+] Saving In file...')
time.sleep(1)
with open("members.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
    for user in all_participants:
        username = user.username if user.username else ""
        first_name = user.first_name if user.first_name else ""
        last_name = user.last_name if user.last_name else ""
        name = (first_name + ' ' + last_name).strip()
        writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])
print(gr+'[+] Members scraped successfully.')