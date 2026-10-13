'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const prefix='beispiele/recherche/';
const {prepareClass5Pages}=require('../m06-reinigungsfall/build-class5-pages.cjs');
const frozen=require('./quelle/prototypes/m06-reinigungsfall/build-class5-pages.cjs');
const hash=data=>crypto.createHash('sha256').update(data).digest('hex');
function entry(){return '<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=klasse5/recherche/"><title>Recherche · zusätzliches Beispiel · IuM Lernwerk 5</title></head><body><h1>Recherche: zusätzliches Beispiel</h1><p><a href="klasse5/recherche/">Recherche-Lernweg mit Leas Film öffnen</a></p><p><a href="../../klasse5/">Bisherige Version öffnen</a></p></body></html>';}
function overview(){return '<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Zusätzliche Beispiele · IuM Lernwerk 5</title><style>body{max-width:850px;margin:auto;padding:2rem;font:1.1rem/1.6 system-ui;color:#202838;background:#F5F6FA}h1{line-height:1.15}a{color:#2442C2}.card{background:white;padding:2rem;border-radius:1rem}</style></head><body><p><a href="../klasse5/">← Bisherige Version des Lernwerks</a></p><h1>Zusätzliche Beispiele</h1><section class="card"><h2>Recherche: Eine Frage zum Mond untersuchen</h2><p>Der neue Lernweg für Klasse 5 enthält Leas Recherchefilm mit zwei Denkstellen, Bildfolge, Lesetext und Arbeitsmaterial.</p><p><a href="recherche/">Zum Recherche-Beispiel →</a></p><p><a href="recherche/klasse5/recherche/schritt-suchplan.html#darstellung">Direkt zu Leas Film</a> · <a href="recherche/klasse5/recherche/lehrkraft.html">Hinweise für Lehrpersonen</a></p><p>Kapitel 1.7.0 · Film 1.0 · 13.10.2026. Zur Sichtung und begleiteten Nutzung. Filmnacharbeiten und Hörsichtung bleiben offen.</p></section></body></html>';}
function banner(name){const up='../'.repeat(name.split('/').length-1);return '<aside class="no-print" aria-label="Zusätzliches Beispiel" style="padding:.7rem 1rem;background:#DCE4FF;color:#202838;font:1rem/1.5 system-ui"><strong>Zusätzliches Recherche-Beispiel</strong> · <a href="'+up+'../../klasse5/">Bisherige Version</a> · <a href="'+up+'../">Weitere Beispiele</a></aside>';}
function prepareAdditionalPages(){
 const old=prepareClass5Pages(),result=new Map(old),bundle=new Map();
 for(const [name,original]of frozen.prepareClass5Pages()){
  if(!name.startsWith('klasse5/'))continue;
  let data=original;
  if(name.endsWith('.html'))data=data.replace(/<body([^>]*)>/,(_,attrs)=>'<body'+attrs+'>'+banner(name));
  if(name==='klasse5/mantel-runtime.js'){
   const key="KEY='ium-klasse'+(/\\/klasse6\\/$/.test(base.pathname)?6:5)+'-mantel-v1'";
   if(!data.includes(key))throw Error('Speicherkennung nicht gefunden');
   data=data.replace(key,"KEY='ium-recherche-beispiel-20261013-mantel-v1'");
  }
  if(name==='klasse5/mantel-sw.js'){
   if(!data.includes("CACHE='ium-klasse5-mantel-'") )throw Error('Offlinekennung nicht gefunden');
   data=data.replace("CACHE='ium-klasse5-mantel-'","CACHE='ium-recherche-beispiel-20261013-'");
  }
  bundle.set(name,data);
 }
 const version=hash(Buffer.concat([...bundle.values()].map(data=>Buffer.from(data)))).slice(0,12);
 bundle.set('klasse5/mantel-sw.js',bundle.get('klasse5/mantel-sw.js').replace(/const VERSION='[a-f0-9]{12}'/,"const VERSION='"+version+"'"));
 bundle.set('index.html',entry());
 for(const [name,data]of bundle){const target=prefix+name;if(result.has(target))throw Error('Bestehender Pages-Pfad: '+target);result.set(target,data);}
 if(result.has('beispiele/index.html'))throw Error('Beispieleinstieg existiert bereits');
 result.set('beispiele/index.html',overview());
 for(const [name,data]of result){
  if(!name.endsWith('.html'))continue;
  for(const [,ref]of data.matchAll(/(?:href|src)="([^"]+)"/g)){
   if(/^(?:https?:|mailto:|tel:|data:|#)/i.test(ref))continue;
   const target=new URL(ref,'https://example.test/ium-lernwerk/'+name);
   if(!target.pathname.startsWith('/ium-lernwerk/'))throw Error('Pages-Pfad verlassen: '+name+' → '+ref);
   const local=decodeURIComponent(target.pathname.slice('/ium-lernwerk/'.length)),file=local.endsWith('/')?local+'index.html':local;
   if(!result.has(file))throw Error('Unveröffentlichter Verweis: '+name+' → '+ref+' → '+file);
  }
 }
 for(const [name,data]of old)if(hash(data)!==hash(result.get(name)))throw Error('Alte Version verändert: '+name);
 return result;
}
function build(output=path.resolve(__dirname,'../../dist/klasse5-pages')){
 if(fs.existsSync(output))throw Error('Buildausgabe existiert bereits; frisches Ziel wählen.');
 const assets=prepareAdditionalPages();
 for(const [name,data]of assets){const file=path.join(output,name);fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,data);}
 console.log('Validated and staged '+assets.size+' Pages-Dateien einschließlich zusätzlichem Recherche-Beispiel in '+output);
}
if(require.main===module)build(process.argv[2]?path.resolve(process.argv[2]):undefined);
module.exports={prepareAdditionalPages,build,prefix};
