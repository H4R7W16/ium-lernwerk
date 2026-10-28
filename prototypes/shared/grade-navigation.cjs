'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const destinations=['klasse5/index.html','klasse6/index.html','klasse7/programmieren/index.html'];
const sha=value=>crypto.createHash('sha256').update(value).digest('hex');
function context(name){
 const match=name.match(/^klasse([56])\//);
 if(match)return {grade:Number(match[1]),root:'klasse'+match[1]+'/'};
 if(name.startsWith('klasse7/gaming/'))return {grade:7,root:'klasse7/gaming/'};
 if(name.startsWith('klasse7/daten/'))return {grade:7,root:'klasse7/daten/'};
 if(name.startsWith('klasse7/medien/'))return {grade:7,root:'klasse7/medien/'};
 return name.startsWith('klasse7/programmieren/')?{grade:7,root:'klasse7/programmieren/'}:null;
}
function relative(name,target){return path.posix.relative(path.posix.dirname(name),target);}
function enhance(name,html,info){
 const header=html.match(/<header\b[^>]*>[\s\S]*?<\/header>/)?.[0];
 const brand=header?.match(/<a class="(lw-shell-brand|brand)"[^>]*>([\s\S]*?)<\/a>/);
 if(!brand)return null;
 let content=brand[2];
 if(info.grade===7&&!content.includes('class-label'))content=content.replace('Lernwerk</span>','Lernwerk <span class="lw-grade-number" aria-hidden="true">7</span></span>');
 const links=destinations.map((target,index)=>'<a href="'+relative(name,target)+'"'+(index+5===info.grade?' aria-current="true"':'')+'>Klasse '+(index+5)+(index+5===info.grade?'<span aria-hidden="true">Aktuell</span>':'')+'</a>').join('');
 const menu='<details class="lw-grade-switch" data-grade-switch><summary class="'+brand[1]+' lw-grade-summary" aria-label="Klassenstufe wählen, aktuell Klasse '+info.grade+'" title="Klassenstufe wechseln">'+content+'<span class="lw-grade-chevron" aria-hidden="true">▾</span></summary><nav class="lw-grade-options" aria-label="Klassenstufe">'+links+'</nav></details>';
 let next=header.replace(brand[0],menu);
 if(info.grade===7)next=next.replace('<span class="header-context">Klasse 7 · Programmieren</span>','<span class="header-context">Programmieren</span>');
 const dependencies='<link rel="stylesheet" href="'+relative(name,info.root+'grade-navigation.css')+'"><script src="'+relative(name,info.root+'grade-navigation.js')+'" defer></script>';
 return html.replace(header,next).replace('</head>',dependencies+'</head>');
}
function refreshWorker(all,root){
 const name=root+'mantel-sw.js',worker=all.get(name);
 if(!worker)return;
 const list=worker.match(/FILES=(\[[^\r\n]*?\]),CACHE=/);
 if(!list||!/const VERSION='[a-f0-9]{12}'/.test(worker))throw Error('Unbekanntes Offlinepaket: '+name);
 const files=JSON.parse(list[1]);
 for(const file of ['grade-navigation.css','grade-navigation.js'])if(!files.includes(file))files.push(file);
 const hash=crypto.createHash('sha256');
 for(const [file,value]of [...all].filter(([file])=>file.startsWith(root)&&file!==name).sort(([a],[b])=>a<b?-1:a>b?1:0)){hash.update(file);hash.update(value);}
 all.set(name,worker.replace(/const VERSION='[a-f0-9]{12}'/,"const VERSION='"+hash.digest('hex').slice(0,12)+"'").replace(list[0],'FILES='+JSON.stringify(files)+',CACHE='));
}
function bindEditorShell(all){
 const root='klasse7/programmieren/',name=root+'snap/lernwerk-herkunft.json';
 if(!all.has(name))return;
 const manifest=JSON.parse(all.get(name)),shell='lernwerk.html';
 const current=sha(all.get(root+'snap/'+shell));
 if(current===manifest.files[shell])return;
 manifest.navigation={version:'1.0.0',date:'2026-10-27',scope:'Klassenstufen-Auswahl in der Lernwerk-Kopfzeile',sourceShellSha256:manifest.files[shell],assets:Object.fromEntries(['grade-navigation.css','grade-navigation.js'].map(file=>['../'+file,sha(all.get(root+file))]))};
 manifest.files[shell]=current;
 all.set(name,JSON.stringify(manifest,null,2)+'\n');
}
function validateLinks(all){
 for(const [name,html]of all){if(!name.endsWith('.html'))continue;
  for(const [,ref]of html.matchAll(/(?:href|src)="([^"]+)"/g)){
   if(/^(?:https?:|mailto:|tel:|data:|#)/i.test(ref))continue;
   const url=new URL(ref,'https://example.test/ium-lernwerk/'+name);
   if(!url.pathname.startsWith('/ium-lernwerk/'))throw Error('Pages-Unterpfad verlassen: '+name+' → '+ref);
   const local=decodeURIComponent(url.pathname.slice('/ium-lernwerk/'.length)),file=local.endsWith('/')?local+'index.html':local;
   if(!all.has(file))throw Error('Unveröffentlichter Verweis: '+name+' → '+ref);
  }
 }
}
function addGradeNavigation(source){
 const all=new Map(source),roots=new Set();
 for(const [name,html]of source){const info=context(name);if(!info||!name.endsWith('.html'))continue;
  const next=enhance(name,html,info);if(next===null)continue;all.set(name,next);roots.add(info.root);
 }
 for(const root of roots)for(const file of ['grade-navigation.css','grade-navigation.js'])all.set(root+file,fs.readFileSync(path.join(__dirname,file),'utf8'));
 for(const root of roots)refreshWorker(all,root);
 bindEditorShell(all);validateLinks(all);
 return all;
}
module.exports={addGradeNavigation};
