"""Add self-contained, mathematically aligned SVG stages without changing code."""
from pathlib import Path
import base64,xml.etree.ElementTree as E,json
BASE=Path(__file__).resolve().parent;ROOT=BASE/'inhalt/klasse7/programmieren'
TASKS=[
 {'id':'alg-1','title':'Welche Route trifft die Station?','minutes':45,'phases':[10,10,15,10],'project':'projekte/ALG-1-Start.xml','targets':[20]},
 {'id':'alg-2','title':'Gleiche Zahl – gleiche Wirkung?','minutes':60,'phases':[15,15,20,10],'project':'projekte/ALG-2-Start.xml','targets':[12]},
 {'id':'alg-3','title':'Welches Depot ist zuständig?','minutes':75,'phases':[15,15,30,15],'project':'projekte/ALG-3-Start.xml','targets':[40]},
 {'id':'alg-4','title':'Warum fährt der Rover immer weiter?','minutes':75,'phases':[10,15,35,15],'project':'projekte/ALG-4-Fehlersuche.xml','targets':[40]},
 {'id':'alg-5','title':'Dein Rover, dein Härtetest','minutes':90,'phases':[15,15,40,20],'project':'projekte/ALG-5-Start.xml','targets':[60,80]},
 {'id':'alg-6','title':'Die Haltestelle ist verpasst!','minutes':60,'phases':[0,10,35,15],'project':'projekte/ALG-6-Fehlersuche.xml','targets':[50]}]

def backdrop(task):
 targets=task['targets'];depot=task['id']=='alg-3';label='DEPOTGRENZE 40' if depot else ('WÄHLE STATION 60 ODER 80' if len(targets)>1 else 'STATION '+str(targets[0]));lines=[]
 for n,x in enumerate(targets):
  px=240+x;y=100 if n==0 else 258;color='#245743' if n==0 else '#2856a3'
  lines.append(f'<line data-target="{x}" x1="{px}" y1="125" x2="{px}" y2="232" stroke="{color}" stroke-width="3"'+(' stroke-dasharray="5 4"' if n else '')+'/>')
  lines.append(f'<path d="M{px},{125 if n==0 else 232}V{y+4 if n==0 else y-23}" stroke="{color}" fill="none"/><rect x="{px-34}" y="{y-22}" width="68" height="28" rx="6" fill="{color}"/><text x="{px}" y="{y-3}" text-anchor="middle" fill="white" font-size="18" font-weight="700">{x}</text>')
 zones='<rect x="30" y="140" width="250" height="78" fill="#e6f0e9"/><rect x="280" y="140" width="170" height="78" fill="#fff0ce"/><text x="95" y="166" fill="#245743">Depot A</text><text x="355" y="166" fill="#593d0c">Depot B</text>' if depot else ''
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360"><title>{label}</title><rect width="480" height="360" fill="#f8faf7"/><g font-family="Arial,sans-serif" font-size="17" fill="#20362f"><text x="28" y="38" font-size="13" letter-spacing="2">ROVER-WERKSTATT</text><text x="28" y="68" font-size="21" font-weight="700">{label}</text>{zones}<path d="M30 180H450" stroke="#a8b7ad" stroke-width="2"/><circle cx="240" cy="180" r="3" fill="#526258"/><text x="238" y="215" text-anchor="end" font-size="14">0</text>{"".join(lines)}<text x="28" y="309" font-size="14">x wächst nach rechts · 1 Schritt = 1 x-Einheit</text><text x="28" y="333" font-size="13" fill="#526258">Vereinfachtes Modell · Richtung 90°</text></g></svg>'

def main():
 out=BASE/'material/buehnen';out.mkdir(exist_ok=True)
 for task in TASKS:
  svg=backdrop(task);(out/(task['id']+'.svg')).write_text(svg,encoding='utf-8')
  files=[task['project']]
  if task['id'] in ['alg-3','alg-4','alg-5','alg-6']:
   files.append('lehrpersonen/'+{'alg-3':'ALG-3-Beispielloesung.xml','alg-4':'ALG-4-Repariert.xml','alg-5':'ALG-5-Beispielloesung.xml','alg-6':'ALG-6-Repariert.xml'}[task['id']])
  for relative in files:
   file=ROOT/relative;root=E.parse(file).getroot();stage=root.find('.//stage');costumes=stage.find('costumes/list');costumes.attrib.pop('struct',None)
   for child in list(costumes):costumes.remove(child)
   next_id=max([int(e.attrib['id']) for e in root.iter() if e.attrib.get('id','').isdigit()]+[10000])+1
   item=E.SubElement(costumes,'item');E.SubElement(item,'costume',{'name':'Lernwerk '+task['id'],'center-x':'240','center-y':'180','image':'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode(),'id':str(next_id)})
   stage.attrib['costume']='1';file.write_text(E.tostring(root,encoding='unicode',short_empty_elements=True),encoding='utf-8',newline='\n')
 (ROOT/'fassung.json').write_text(json.dumps({'version':'2.1','date':'2026-10-27','totalMinutes':405,'annualUE':36,'source':'Eigene Unterrichtskonstruktion, bestätigtes didaktisches Mapping vom 23.09.2026','license':'CC BY-SA 4.0','tasks':[dict(t,revision='2.1' if t['id']=='alg-4' else '2.0') for t in TASKS],'boundaries':'Unterrichtszeit, Motivation und Safari/Touch noch zu erproben; keine neue Datenschutzfreigabe.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Prepared 10 embedded stages; program blocks untouched')
if __name__=='__main__':main()
