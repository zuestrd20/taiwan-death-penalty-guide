import os
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent.parent
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root)))
Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/'
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_EXECUTABLE','/usr/bin/chromium'),args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':1000});errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(url,wait_until='networkidle')
 assert page.locator('.bar').count()==30
 assert '201人' in page.locator('#range-summary').inner_text()
 page.screenshot(path='/tmp/dp-desktop.png')
 page.locator('#start-year').select_option('2000');page.locator('#end-year').select_option('2000')
 assert '17人' in page.locator('#range-summary').inner_text();assert '尚未完整' in page.locator('#year-detail').inner_text()
 page.locator('#reset-years').click();assert page.locator('.bar').count()==30
 page.locator('#search').fill('假釋');page.wait_for_timeout(250)
 assert page.locator('#search-results a').count()>0
 page.locator('#search-results a').first.click();assert page.locator('details[open]').count()>0
 page.locator('#clear-search').click();assert page.locator('#search-results a').count()==0
 page.locator('#search').fill('zzzznothing');page.wait_for_timeout(250);assert '找到 0' in page.locator('#search-status').inner_text()
 page.locator('#clear-search').click()
 page.locator('#global-filter').evaluate('(e)=>e.closest("details").open=true');page.locator('#global-filter').select_option('unknown');assert page.locator('.global-item').count()==4
 assert all(x=='+' for x in page.locator('.global-item strong').all_text_contents())
 page.locator('#global-filter').select_option('all');assert page.locator('.global-item').count()==17
 page.locator('#source-filter').select_option('學術／研究');assert page.locator('.source-item:visible').count()>0
 page.locator('#source-filter').select_option('all')
 for width in [1440,768,390,320]:
  page.set_viewport_size({'width':width,'height':844})
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'overflow at {width}'
  page.locator('details').evaluate_all('(els)=>els.forEach(e=>e.open=true)')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'open overflow at {width}'
 page.set_viewport_size({'width':390,'height':844});page.goto(url,wait_until='networkidle');page.screenshot(path='/tmp/dp-mobile.png')
 page.locator('#menu-toggle').click();assert page.locator('#menu-toggle').get_attribute('aria-expanded')=='true'
 page.locator('#nav a').first.click();assert page.locator('#menu-toggle').get_attribute('aria-expanded')=='false'
 page.locator('#menu-toggle').click();page.locator('#menu-toggle').click();assert page.locator('#menu-toggle').get_attribute('aria-expanded')=='false'
 page.screenshot(path='/tmp/dp-chart-mobile.png')
 # Direct anchor opens nested content. All static readings survive without JavaScript.
 page.goto(url+'#batch-data');assert page.locator('#batch-data').get_attribute('open') is not None
 nojs=b.new_context(java_script_enabled=False);np=nojs.new_page();np.goto(url);assert np.locator('details').count()>25;assert np.locator('a[href="data/taiwan_annual.csv"]').count()>0;nojs.close()
 assert not errors,errors
 b.close()
server.shutdown();print('PASS browser: desktop/mobile 1440/768/390/320; chart range/reset, search/no-result/clear, unknown filter, source filter, menu repeat/close, deep links, no-JS, no page errors or document overflow')
