from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import json,re
root=Path('/home/server1/mxm-food')
files=[('pizza','Meniu Pizza 32 cm.docx'),('shaorma','Shaorma fastfood bucuresti site.docx'),('meniu','Meniu fastfood bucuresti.docx'),('paste','meniu paste fastfood site.docx'),('salate','Salate fast food bucuresti site.docx'),('deserturi','Deserturi si bauturi fastfood bucuresti site.docx')]
items=[]
for category,name in files:
 with ZipFile(root/'source-docs'/name) as z: doc=ET.fromstring(z.read('word/document.xml'))
 ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
 lines=[''.join(x.text or '' for x in p.findall('.//w:t',ns)).strip() for p in doc.findall('.//w:p',ns)]
 subcat=category
 for line in lines:
  if not line: continue
  if category=='deserturi':
   if line.lower().strip()=='bauturi':subcat='bauturi';continue
   title=line.strip(); detail=''
  else:
   if line.lower().strip()=='meniu pizza':continue
   line=re.sub(r'^\s*\d+\.\s*','',line)
   parts=re.split(r'\s*[.(]\s*',line,1)
   title=parts[0].strip().rstrip('. ')
   detail=parts[1].strip(' )') if len(parts)>1 else ''
  if title:
   detail=re.sub(r'\s+',' ',detail).replace('ciuoerci','ciuperci').replace('uesturoi','usturoi').replace('ketchp','ketchup')
   items.append({'id':f'p{len(items)+1:02d}','category':subcat,'name':title[0].upper()+title[1:],'description':detail,'price':None,'available':None})
(root/'menu.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
print(len(items))
