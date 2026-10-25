"""Render the authored Klasse-7 Markdown into the existing static page shells.
No external packages. Supports only the deliberately small local authoring format.
"""
from pathlib import Path
import re, html, json, sys
BASE=Path(__file__).resolve().parent
ROOT=BASE/'inhalt/klasse7/programmieren'
FILES={**{f'alg-{i}':f'lernende/alg-{i}.html' for i in range(1,7)},**{x:f'lehrpersonen/{x}.html' for x in ['durchfuehrung-134','durchfuehrung-256','sicherung','hoerbriefing','umgebung','jahrgang']}}

def inline(text):
 tokens=[]
 def protect(m):
  raw=m.group(0)
  if raw.startswith('`'):result='<code>'+html.escape(raw[1:-1])+'</code>'
  elif raw.startswith('[['):result=html.escape(raw[2:-2].split('|')[-1])
  else:
   label,url=re.match(r'\[([^\]]+)\]\(([^)]+)\)',raw).groups()
   result='<a href="'+html.escape(url,quote=True)+'">'+html.escape(label)+'</a>'
  tokens.append(result);return '\x00'+str(len(tokens)-1)+'\x00'
 text=re.sub(r'`[^`]+`|\[\[[^\]]+\]\]|\[[^\]]+\]\([^)]+\)',protect,text)
 text=html.escape(text);text=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',text)
 for i,value in enumerate(tokens):text=text.replace('\x00'+str(i)+'\x00',value)
 return text

def render(md):
 lines=md.strip().splitlines();out=[];anchors=[];i=0;section=False
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line.startswith('```'):
   code=[];i+=1
   while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
   out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>');i+=1;continue
  if line.startswith('#'):
   match=re.match(r'^(#{1,3})\s+(.+)',line);level=len(match[1]);title=match[2]
   if level==2:
    if section:out.append('</section>')
    anchor='abschnitt-'+str(len(anchors)+1);anchors.append((anchor,title));out.append('<section class="lesson-section" id="'+anchor+'">');section=True
   out.append(f'<h{level}>'+inline(title)+f'</h{level}>');i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r':?-+:?',c) for c in cells):rows.append(cells)
    i+=1
   out.append('<div class="table-scroll" tabindex="0" role="region" aria-label="Tabelle, bei Bedarf seitlich verschieben"><table><thead><tr>'+''.join('<th>'+inline(c)+'</th>' for c in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>');continue
  if line.startswith('- '):
   items=[]
   while i<len(lines) and lines[i].strip().startswith('- '):items.append('<li>'+inline(lines[i].strip()[2:])+'</li>');i+=1
   out.append('<ul>'+''.join(items)+'</ul>');continue
  if line.startswith('<'):
   out.append(line);i+=1;continue
  para=[line];i+=1
  while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||-|<|```)',lines[i].strip()):para.append(lines[i].strip());i+=1
  out.append('<p>'+inline(' '.join(para))+'</p>')
 if section:out.append('</section>')
 return '\n'.join(out),anchors

def page(name,relative):
 md=(BASE/'material'/f'{name}.md').read_text(encoding='utf-8-sig')
 body,anchors=render(md);old=(ROOT/relative).read_text(encoding='utf-8')
 if name.startswith('alg-'):
  actions=re.search(r'<p class="project-actions">[\s\S]*?</p>',old)[0]
  hint='<p class="project-instruction">Der Link lädt dein Startprojekt bereits. Halte deine Vorhersage fest, bevor du startest. Eigene Arbeit sicherst du über Datei speichern und prüfst sie mit Datei öffnen.</p>'
  end=body.index('</p>')+4;body=body[:end]+'\n'+actions+hint+body[end:]
 nav='<nav class="phase-links" aria-label="Abschnitte dieser Aufgabe"><strong>Auf dieser Seite</strong><ol>'+''.join('<li><a href="#'+a+'">'+html.escape(t)+'</a></li>' for a,t in anchors)+'</ol></nav>'
 body=body.replace('<section class="lesson-section"',nav+'<section class="lesson-section"',1)
 old=re.sub(r'(<article\b[^>]*>)[\s\S]*?</article>',lambda m:m[1]+body+'</article>',old,count=1)
 title=re.match(r'#\s+(.+)',md.strip())[1];old=re.sub(r'<title>[^<]+</title>','<title>'+html.escape(title)+' · IuM 7</title>',old,count=1)
 old=re.sub(r'stil.css\?v=20261025(?:-2)?','stil.css?v=20261025-2',old)
 old=re.sub(r'<p class="editor-adaptation">[\s\S]*?</p>','',old)
 return old

def main():
 check='--check' in sys.argv;bad=[]
 for name,relative in FILES.items():
  actual=page(name,relative);file=ROOT/relative
  if actual!=file.read_text(encoding='utf-8'):
   if check:bad.append(relative)
   else:file.write_text(actual,encoding='utf-8',newline='\n')
 if bad:raise SystemExit('Materialausgabe veraltet: '+', '.join(bad))
 print(('Checked' if check else 'Rendered')+' 12 material pages')
if __name__=='__main__':main()
