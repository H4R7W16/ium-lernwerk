'use strict';
// Eigene geometrische Modelle, CC BY-SA 4.0; Erzeugungscode MIT.
const fs=require('node:fs'),path=require('node:path');
function inside(key,x,y){
 const d=Math.hypot(x-2,y-2);
 return (d<=1.8&&d>=.8)||(x>=3&&x<=7.7&&y>=2.4&&y<=3.6)||
 (x>=4.8&&x<=5.8&&y>=3.4&&y<=6.2)||(x>=6.8&&x<=7.7&&y>=3.4&&y<=(key===1?5.2:5.8));
}
function raster(key,n){return Array.from({length:n},(_,y)=>Array.from({length:n},(_,x)=>inside(key,(x+.5)*8/n,(y+.5)*8/n)?'1':'0').join(''));}
function geometry(key){return '<path fill-rule="evenodd" d="M3.8 2A1.8 1.8 0 1 0 .2 2A1.8 1.8 0 1 0 3.8 2ZM2.8 2A.8 .8 0 1 0 1.2 2A.8 .8 0 1 0 2.8 2Z"/><path d="M3 2.4H7.7V3.6H3Z M4.8 3.4H5.8V6.2H4.8Z M6.8 3.4H7.7V'+(key===1?'5.2':'5.8')+'H6.8Z"/>';}
function panel(key,n){
 if(!n)return geometry(key);
 let s='';for(const[y,row]of raster(key,n).entries())for(const[x,bit]of [...row].entries())if(bit==='1')s+='<rect x="'+(x*8/n)+'" y="'+(y*8/n)+'" width="'+(8/n)+'" height="'+(8/n)+'"/>';
 for(let i=0;i<=n;i++)s+='<path d="M'+(i*8/n)+' 0V8M0 '+(i*8/n)+'H8" fill="none" stroke="#82908c" stroke-width=".02"/>';
 return s;
}
function image(n){return '<svg xmlns="http://www.w3.org/2000/svg" width="800" height="420" viewBox="0 0 800 420" role="img" aria-labelledby="t d"><title id="t">Schlüssel I und II · '+(n?n+' × '+n+' Pixel':'Vorlagen')+'</title><desc id="d">Zwei konstruierte Schlüsselmodelle in gleicher Anzeigegröße, I links und II rechts. '+(n?'Die feldweisen Werte stehen in den zugehörigen Tabellen der Lernseite.':'Konturen zur Gegenprüfung nach dem eigenen Urteil.')+'</desc><rect width="800" height="420" rx="12" fill="#f2f5f1"/>'+[1,2].map((key,i)=>'<text x="'+(40+i*400)+'" y="45" font-family="Arial,sans-serif" font-size="40" fill="#172026">'+(key===1?'I':'II')+'</text><g transform="translate('+(40+i*400)+' 70) scale(40)"><rect width="8" height="8" fill="white"/><g fill="#172026">'+panel(key,n)+'</g><rect width="8" height="8" fill="none" stroke="#82908c" stroke-width=".035"/></g>').join('')+'</svg>\n';}
function generate(out){fs.mkdirSync(out,{recursive:true});const model={rule:'Mittelpunkt auf schwarzer Form; Rand zählt schwarz',bounds:{ring:{cx:2,cy:2,outer:1.8,inner:.8},shaft:[3,2.4,7.7,3.6],toothLeft:[4.8,3.4,5.8,6.2],toothRightI:[6.8,3.4,7.7,5.2],toothRightII:[6.8,3.4,7.7,5.8]},rasters:{I4:raster(1,4),II4:raster(2,4),I8:raster(1,8),II8:raster(2,8)}};for(const n of [4,8])fs.writeFileSync(path.join(out,'schluesselpaar-'+n+'.svg'),image(n));fs.writeFileSync(path.join(out,'schluesselpaar-vorlagen.svg'),image(null));fs.writeFileSync(path.join(out,'schluesselpaar-modell.json'),JSON.stringify(model,null,2)+'\n');return model;}
if(require.main===module){if(!process.argv[2])throw Error('Ausgabeordner angeben');generate(path.resolve(process.argv[2]));}
module.exports={generate,raster};
