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
# Product extensions requested for the website preview. The 32 cm recipes are the source;
# exact 50 cm weights and the two soup recipes require client confirmation.
pizza50=[]
for n, item in enumerate((x for x in items if x['category']=='pizza'), 1):
 ingredients=re.sub(r'\btotal\s*\d+\s*g\b.*','',item['description'],flags=re.I)
 ingredients=re.sub(r'\b\d+\s*g?\b','',ingredients)
 ingredients=re.sub(r'\s*,\s*',', ',ingredients).strip(' ,.;')
 pizza50.append({'id':f'p50-{n:02d}','category':'pizza50','name':item['name']+' 50 cm','description':f'{ingredients}. Gramajul pentru 50 cm se confirmă.','price':None,'available':None,'mock':True,'badge':'Variantă propusă'})
soups=[
 {'id':'soup-01','category':'supe','name':'Supă cremă de roșii','description':'Ingrediente: usturoi, ceapă, pulpă de roșii, busuioc, ulei de măsline, sare, piper și crutoane.','price':None,'available':None,'source':'client'},
 {'id':'soup-02','category':'supe','name':'Supă cremă de ciuperci','description':'Ingrediente: ceapă, ulei de măsline, unt, ciuperci champignon, hribi, nucșoară, Gran Cucina, crutoane, sare și piper alb.','price':None,'available':None,'source':'client'},
 {'id':'soup-03','category':'supe','name':'Supă cremă de legume','description':'Ingrediente: păstârnac, cartof, morcov, țelină, Knorr, ulei de măsline, ceapă, usturoi, pătrunjel, ardei gras, unt, Gran Cucina, sare, piper și crutoane.','price':None,'available':None,'source':'client'}
]
pizza_end=next(i for i,x in enumerate(items) if x['category']!='pizza')
items[pizza_end:pizza_end]=pizza50
soup_at=next(i for i,x in enumerate(items) if x['category']=='deserturi')
items[soup_at:soup_at]=soups
(root/'menu.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
print(len(items))
