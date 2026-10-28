'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {prepareAdditionalPages}=require('../recherche-beispiel/build.cjs');
const {augment}=require('../shared/class6-render.cjs');
const preserved=require('./bestand-sha256.json');
const {addClass7}=require('../klasse7-programmieren/build.cjs');
const {addMedia,connectMedia}=require('../klasse7-medien/build.cjs');
const digest=data=>crypto.createHash('sha256').update(data).digest('hex');
function preparePages(){
 const old=prepareAdditionalPages(),all=addMedia(addClass7(augment(new Map(old))));
 for(const [name,hash]of Object.entries(preserved.files)){
  if(!all.has(name)||digest(all.get(name))!==hash)throw Error('Veröffentlichter Bestand verändert: '+name);
 }
 for(const name of old.keys())if(!Object.hasOwn(preserved.files,name))throw Error('Ungeprüfter Bestandspfad: '+name);
 for(const name of all.keys())if(!old.has(name)&&!name.startsWith('klasse6/')&&!name.startsWith('klasse7/'))throw Error('Zusatz außerhalb Klasse 6/7: '+name);
 for(const [name,data]of all){
  if(name.startsWith('klasse6/')||name.startsWith('klasse7/')){
   if(/(?:^|\/)(?:docs|qa|quelle|node_modules|\.git)(?:\/|$)|\.(?:test\.cjs|py|log)$/i.test(name))throw Error('Interner Pfad: '+name);
   if(typeof data==='string'&&(!name.startsWith('klasse7/programmieren/snap/src/')||name.endsWith('.html'))&&/C:[\\/]Users[\\/]|127\.0\.0\.1|localhost/i.test(data))throw Error('Lokaler Verweis: '+name);
  }
  if(!name.endsWith('.html'))continue;
  for(const [,ref]of data.matchAll(/(?:href|src)="([^"]+)"/g)){
   if(/^(?:https?:|mailto:|tel:|data:|#)/i.test(ref))continue;
   const target=new URL(ref,'https://example.test/ium-lernwerk/'+name);
   if(!target.pathname.startsWith('/ium-lernwerk/'))throw Error('Pages-Unterpfad verlassen: '+name+' → '+ref);
   const local=decodeURIComponent(target.pathname.slice('/ium-lernwerk/'.length)),file=local.endsWith('/')?local+'index.html':local;
   if(!all.has(file))throw Error('Unveröffentlichter Verweis: '+name+' → '+ref);
  }
 }
 return all;
}
function preparePublishedPages(){return require('../shared/grade-navigation.cjs').addGradeNavigation(connectMedia(require('../klasse7-programmieren/layout.cjs').applySeriesLayout(preparePages())));}
function build(output=path.resolve(__dirname,'../../dist/klasse5-pages')){
 if(fs.existsSync(output))throw Error('Buildausgabe existiert bereits; frisches Ziel wählen.');
 const all=preparePublishedPages();
 for(const [name,data]of all){const file=path.join(output,name);fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,data);}
 console.log(`Validated and staged ${all.size} Pages-Dateien; ${Object.keys(preserved.files).length} Bestandsdateien als Ausgang gebunden; Klassenstufen-Navigation ergänzt in ${output}`);
}
if(require.main===module)build(process.argv[2]?path.resolve(process.argv[2]):undefined);
module.exports={preparePages,preparePublishedPages,build};
