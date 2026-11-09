'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {preparePublishedPages}=require('../pages/build.cjs');
const pages=preparePublishedPages(),root='klasse7/medien/';
test('MED-3 nutzt ein einziges KI-Arbeitsbild in Aufgabe, Download und Projektion',()=>{
 const page=pages.get(root+'med-3-ein-bild-zwei-geschichten.html');
 const p3=pages.get(root+'projektion-3.html');
 assert.match(page,/<img\b[^>]*src="material\/hof-arbeitsbild\.png"/);
 assert.match(page,/href="material\/hof-arbeitsbild\.png"[^>]*download="hof-original\.png"/);
 assert.match(p3,/<img\b[^>]*src="material\/hof-arbeitsbild\.png"/);
 for(const html of [page,p3])assert.match(html,/KI-generiert/);
 assert.doesNotMatch(page,/Bearbeitbare SVG-Quelle|eigene schematische Illustration/);
});
test('Arbeitsbild hat genügend Rasterauflösung und der bisherige Bildbestand bleibt verfügbar',()=>{
 const png=pages.get(root+'material/hof-arbeitsbild.png');
 assert.ok(Buffer.isBuffer(png),'Arbeits-PNG fehlt');
 assert.equal(png.subarray(0,8).toString('hex'),'89504e470d0a1a0a');
 assert.ok(png.readUInt32BE(16)>=1500);assert.ok(png.readUInt32BE(20)>=1000);
 assert.ok(pages.has(root+'material/hof-original.svg'));
 assert.ok(pages.has(root+'material/hof-original.png'));
 for(const name of pages.keys())if(name.startsWith(root+'material/'))assert.doesNotMatch(name,/hof-(?:variante|loesung|ausschnitt)-/);
});
test('Herkunft und tatsächliche Gestaltungsarbeit bleiben im vollständigen MED-3-Weg erhalten',()=>{
 const page=pages.get(root+'med-3-ein-bild-zwei-geschichten.html');
 const rights=pages.get(root+'medienbogen-quellen-und-nutzungsrechte.html');
 assert.match(rights,/hof-arbeitsbild\.png/);assert.match(rights,/KI-generiert/);
 assert.match(page,/Notiere beide <strong>vor<\/strong> dem Bearbeiten/);
 assert.match(page,/zunächst ohne deine Absichten/);
 assert.match(page,/Führe die geplante Änderung selbst aus/);
 assert.match(page,/Vereinsfoto/);
 const f=JSON.parse(pages.get(root+'fassung.json'));
 assert.deepEqual(f.aufgaben,[45,45,90,45,45]);assert.equal(f.minuten,270);
});