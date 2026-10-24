from pathlib import Path
import json
import html,re
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
data=json.loads((OUT/'plan.json').read_text())
template=(OUT/'planner.template.html').read_text().replace('__PLANNER_CSS__',(OUT/'planner.css').read_text())
payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
(ROOT/'planner.html').write_text(template.replace('__PLANNER_DATA__',payload))
source=(ROOT/'Resources/phase-01/organic-bridge-check.md').read_text()
questions,answers=source.split('\n---\n',1)
def paragraphs(s):
 result=[];listing=False
 for line in s.splitlines():
  if not line.strip():continue
  m=re.match(r'^(\d+)\. (.*)',line)
  if m:
   if not listing:result.append('<ol>');listing=True
   result.append('<li>'+html.escape(m[2])+'</li>');continue
  if listing:result.append('</ol>');listing=False
  if line.startswith('# '):result.append('<h1>'+html.escape(line[2:])+'</h1>')
  else:result.append('<p>'+html.escape(line.replace('**',''))+'</p>')
 if listing:result.append('</ol>')
 return '\n'.join(result)
check='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Organic bridge readiness check</title><style>__READING_CSS__</style><main><a href="../../planner.html">← Back to planner</a> <button onclick="window.print()" style="float:right">Print</button>'''+paragraphs(questions)+'<details><summary>Reveal answers after attempting</summary>'+paragraphs(answers)+'</details></main></html>'
check=check.replace('__READING_CSS__',(OUT/'reading.css').read_text())
(ROOT/'Resources/phase-01/organic-bridge-check.html').write_text(check)
maths_path=ROOT/'Resources/phase-01/maths-precalculus-bridge.html'
maths_page=re.sub(r'<style>.*?</style>',lambda _: '<style>'+(OUT/'reading.css').read_text()+'</style>',maths_path.read_text(),count=1,flags=re.S)
maths_path.write_text(maths_page)
print('Built planner.html — fully embedded data, no network required for the interface.')
