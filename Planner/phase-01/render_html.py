from pathlib import Path
import json
import html,re
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
data=json.loads((OUT/'plan.json').read_text())
template=(OUT/'planner.template.html').read_text()
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
check='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Organic bridge readiness check</title><style>body{font:16px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#263047;background:#f7f8fb;margin:0}main{max-width:850px;margin:35px auto;padding:30px 40px;background:white;border:1px solid #e5e9f0;border-radius:15px}h1{font-size:28px;line-height:1.25}li{padding:8px 0 8px 6px}summary{cursor:pointer;font-weight:700;color:#6545a5;padding:15px;background:#f2edfb;border-radius:9px}a{color:#4267cf}details{margin-top:35px}button{font:inherit;padding:7px 12px;border:1px solid #ddd;border-radius:7px;background:white;cursor:pointer}@media(max-width:600px){main{margin:0;padding:25px 20px;border-radius:0}li{font-size:14px}}@media print{details{display:block}button{display:none}}</style><main><a href="../../planner.html">← Back to planner</a> <button onclick="window.print()" style="float:right">Print</button>'''+paragraphs(questions)+'<details><summary>Reveal answers after attempting</summary>'+paragraphs(answers)+'</details></main></html>'
(ROOT/'Resources/phase-01/organic-bridge-check.html').write_text(check)
print('Built planner.html — fully embedded data, no network required for the interface.')
