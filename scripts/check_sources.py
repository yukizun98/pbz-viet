#!/usr/bin/env python3
"""Kiểm tra metadata/hash nội dung trang công khai; không sao chép hay đăng toàn văn.
Không vượt robots; kiểm tra thủ công điều khoản/robots của mỗi trang trước khi thêm URL.
Nếu nguồn chặn truy cập, báo lỗi và giữ trạng thái cũ.
"""
import datetime as dt
import hashlib
import json
import re
import time
import urllib.request
import urllib.error
import urllib.robotparser
from urllib.parse import urlsplit
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

USER_AGENT='PBZ-Viet-Source-Monitor/0.1'
ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'state/source_state.json'
UPDATES=ROOT/'data/updates.json'
# Chỉ thêm trang sau khi xác minh có quyền/điều kiện truy cập tự động.
WATCH=[
    {'url':'https://www.playstation.com/ja-jp/games/phantom-blade-zero/','label':'PlayStation Nhật · PBZ'},
    {'url':'https://kungfupunk.com/names','label':'Kungfupunk · Tên Trung–Anh'},
    {'url':'https://kungfupunk.com/bosses','label':'Kungfupunk · Boss'},
]

class MainReader(HTMLParser):
    def __init__(self):
        super().__init__();self.in_main=0;self.main_seen=False;self.skip=0;self.text=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','noscript','svg'):self.skip+=1
        if tag=='main':self.in_main+=1;self.main_seen=True
    def handle_endtag(self,tag):
        if tag in ('script','style','noscript','svg'):self.skip=max(0,self.skip-1)
        if tag=='main':self.in_main=max(0,self.in_main-1)
    def handle_data(self,data):
        if not self.skip and self.in_main:self.text.append(data)

def allowed_by_robots(url):
    parts=urlsplit(url)
    robots_url=f'{parts.scheme}://{parts.netloc}/robots.txt'
    try:
        with urllib.request.urlopen(urllib.request.Request(robots_url,headers={'User-Agent':USER_AGENT}),timeout=12) as r:
            rules=r.read(200_000).decode('utf-8','replace').splitlines()
    except urllib.error.HTTPError as e:
        if e.code in (404,410): return True
        raise RuntimeError(f'Không xác minh được robots.txt ({e.code})')
    except Exception as e:
        raise RuntimeError(f'Không đọc được robots.txt: {e}')
    rp=urllib.robotparser.RobotFileParser();rp.parse(rules)
    return rp.can_fetch(USER_AGENT,url)

def snapshot(url):
    if not allowed_by_robots(url): raise PermissionError('robots.txt không cho phép tự động truy cập URL này')
    req=urllib.request.Request(url,headers={'User-Agent':USER_AGENT})
    with urllib.request.urlopen(req,timeout=20) as r:
        raw=r.read(2_000_001)
    if len(raw)>2_000_000:raise ValueError('Trang lớn hơn giới hạn 2 MB; bỏ qua để tránh tải quá mức')
    html=raw.decode('utf-8','replace')
    parser=MainReader();parser.feed(html)
    if not parser.main_seen:raise ValueError('Không tìm thấy thẻ main; cần chỉnh parser thủ công, không đoán nội dung')
    normalized=re.sub(r'\s+',' ',unescape(' '.join(parser.text))).strip()
    if len(normalized)<150:raise ValueError('Nội dung chính quá ngắn / có thể bị chống bot')
    return hashlib.sha256(normalized.encode()).hexdigest()

def run():
    state=json.loads(STATE.read_text('utf-8'))
    updates=json.loads(UPDATES.read_text('utf-8'))
    now=dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    for item in WATCH:
        url=item['url']
        try:
            fingerprint=snapshot(url)
            old=state.get(url)
            if old and old.get('sha256')!=fingerprint:
                updates.append({'url':url,'title':item['label']+' đã thay đổi','detected_at':now,'status':'Chờ xác minh và biên tập tiếng Việt'})
                print('CHANGED',url)
            elif old is None:print('BASELINE',url)
            else:print('UNCHANGED',url)
            state[url]={'sha256':fingerprint,'last_checked':now}
        except Exception as ex:
            print('ERROR',url, str(ex),'-- giữ nguyên trạng thái cũ')
        time.sleep(3)
    STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    UPDATES.write_text(json.dumps(updates[-50:],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':run()
