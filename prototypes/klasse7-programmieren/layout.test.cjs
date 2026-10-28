'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),path=require('node:path'),crypto=require('node:crypto');
const build=require('../pages/build.cjs'),{addGradeNavigation}=require('../shared/grade-navigation.cjs');
const raw=build.preparePages(),before=addGradeNavigation(raw),published=addGradeNavigation(require('./layout.cjs').applySeriesLayout(raw)),root='klasse7/programmieren/';
const sha=value=>crypto.createHash('sha256').update(value).digest('hex');
const pages=[...raw].filter(([name,html])=>name.startsWith(root)&&name.endsWith('.html')&&/<header class="(?:site-header|editor-header)"/.test(html));
const main=html=>html.match(/<main\b[^>]*>[\s\S]*?<\/main>/)?.[0];

test('Klasse 7 nutzt die gemeinsame Wortmarke und die tatsächlichen Mantelquellen der Reihe',()=>{
 assert.ok(pages.length>20);
 assert.equal(published.get(root+'mantel.css'),raw.get('klasse5/mantel.css'));
 assert.equal(published.get(root+'identity.css'),raw.get('klasse5/identity.css'));
 for(const [name]of pages){const html=published.get(name);assert.match(html,/class="lw-brand-logo"/,name);assert.match(html,/IuM Lernwerk 7 – Informatik und Medienbildung/,name);assert.doesNotMatch(html,/class="brand-mark"/,name);assert.match(html,/reihenlayout\.css\?v=20261027/,name);}
});

test('Isolierter Reihenlayout-Adapter erhält alle Lerntexte, Lehrtexte, Aufgabenlinks und den ausführbaren Editorinhalt',()=>{
 for(const [name,html]of pages){assert.equal(main(published.get(name)),main(html),name);}
 for(const [name,data]of raw)if(name.startsWith(root)&&!pages.some(([page])=>page===name)&&!name.endsWith('snap/lernwerk-herkunft.json'))assert.deepEqual(published.get(name),data,name);
});

test('Reihenlayout-Adapter erhält Klasse 5 und 6 bytegleich',()=>{
 for(const [name,data]of before)if(!name.startsWith('klasse7/'))assert.deepEqual(published.get(name),data,name);
 for(const name of published.keys())if(!before.has(name))assert.ok(name.startsWith(root),name);
});

test('alle neuen Wortmarken und responsiven Bildquellen bleiben im Pages-Unterpfad erreichbar',()=>{
 for(const [name]of pages){const html=published.get(name);for(const [,ref]of html.matchAll(/(?:src|srcset)="([^"]*brand\/[^"]+)"/g)){const url=new URL(ref,'https://example.test/ium-lernwerk/'+name);assert.ok(url.pathname.startsWith('/ium-lernwerk/'));assert.ok(published.has(url.pathname.slice('/ium-lernwerk/'.length)),name+' → '+ref);}}
 for(const file of ['brand/ium-lernwerk-7.png','brand/ium-lernwerk-7-compact.png']){const png=published.get(root+file);assert.ok(Buffer.isBuffer(png),file);assert.equal(png.subarray(1,4).toString(),'PNG');}
});

test('der veröffentlichte Editor bindet Layout und Navigation ohne Änderung der Snap-Laufzeit',()=>{
 const source=JSON.parse(raw.get(root+'snap/lernwerk-herkunft.json')),current=JSON.parse(published.get(root+'snap/lernwerk-herkunft.json'));
 assert.ok(current.layout,'ergänzende Layoutbindung');assert.equal(current.layout.sourceShellSha256,source.files['lernwerk.html']);
 for(const [file,h]of Object.entries(current.layout.assets))assert.equal(sha(published.get(path.posix.normalize(root+'snap/'+file))),h,file);
 for(const [file,h]of Object.entries(current.files))assert.equal(sha(published.get(root+'snap/'+file)),h,file);
 for(const file of Object.keys(source.files))if(file!=='lernwerk.html')assert.equal(current.files[file],source.files[file],file);
});

test('Lehrpersonen erhalten eine einklappbare Materialwahl mit allen bisherigen Links',()=>{
 for(const [name,html]of pages.filter(([name])=>name.includes('/lehrpersonen/'))){
  const old=html.match(/<nav class="course-nav teacher-nav"[^>]*>[\s\S]*?<\/nav>/)[0];
  const output=published.get(name),menu=output.match(/<details class="teacher-menu">([\s\S]*?)<\/details>/);
  assert.ok(menu,name);assert.match(menu[1],/<summary>Lehrmaterial auswählen<\/summary>/,name);assert.ok(menu[1].includes(old),name);
 }
});
