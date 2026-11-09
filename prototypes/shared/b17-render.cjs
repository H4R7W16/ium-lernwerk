'use strict';
const fs=require('node:fs'),path=require('node:path');
function render(paper=false){if(paper)return '';return [
'<details class="b17-help"><summary>Bildschirmhilfe: B17 Schritt für Schritt (statt Zettel)</summary>',
'<div class="b17-model" data-b17-model><p class="b17-intro">Erfundenes Modell, keine echten Browserdaten. Nutze dieselbe Versuchsspur unter der Hilfe. Beim erneuten Öffnen der Seite beginnt nur das Modell von vorn.</p>',
'<div class="b17-stations"><section class="b17-browser"><h3>Im Browser</h3><div class="b17-id">Kennung <strong>B17</strong></div><p class="b17-current">Aktuelle Seite<br><strong>Lesen</strong> · bleibt gleich</p><p>Die Kennung ordnet die Liste zu. Sie ist selbst keine Besuchsliste.</p></section>',
'<section class="b17-provider"><h3>Beim Anbieter</h3><p>Liste zu <strong>B17</strong></p><fieldset><legend data-b17-list-label>Frühere Besuche · Start</legend>',
...['Lesen','Zeichnen','Zeichnen'].map((t,i)=>'<label class="b17-visit"><input type="radio" name="b17-visit" value="'+i+'" disabled><span>Besuch '+(i+1)+': <strong data-b17-topic="'+i+'">'+t+'</strong></span></label>'),
'</fieldset><p class="b17-small">Auswahl ersetzt genau einen Besuch durch das andere Thema. Die aktuelle Seite wird hier nicht hinzugezählt.</p></section>',
'<section class="b17-rules"><h3>Zwei Auswahlregeln</h3><p><strong>K · Kontext</strong><br>Nur aktuelle Seite: Lesen → Buchwerbung; Zeichnen → Stiftewerbung.</p><p><strong>V · Verlauf</strong><br>Mehr frühere Besuche Lesen → Buchwerbung; mehr Zeichnen → Stiftewerbung. Bei Gleichstand gilt K.</p></section></div>',
'<p class="b17-status" data-b17-status role="status" aria-live="polite" aria-atomic="true"></p>',
'<div class="b17-controls"><button type="button" data-b17-start>Start prüfen</button><button type="button" data-b17-check hidden>Änderung prüfen</button><button type="button" data-b17-reset hidden>Zum Start</button></div>',
'<div class="b17-before" data-b17-before hidden><strong>Zum Vergleich: Start</strong><p>K: Buchwerbung. V: Stiftewerbung (1 Lesen, 2 Zeichnen).</p></div>',
'<div class="b17-results" data-b17-results hidden><h3>Geprüfte Auswahl</h3><p data-b17-counts></p></div>',
'<p data-b17-rule-note hidden>Notiere deine Erklärung in der Versuchsspur. Die Schaltflächen prüfen die Regeln, nicht deine Vorhersage oder Erklärung. „Zum Start“ lässt deine Notizen stehen.</p>',
'<noscript><p>Die Bildschirmhilfe benötigt JavaScript. Nutze ohne JavaScript die Zettel oder Liste aus dem Auftrag.</p></noscript></div></details>'
].join('');}
function assets(pack){if(!pack.steps.some(s=>s.blocks.some(b=>b.selectionModel)))return new Map();return new Map(['b17-model.js','b17-model.css'].map(f=>[f,fs.readFileSync(path.join(__dirname,f),'utf8')]));}
module.exports={render,assets};
