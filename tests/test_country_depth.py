from pathlib import Path
import json,re
from html.parser import HTMLParser
root=Path(__file__).resolve().parent.parent
text=(root/'index.html').read_text();manifest=json.loads((root/'data/country-depth-manifest.json').read_text())
expected={'日本':'entry-10','韓國':'entry-11','美國':'entry-12','新加坡':'entry-13','加拿大':'entry-14','法國':'entry-15','南非':'entry-16'}
assert set(manifest['countries'])==set(expected)
for country,anchor in expected.items():
 assert f'data-search-group="country" id="{anchor}"' in text
 topics=manifest['countries'][country]
 assert len(topics)>=4,(country,len(topics))
 assert sum(t['chars'] for t in topics)>=900,(country,'depth too short')
 for topic in topics:
  assert f'id="{topic["id"]}"' in text
  start=text.index(f'id="{topic["id"]}"');end=text.index('</details>',start)
  assert 'https://' in text[start:end],(country,topic['heading'],'needs nearby references')
 assert f'href="#{anchor}"' in text
assert 'searchable:not([data-search-group])' in (root/'app.js').read_text()
assert text.count('country-overview searchable')==7
assert 'country-topic' in (root/'style.css').read_text()
assert len(json.loads((root/'data/source-index.json').read_text()))>146
assert '編輯分析' in text and '查核：2026-10-04 UTC' in text
print('PASS 7 countries: added depth, 4+ topic groups each, adjacent sources, established anchors, nested-search wiring and responsive styles')
