'use strict';
const base=require('../m06-selbstlernen/content.cjs');
const names=['Beispiel verstehen','4×2-Plan ergänzen','Linken Wechsel planen','Eigenen 4×3-Plan entwickeln'];
function replaceRequired(html,from,to){if(!html.includes(from))throw new Error('Planungsinhalt fehlt: '+from);return html.replace(from,to);}
function field(html,id,control){return replaceRequired(html,html.match(new RegExp('<textarea id="'+id+'"[^>]*></textarea>'))?.[0]||'MISSING '+id,control);}
function select(id,words=['links','rechts']){return '<select id="'+id+'" data-material-answer><option value="">Bitte wählen</option>'+words.map(word=>'<option value="'+word+'">'+word+'</option>').join('')+'</select>';}
function exercisePanel(id,label){return '<div class="enhanced"><button type="button" class="primary" id="'+id+'-run">'+label+'</button><div class="feedback" id="'+id+'-feedback" role="status"></div><div id="'+id+'-run-holder" hidden><p class="caption">Diese Fahrt gehört zu deinen aktuellen Eingaben. Nutze Zurück, um die entscheidende Stelle zu untersuchen.</p><div class="simulation" id="'+id+'-simulation"></div></div></div>';}
function planning(html){
 const a6=html.indexOf('<section class="task" id="a6">'),a7=html.indexOf('<section class="task" id="a7">'),own=html.indexOf('<h2 id="free-plan">');
 if(a6<0||a7<a6||own<a7)throw new Error('Die vier Planungsabschnitte konnten nicht zugeordnet werden.');
 const chunks=[html.slice(0,a6),html.slice(a6,a7),html.slice(a7,own),html.slice(own)];
 for(const id of ['a6-first','a6-last'])chunks[1]=field(chunks[1],id,'<input id="'+id+'" data-material-answer type="number" min="2" max="9" step="1" inputmode="numeric" aria-describedby="bridge-input-note">');
 chunks[1]=field(chunks[1],'a6-turn',select('a6-turn'));
 chunks[1]=replaceRequired(chunks[1],'<p><strong>Selbstkontrolle:', '<p class="caption" id="bridge-input-note">Ganze Schleifenzahlen von 2 bis 9. Deine Begründung vergleichst du selbst; der Roboter prüft den Weg.</p>'+exercisePanel('bridge','Meinen 4×2-Plan ausführen')+'<p><strong>Selbstkontrolle:');
 chunks[2]=replaceRequired(chunks[2],'Erste Drehung und Blick danach','Erste Anweisung');
 chunks[2]=field(chunks[2],'a7-first',select('a7-first',['vor','links','rechts']));
 chunks[2]=replaceRequired(chunks[2],'Fahrt und zweite Drehung · jeweils Standort und Blick','Zweite Anweisung');
 chunks[2]=field(chunks[2],'a7-next',select('a7-next',['vor','links','rechts'])+'<label for="a7-last">Dritte Anweisung</label>'+select('a7-last',['vor','links','rechts'])+'<label for="a7-reason">Standort und Blick nach jeder Anweisung · Warum passt die erste Drehung?</label><textarea id="a7-reason" data-material-answer rows="3" maxlength="4000"></textarea>');
 chunks[2]=replaceRequired(chunks[2],'<p><strong>Selbstkontrolle:',exercisePanel('switch','Meinen Reihenwechsel ausführen')+'<p><strong>Selbstkontrolle:');
 const bridges=[
  'Du hast gesehen, wie ein Plan aus Reihenfahrten und einem Wechsel entsteht. Jetzt veränderst du die Breite: Welche Zahlen und welche Drehung passen bei vier Spalten?',
  'Für den größeren Raum brauchst du noch einen Wechsel am linken Rand. Dort beginnt der Roboter mit einem anderen Blick.',
  'Jetzt hast du beide Randwechsel untersucht. Plane als Nächstes die ganze Fläche selbst. Die Etappen bleiben als Hilfe erreichbar.',
  'Vergleiche zum Schluss deine Begründungen mit der Selbstkontrolle. Im Lerncheck wendest du Schleifen auf neue Aufgaben an.'
 ];
 return '<div class="journey-intro"><p class="eyebrow">Lernfassung 3 · Dein Planungsweg</p><p>Erst nachvollziehen, dann ergänzen, einen Übergang selbst lösen und schließlich alles verbinden. Du kannst jede Etappe direkt wählen. Hilfen, Lösungen und die vollständige Lesefassung bleiben zugänglich.</p><p class="caption">Die Eingaben in den beiden Teilaufgaben bleiben im offenen Tab. Halte sie für eine spätere Sitzung zusätzlich auf Papier fest; deinen eigenen 4×3-Code kannst du über „Stand mitnehmen“ sichern.</p></div><nav class="journey-nav enhanced" aria-label="Etappen der Planung">'+names.map((name,i)=>'<button type="button" data-stage="'+i+'"><span class="stage-number">'+(i+1)+'</span><span>'+name+'</span></button>').join('')+'</nav><p class="enhanced caption" id="journey-position" role="status"></p>'+chunks.map((chunk,i)=>'<section class="journey-stage" data-stage-panel="'+i+'" aria-labelledby="stage-title-'+i+'"><h2 id="stage-title-'+i+'" tabindex="-1" class="stage-title">Etappe '+(i+1)+' · '+names[i]+'</h2>'+chunk+'<div class="stage-bridge"><p>'+bridges[i]+'</p><div class="stage-actions enhanced">'+(i?'<button type="button" data-stage="'+(i-1)+'">← Zur vorherigen Etappe</button>':'')+(i<3?'<button type="button" class="primary" data-stage="'+(i+1)+'">Weiter: '+names[i+1]+' →</button>':'<a class="next-link" href="#check">Weiter zum Lerncheck →</a>')+'</div></div></section>').join('');
}
const pages=base.pages.map(page=>page.id==='plan'?{...page,intro:'Vier verbundene Etappen: Du probierst Teilentscheidungen aus und entwickelst daraus deinen eigenen Plan.',html:planning(page.html)}:page.id==='start'?{...page,html:'<aside class="journey-intro"><p class="eyebrow">Lernfassung 3</p><p>Diese Fassung verbindet die ausführlichen Erklärungen mit einem interaktiven Planungsweg. Du kannst das ganze Kapitel bearbeiten oder direkt <a href="#plan">in die vier Planungsetappen einsteigen</a>.</p></aside>'+page.html}:page);
module.exports={pages,names};
