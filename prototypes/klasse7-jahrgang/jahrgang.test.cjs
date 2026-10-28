'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {prepareNavigablePages,preparePublishedPages,preparePages}=require('../pages/build.cjs');
const original=require('../klasse7-programmieren/layout.cjs').applySeriesLayout(preparePages());
const final=preparePublishedPages();
const main=s=>s.match(/<main\b[^>]*>[\s\S]*?<\/main>/)?.[0];
test('22 Aufgaben und fachliche Materialien behalten ihre Hauptinhalte',()=>{
 let count=0;
 for(const [name,html]of original){if(!name.startsWith('klasse7/')||!name.endsWith('.html')||name==='klasse7/index.html'||name.endsWith('/lehrpersonen/jahrgang.html')||name==='klasse7/programmieren/index.html')continue;
  assert.equal(main(final.get(name)),main(html),name);count++;
 }assert.ok(count>=22);
 for(let i=1;i<=6;i++)assert.ok(final.has('klasse7/programmieren/lernende/alg-'+i+'.html'));
 for(const [prefix,total]of [['med',5],['dat',5],['gam',6]])assert.equal([...final.keys()].filter(n=>new RegExp('/'+prefix+'-[1-6]-(?!briefing)[^/]+\\.html$').test(n)&&!n.includes('bedienkarte')).length,total);
});
test('Alle regulären Klasse-7-Seiten haben dieselbe geordnete Hauptnavigation',()=>{
 let count=0;
 for(const [name,html]of final){if(!name.startsWith('klasse7/')||!name.endsWith('.html')||name.includes('/snap/'))continue;
  const nav=html.match(/<nav class="year-nav"[^>]*>([\s\S]*?)<\/nav>/)?.[1];assert.ok(nav,name);
  const labels=[...nav.matchAll(/<a[^>]*>([^<]+)<\/a>/g)].map(m=>m[1]);assert.deepEqual(labels,['Jahrgang','Medien','Daten','Programmieren','Gaming'],name);
  assert.equal([...nav.matchAll(/aria-current=/g)].length,1,name);count++;
 }assert.ok(count>=22);
});
test('Jahresmaterialien und vier unveränderte Diagnosedateien sind erreichbar',()=>{
 for(const name of ['index','lehrpersonen','lernziele','briefing','uebergaenge','wiederaufnahme-medien','wiederaufnahme-daten','wiederaufnahme-programmieren','wiederaufnahme-gemischt','wiederaufnahme-lehrpersonen'])assert.ok(final.has('klasse7/'+name+'.html'));
 for(const file of ['eingangsdiagnose-lernende.pdf','eingangsdiagnose-lehrpersonen.pdf','Startdatei.txt','Beobachtungsraster.txt'])assert.ok(final.has('klasse7/material/'+file));
 assert.equal((final.get('klasse7/lernziele.html').match(/<td>3\.2\./g)||[]).length,29);
 assert.equal(270+270+405+270+90+90+135+45+45,36*45);
});
test('Snap-Laufzeit bleibt vom Jahresmantel unberührt und Verweise sind unterpfadfähig',()=>{
 const before=prepareNavigablePages();
 for(const [name,value]of original)if(name.startsWith('klasse7/programmieren/snap/'))assert.deepEqual(before.get(name),value,name);
 for(const [name,html]of final){if(!name.endsWith('.html'))continue;for(const [,ref]of html.matchAll(/(?:href|src)="([^"]+)"/g)){
  if(/^(https?:|mailto:|tel:|data:|#)/.test(ref))continue;
  const url=new URL(ref,'https://example.test/ium-lernwerk/'+name);assert.ok(url.pathname.startsWith('/ium-lernwerk/'),name);
  const target=decodeURIComponent(url.pathname.slice(14));assert.ok(final.has(target.endsWith('/')?target+'index.html':target),name+' -> '+ref);
 }}
});
