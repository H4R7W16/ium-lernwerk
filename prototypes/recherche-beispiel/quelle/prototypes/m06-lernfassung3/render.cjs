'use strict';
const fs=require('node:fs'),path=require('node:path');
const base=require('../m06-selbstlernen/render.cjs');
const {pages}=require('./content.cjs');
function adapt(html,reading=false){
 html=html.replace('<body>','<body data-storage-key="ium-schleifen-planung-v3">')
  .replace('<span class="version-current" aria-current="true">Selbstlernstrecke</span>','<a href="../m06-selbstlernen/index.html">Selbstlernstrecke</a>')
  .replace('<a href="../m06-lernfassung3/index.html">Lernfassung 3</a>','<span class="version-current" aria-current="true">Lernfassung 3</span>')
  .replace('href="app.css"','href="../m06-selbstlernen/app.css"><link rel="stylesheet" href="journey.css"')
  .replace('· Referenzstrecke<br>','· Lernfassung 3<br>')
  .replace('Sicherung dieser Referenzstrecke','Sicherung der Lernfassung 3')
  .replace('Die neuen freien Antwortfelder bleiben nur im offenen Tab;','Die Eingaben der Planungsetappen und die freien Antwortfelder bleiben nur im offenen Tab;');
 for(const file of ['cleaning-core.js','model.js','app.js'])html=html.replace('src="'+file+'"','src="../m06-selbstlernen/'+file+'"');
 if(!reading)html=html.replace('<script src="../m06-selbstlernen/app.js"','<script src="journey-model.js" defer></script><script src="journey.js" defer></script><script src="../m06-selbstlernen/app.js"');
 return html;
}
function render(){return adapt(base.render(pages));}
function renderReading(){return adapt(base.renderReading(pages),true).replace(/<select[\s\S]*?<\/select>/g,'<p class="caption">Auf Papier auswählen.</p>').replace('Die Eingaben in den beiden Teilaufgaben bleiben im offenen Tab. Halte sie für eine spätere Sitzung zusätzlich auf Papier fest; deinen eigenen 4×3-Code kannst du über „Stand mitnehmen“ sichern.','Halte deine Teilentscheidungen, deinen eigenen 4×3-Code und deine Begründungen auf Papier fest. Die Lösungen und Ablauftabellen stehen jeweils bei der Aufgabe.').replace('Ganze Schleifenzahlen von 2 bis 9. Deine Begründung vergleichst du selbst; der Roboter prüft den Weg.','Ganze Schleifenzahlen von 2 bis 9. Vergleiche deinen Weg und deine Begründung mit der Lösung und der Ablauftabelle.');}
if(require.main===module){fs.writeFileSync(path.join(__dirname,'index.html'),render());fs.writeFileSync(path.join(__dirname,'read.html'),renderReading());}
module.exports={render,renderReading};
