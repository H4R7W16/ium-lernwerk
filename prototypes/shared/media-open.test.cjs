const test=require('node:test'),a=require('node:assert/strict'),A=require('./class5-content.cjs'),R=require('./class5-author-render.cjs');
test('Statische Lernbilder lassen sich in Lernschritt und Papierquelle groß öffnen; Dateiaufträge bleiben Downloads',()=>{
 const p=A.load().find(p=>p.area==='geraete'),m=p.media.find(m=>m.kind==='image');
 const html=A.mediaHTML([m.id],p);a.match(html,/class="lw-media-open no-print"/);a.ok(html.includes('href="bild-'+m.id+'.html"'));a.doesNotMatch(html,/target="_blank"/); const viewer=R.render(p).get("bild-"+m.id+".html"); a.match(viewer,/lw-image-view/); a.match(viewer,/data-lw-return/); a.ok(viewer.includes(m.file));
 const dl=A.load().find(p=>p.area==='dateien'),d=dl.media.find(m=>m.kind==='download');a.doesNotMatch(A.mediaHTML([d.id],dl),/lw-media-open/);a.match(A.mediaHTML([d.id],dl),/ download/);
 for(const file of ['schritt-auftakt.html','baustein-auftakt.html'])a.match(R.render(p).get(file),/lw-media-open/);
});
