'use strict';
const fs=require('node:fs'),path=require('node:path');
function render(paper=false){if(paper)return '';return [
'<details class="b17-help" id="b17-hilfe"><summary>Bildschirmhilfe: B17 Schritt für Schritt (statt Zettel)</summary>',
'<div class="b17-model" data-b17-model><p class="b17-intro">Erfundenes Modell, keine echten Browserdaten.</p>',
'<p class="b17-status" data-b17-status role="status" aria-live="polite" aria-atomic="true"></p>',
'<div class="b17-actions"><a href="#answer-modell-versuch" data-b17-to-answer>Zur Versuchsspur</a><button type="button" data-b17-start>Start prüfen</button></div>',
'<div class="b17-stations"><section class="b17-browser"><h3>Im Browser</h3><div class="b17-id">Kennung <strong>B17</strong></div><p class="b17-current">Aktuelle Seite<br><strong>Lesen</strong> · bleibt gleich</p><p>Die Kennung ist keine Besuchsliste.</p></section>',
'<section class="b17-provider"><h3>Beim Anbieter</h3><p>Liste zu <strong>B17</strong></p><fieldset><legend data-b17-list-label>Frühere Besuche · Start</legend>',
...['Lesen','Zeichnen','Zeichnen'].map((t,i)=>'<label class="b17-visit"><input type="radio" name="b17-visit" value="'+i+'" disabled><span>Besuch '+(i+1)+': <strong data-b17-topic="'+i+'">'+t+'</strong></span></label>'),
'</fieldset><p class="b17-small">Ein gewählter Besuch wechselt sein Thema. Die aktuelle Seite zählt hier nicht mit.</p><button type="button" data-b17-check hidden>Änderung prüfen</button></section>',
'<section class="b17-rules"><h3>Die Regeln kurz</h3><p><strong>K · Kontext</strong><br>Nur die aktuelle Seite.</p><p><strong>V · Verlauf</strong><br>Nur frühere Besuche: Mehrheit entscheidet, bei Gleichstand gilt K.</p><p class="b17-small">Lesen → Buchwerbung<br>Zeichnen → Stiftewerbung</p><a href="#arbeitsstelle-unser-modell-kennt-nur-zwei-themen">Vollständige Regeln</a></section></div>',
'<section class="b17-results" data-b17-results hidden><h3 id="b17-ergebnis" tabindex="-1" data-b17-result-title>Dein Vergleich</h3>',
'<table class="b17-comparison"><thead><tr><th scope="col">Regel / Daten</th><th scope="col">Start</th><th scope="col" data-b17-after hidden>Nach deinem Eingriff</th></tr></thead><tbody>',
...['context','history','counts'].map((key,i)=>'<tr><th scope="row">'+['K · Kontext','V · Verlauf','Für V gezählt'][i]+'</th><td data-b17-cell="'+key+'-start"></td><td data-b17-cell="'+key+'-after" data-b17-after hidden></td></tr>'),
'</tbody></table><p data-b17-explain hidden><a class="b17-explain" href="#answer-modell-versuch" data-b17-to-answer>Meine Erklärung festhalten →</a></p></section>',
'<p class="b17-small b17-boundary">Die Knöpfe prüfen die Regeln, nicht deine Erklärung. Mündlich oder im Heft geht auch.</p>',
'<div class="b17-restart"><button type="button" data-b17-reset hidden>Zum Start</button><span class="b17-small">Nur das Modell startet beim Seitenwechsel neu. Deine Notizen bleiben beim Zurücksetzen stehen.</span></div>',
'<noscript><p>Die Bildschirmhilfe benötigt JavaScript. Nutze ohne JavaScript Zettel oder Liste.</p></noscript></div></details>'
].join('');}
function returnLink(paper=false){return paper?'':'<p class="b17-return"><a href="#b17-hilfe" data-b17-return>Zurück zur Bildschirmhilfe →</a></p>';}
function assets(pack){if(!pack.steps.some(s=>s.blocks.some(b=>b.selectionModel)))return new Map();return new Map(['b17-model.js','b17-model.css'].map(f=>[f,fs.readFileSync(path.join(__dirname,f),'utf8')]));}
module.exports={render,returnLink,assets};
