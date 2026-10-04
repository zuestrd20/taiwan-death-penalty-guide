from html.parser import HTMLParser
from pathlib import Path
import json,re
root=Path(__file__).resolve().parent.parent
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.external=[];self.section=[];self.active=None;self.details=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id'in a:self.ids.append(a['id'])
  if tag=='a':
   self.links.append(a.get('href',''))
   if a.get('href','').startswith('http'):self.external.append(a['href'])
  if tag=='section':self.section.append(a.get('id'))
p=Parser();text=(root/'index.html').read_text();p.feed(text)
assert len(p.ids)==len(set(p.ids)),'duplicate ids'
for link in p.links:
 if link.startswith('#'):assert link[1:] in p.ids,link
 elif not link.startswith('http'):assert (root/link).exists(),link
assert len(set(p.external))>=140
for chunk in text.split('<details')[1:]:
 body=chunk.split('</details>')[0]
 assert 'https://' in body,'Missing evidence links in detail panel'
for id in ['taiwan','world','alliance','evidence','experience','law','sources']:assert id in p.section
for phrase in ['9月至查核日未驗證','未顯著不是等效證明','非個案法律意見','2001年執行1人','07-21公告','2026-09-18']:
 assert phrase in text,phrase
assert 'https://www.cy.gov.tw/IntraExternalBBSContent' not in text
assert len(list((root/'data').glob('*.pdf')))==0
for match in re.findall(r'<script[^>]*src="([^"]+)"',text):assert (root/match).exists()
# Every curated card contains its own evidence link; methods cards are editorial.
for chunk in text.split('<article class="card searchable">')[1:]:assert 'https://' in chunk.split('</article>')[0]
print('PASS HTML: unique ids, internal links, local assets, 140+ direct sources, card/detail citation coverage, caveats, no republished PDFs')
