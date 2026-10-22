from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
data=json.loads((OUT/'plan.json').read_text())
template=(OUT/'planner.template.html').read_text()
payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
(ROOT/'planner.html').write_text(template.replace('__PLANNER_DATA__',payload))
print('Built planner.html — fully embedded data, no network required for the interface.')
