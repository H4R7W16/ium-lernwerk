'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const dir=path.join(__dirname,'inhalt');
const read=f=>fs.readFileSync(path.join(dir,f),'utf8');
test('GAM-2 bietet den stillen Film als steuerbare Alternative innerhalb der bestehenden Übung',()=>{
 const html=read('gam-2-kostenlos-oder-bezahlt.html');
 const start=html.indexOf('id="wolkenteam-shopfolge"');
 assert.ok(start>html.indexOf('2-ein-beispiel-und-eine-rechnung'),'Film in der vorhandenen Übungsphase');
 assert.ok(start<html.indexOf('3-vergleichen-und-entscheiden'),'Film vor eigener Vergleichsphase');
 assert.ok(html.indexOf('Übertrage den Gedankengang auf B.')<start,'A-Beispiel zuerst auf B anwenden, bevor die C-Medienfolge beginnt');
 const media=html.slice(start,html.indexOf('</section>',start));
 assert.match(media,/<video\b[^>]*controls[^>]*preload="none"/);
 assert.match(media,/material\/wolkenteam-shopfolge\.mp4/);
 assert.doesNotMatch(media,/\b(?:autoplay|loop)\b|<script\b|<iframe\b|<form\b/i);
 assert.ok(html.indexOf('id="gam-2-rechenauftrag"')<html.indexOf('class="shop-media"'),'Konkrete Frage vor der Medienhilfe');
 assert.match(html,/Mit Karte C kannst du direkt rechnen/);
 assert.match(html,/Bei Bedarf helfen dir die Shopfolge oder die Einzelansichten/);
 assert.match(html,/Wie viele Sterne bleiben übrig/);
 assert.match(media,/Ende vor dem Kauf/);
});
test('Shopzustände behalten Paketbindung und lassen Zahlung, Rest und Kaufurteil offen',()=>{
 const episode=JSON.parse(fs.readFileSync(path.join(__dirname,'../../media-source/gam2-wolkenteam/episode.json'),'utf8'));
 assert.equal(episode.duration,24);assert.equal(episode.fps,30);
 assert.deepEqual(episode.prices,{outfitStars:450,packageStars:500,packageEuro:5});
 assert.equal(Math.ceil(episode.prices.outfitStars/episode.prices.packageStars)*episode.prices.packageEuro,5);
 assert.equal(episode.prices.packageStars-episode.prices.outfitStars,50);
 for(const [i,file]of ['wolkenteam-start.svg','wolkenteam-outfit.svg','wolkenteam-sterne.svg'].entries()){
  const svg=read('material/'+file);assert.match(svg,/viewBox="0 0 1920 1080"/);
  assert.doesNotMatch(svg,/4[,.]50|\b50 Sterne|Rest|Mindestzahlung|richtige Wahl|kaufen lohnt/i,file);
  if(i===1){assert.match(svg,/450 Sterne/);assert.match(svg,/Nur heute!/);assert.match(svg,/Nur das Aussehen/);}
  if(i===2){assert.match(svg,/500 Sterne/);assert.match(svg,/5 €/);assert.match(svg,/Nur dieses Paket/);assert.match(svg,/450 Sterne/);}
 }
});
test('Ruhende Shopansichten und vollständiger Textzugang bewahren den Angebotsvergleich und den Rechenrückweg',()=>{
 const html=read('gam-2-kostenlos-oder-bezahlt.html');
 assert.match(html,/id="wolkenteam-einzelansichten"/);
 for(const file of ['wolkenteam-start.svg','wolkenteam-outfit.svg','wolkenteam-sterne.svg'])assert.match(html,new RegExp('material/'+file.replace('.','\\.')));
 assert.match(html,/Zum Rechenauftrag/);assert.match(html,/id="gam-2-rechenauftrag"/);
 assert.match(html,/12 € einmalig/);assert.match(html,/Werbeunternehmen zahlen dem Anbieter/);
 assert.match(html,/Alle Aufgaben ohne Käufe lösbar/);
 assert.match(html,/Du darfst A, B, C oder keines empfehlen/);
 assert.match(html,/Die private Notiz bleibt geschlossen/);
 const projection=read('projektion-2.html');assert.match(projection,/gam-2-kostenlos-oder-bezahlt\.html#wolkenteam-shopfolge/);
});

test('C-Rechenfall legt fehlendes Sternenguthaben fest, ohne Zahlung oder Rest vorzugeben',()=>{
 const html=read('gam-2-kostenlos-oder-bezahlt.html');
 const question=html.match(/<p id="gam-2-rechenauftrag">([\s\S]*?)<\/p>/)?.[1];
 assert.ok(question,'Rechenauftrag bleibt gezielt erreichbar');
 assert.match(question,/Die Person hat noch keine Sterne und kauft die benötigten Sterne im Shop/);
 assert.match(question,/Wie viel muss sie für das Outfit mindestens bezahlen/);
 assert.doesNotMatch(question,/5 €|\b50 Sterne|ein Paket/);
 assert.ok(html.indexOf('id="wolkenteam-shopfolge"')<html.indexOf('id="gam-2-rechenauftrag"'),'Bisheriger Medienanker führt zuerst zur Frage');
});
