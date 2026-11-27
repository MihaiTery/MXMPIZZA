"""Editorial corrections for the client-supplied menu; source DOCX files stay unchanged."""
import re

NAMES = {
 'p01':'Pizza Margherita','p02':'Pizza Prosciutto Cotto','p03':'Pizza Prosciutto e Funghi',
 'p04':'Pizza Quattro Stagioni','p05':'Pizza Capricciosa','p06':'Pizza Salami',
 'p07':'Pizza Diavola','p08':'Pizza Quattro Formaggi','p09':'Pizza Hot Cheese',
 'p10':'Pizza Carnivora','p11':'Pizza Tonno e Cipolla','p12':"Pizza Miky's",
 'p13':'Pizza Carbonara','p14':'Pizza Pollo','p15':'Pizza vegetariană',
 'p16':'Shaorma de pui mică','p17':'Shaorma de pui mare',
 'p18':'Shaorma de vită-berbecuț mică','p19':'Shaorma de vită-berbecuț mare',
 'p20':'Shaorma mixtă mică','p21':'Shaorma mixtă mare',
 'p22':'Kebab de pui','p23':'Kebab de vită-berbecuț','p24':'Kebab mixt',
 'p25':'Shaorma cheese cu pui','p26':'Shaorma cheese cu vită-berbecuț',
 'p27':'Meniu crispy','p28':'Meniu aripioare de pui','p29':'Meniu aripioare picante',
 'p30':'Meniu nuggets de pui','p31':'Șnițel gratinat Diavola',
 'p32':'Șnițel gratinat Carbonara','p33':'Șnițel gratinat Quattro Formaggi',
 'p34':'Paste arrabbiata','p35':'Paste amatriciana','p36':'Paste carbonara',
 'p37':'Paste cu pui și ciuperci','p38':'Paste quattro formaggi',
 'p39':'Salată bulgărească','p40':'Salată cu ton','p41':'Salată Caesar','p42':'Salată de vară',
 'p43':'Baclavă cu ciocolată','p44':'Baclavă clasică','p45':'Baclavă cu cireșe',
 'p46':'Lava Cake','p47':'Cheesecake','p48':'Tiramisu',
 'p49':'Coca-Cola','p50':'Fanta','p51':'Sprite','p52':'Schweppes Mandarine',
 'p53':'Schweppes Bitter Lemon','p54':'Apă plată','p55':'Apă minerală',
}

REPLACEMENTS = [
 ('ulei malsine','ulei de măsline'),('ulei masline','ulei de măsline'),
 ('sos maioneza cu usturoi','sos de maioneză cu usturoi'),
 ('sos maioneza','sos de maioneză'),('maioneza cu usturoi','maioneză cu usturoi'),
 ('sos usturoi','sos de usturoi'),('sos pizza','sos de pizza'),
 ('sos rosii','sos de roșii'),('sos anatolya','sos Anatolya'),
 ('salata verde','salată verde'),('schnitzel pui','șnițel de pui'),
 ('piept pui','piept de pui'),('aripioare pui','aripioare de pui'),
 ('nuggets pui','nuggets de pui'),('pui-vita-berbecut','pui și vită-berbecuț'),
 ('vita-berbecut','vită-berbecuț'),('scalie parmezan','fulgi de parmezan'),
 ('branza feta','brânză feta'),('sare si piper','sare și piper'),
 ('ceapa rosie','ceapă roșie'),('ardei capia','ardei capia'),
 ('cartofi prajiti','cartofi prăjiți'),('gran cucina','Gran Cucina'),
 ('emmentaller','emmentaler'),('jalapeno','jalapeño'),
 ('nucsoara','nucșoară'),('carnati','cârnați'),('sunca','șuncă'),
 ('masline','măsline'),('rosii','roșii'),('castraveti','castraveți'),
 ('lamaie','lămâie'),('chifla','chiflă'),('parmezan','parmezan'),
]

# The document says "ciuperci 20" without a unit. Keep the number but do not infer grams.
def polish_description(raw):
 if not raw.strip():
  return ''
 text=re.sub(r'\s+', ' ', raw.strip())
 total_match=re.search(r'\btotal\s*(\d+)\s*g\b', text, flags=re.I)
 total=total_match.group(1) if total_match else None
 if total_match:
  text=text[:total_match.start()]
 text=text.strip(' ,.;')
 text=re.sub(r'\bm[aă]sline,\s*(\d+)\s*g\b',r'masline \1 g',text,flags=re.I)
 for old,new in REPLACEMENTS:
  text=re.sub(re.escape(old),new,text,flags=re.I)
 text=re.sub(r'(?<=[a-zăâîșț])(?=\d)', ' ', text, flags=re.I)
 text=re.sub(r'(?<=\d)\s*g\b',' g',text)
 text=re.sub(r'(\d+ g)\s+(?=[a-zăâîșțA-ZĂÂÎȘȚ])',r'\1, ',text)
 text=re.sub(r'\s*,\s*',', ',text)
 text=re.sub(r',\s*,+',', ',text)
 text=re.sub(r'\s+',' ',text).strip(' ,.;')
 text=text[0].lower()+text[1:] if text else text
 result='Ingrediente: '+text+'.'
 if total:
  result+=f' Total: {total} g.'
 return result


def polish_item(item):
 item=dict(item)
 item['name']=NAMES.get(item['id'],item['name'])
 item['description']=polish_description(item['description'])
 if item['id']=='p04':
  item['description']=item['description'].replace('ciuperci 20','ciuperci (cantitate de confirmat)')
 if item['id'] in ('p20','p21'):
  item['description']=item['description'].replace('pui, vită-berbecuț','pui și vită-berbecuț')
 return item


def pizza_50_description(description):
 ingredients=description.split(' Total: ')[0].removeprefix('Ingrediente: ').rstrip('.')
 ingredients=re.sub(r'\b\d+\s*g\b','',ingredients)
 ingredients=re.sub(r'\s*\(cantitate de confirmat\)','',ingredients)
 # One source quantity has no unit ("ciuperci 20"); do not copy it into a 50 cm recipe.
 ingredients=re.sub(r'\bciuperci\s+20\b','ciuperci',ingredients)
 ingredients=re.sub(r'\s*,\s*',', ',ingredients)
 ingredients=re.sub(r'\s+',' ',ingredients).strip(' ,.;')
 return f'Ingrediente: {ingredients}. Gramajul pentru 50 cm se confirmă.'
