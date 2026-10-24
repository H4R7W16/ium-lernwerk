'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const baseline=require('./bestand-sha256.json');
const hash=data=>crypto.createHash('sha256').update(data).digest('hex');
function addClass7(existing){
 for(const [name,h]of Object.entries(baseline.files))if(!existing.has(name)||hash(existing.get(name))!==h)throw Error('Veröffentlichter Bestand verändert: '+name);
 for(const name of existing.keys())if(!Object.hasOwn(baseline.files,name))throw Error('Ungebundener bisheriger Pfad: '+name);
 const all=new Map(existing),root=path.join(__dirname,'inhalt');
 function walk(dir,base=''){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const name=path.posix.join(base,e.name),file=path.join(dir,e.name);if(e.isSymbolicLink())throw Error('Symlink im Inhalt: '+name);if(e.isDirectory()){walk(file,name);continue;}if(!name.startsWith('klasse7/'))throw Error('Zusatz außerhalb Klasse 7: '+name);if(all.has(name))throw Error('Bestehender Pages-Pfad: '+name);if(/(?:^|\/)(?:qa|quellen|node_modules|\.git)(?:\/|$)|(?:run\.json|\.env|\.test\.cjs)$/.test(name))throw Error('Interner Pfad: '+name);const b=fs.readFileSync(file),text=/\.(?:html|css|js|xml|json|md|txt)$/.test(name)||name.endsWith('/LICENSE');const data=text?b.toString('utf8'):b;if(name.endsWith('.html')&&/C:[\\/]Users[\\/]|127\.0\.0\.1|localhost/i.test(data))throw Error('Lokaler Verweis: '+name);all.set(name,data);}}
 walk(root);return all;
}
module.exports={addClass7};
