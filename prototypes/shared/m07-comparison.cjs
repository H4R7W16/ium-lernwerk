'use strict';
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function validate(model){
 const text=v=>typeof v==='string'&&!!v.trim();
 if(!model||!text(model.badClaim)||!text(model.readingPrompt)||!model.facts)throw Error('Bibliotheksvergleich braucht Ausgangsaussage und gemeinsame Fakten');
 for(const key of ['question','validity','instruction','oldNotice','source','credit'])if(!text(model.facts[key]))throw Error('Bibliotheksvergleich: '+key+' fehlt');
 const loans=model.facts.loans;if(!Array.isArray(loans)||loans.length!==2||loans.some(row=>!Array.isArray(row)||row.length!==2||row.some(v=>!text(v)))||loans[0][0]===loans[1][0])throw Error('Bibliotheksvergleich braucht zwei verschiedene Buchgruppen mit Frist');
 return model;
}
const star='<svg class="m07-star" viewBox="0 0 100 100" aria-hidden="true" focusable="false"><path d="M50 3 61 36 96 36 68 57 79 91 50 70 21 91 32 57 4 36 39 36Z" fill="#e2b34f"/></svg>';
function card(model,state){
 validate(model);if(!['A','B','C'].includes(state))throw Error('Unbekannter Bibliotheksstand');
 const f=model.facts,rough=state!=='C',label={A:'A · Erster Entwurf',B:'B · Inhalt berichtigt',C:'C · Klarer gestaltet'}[state];
 const fact=(key,text,cls='')=>'<p data-m07-fact="'+key+'"'+(cls?' class="'+cls+'"':'')+'>'+esc(text)+'</p>';
 const loans=f.loans.map(([name,period],i)=>'<div data-m07-fact="loan-'+i+'" class="m07-loan"><span class="m07-book-name">'+esc(name)+'</span> <span class="m07-period">'+esc(period)+'</span></div>').join('');
 const content=state==='A'?'<p class="m07-question">'+esc(f.question)+'</p><p class="m07-bad-claim">'+esc(model.badClaim)+'</p>'+star+'<p class="m07-old-copy">Aus dem alten Mai-Aushang übernommen.</p>':fact('question',f.question,'m07-question')+fact('validity',f.validity,'m07-validity')+'<div class="m07-loans">'+loans+'</div>'+(rough?star:'')+fact('instruction',f.instruction)+fact('oldNotice',f.oldNotice)+fact('source',f.source,'m07-source')+fact('credit',f.credit,'m07-source');
 return '<figure id="m07-state-'+state.toLowerCase()+'" data-m07-state="'+state+'" class="m07-card m07-state-'+state.toLowerCase()+'"><figcaption>'+label+'</figcaption><div class="m07-card-body '+(rough?'m07-rough':'m07-clear')+'">'+content+'</div></figure>';
}
function render(model,{paper=false,standalone=false}={}){
 validate(model);
 const focus='<p class="m07-focus"><strong>Darauf achtest du:</strong> '+esc(model.readingPrompt)+'</p>';
 const purpose='<p id="m07-gestaltung-hilfe" class="m07-comparison-help">B und C enthalten dieselben Informationen.</p>';
 const control='<input type="checkbox" id="m07-correction" class="m07-choice" aria-controls="m07-state-a m07-state-b" aria-describedby="m07-gestaltung-hilfe"><label for="m07-correction">Bei Bedarf: Nur die Gestaltung vergleichen (B statt A)</label>';
 const grid='<div class="m07-compare-grid">'+card(model,'A')+(paper?'':card(model,'B'))+card(model,'C')+'</div>';
 const help=paper?'<details class="lw-help m07-paper-help"><summary>Bei Bedarf: Zwischenstand B ansehen</summary><p>B und C enthalten dieselben Informationen. B behält die einfache Gestaltung von A.</p>'+card(model,'B')+'</details>':'';
 return '<section id="m07-vergleich" class="m07-comparison m07-comparison-'+(paper?'paper':'screen')+'" aria-label="Bibliothekskarte: Inhalt und Gestaltung vergleichen">'+focus+(paper?'':purpose+control)+grid+help+'<p class="m07-comparison-credit">Erfundener Bibliotheksfall · eigene Darstellung · IuM-Lernwerk · CC BY-SA 4.0</p>'+(!paper&&!standalone?'<nav class="lw-reading-links" aria-label="Vergleichsansicht"><a href="bild-vergleich.html">Vergleich einzeln öffnen →</a></nav>':'')+'</section>';
}
function modelFrom(pack){return pack.grade===6&&pack.area==='medienprodukt'?pack.steps.find(s=>s.id==='auftrag')?.blocks.find(b=>b.libraryComparison)?.libraryComparison:null;}
function integrate(pack,pages){
 const model=modelFrom(pack);if(!model)return pages;const out=new Map(pages);
 out.set('bild-vergleich.html','<article class="lw-author"><p><a href="schritt-auftrag.html#m07-vergleich">← Zurück zum Bibliotheksvergleich im Auftrag</a></p><h1>Inhalt und Gestaltung vergleichen</h1>'+render(model,{standalone:true})+'<p><a href="schritt-auftrag.html#arbeitsstelle-was-bewirkt-die-anderung">Zur eigenen Erklärung →</a></p></article>');
 const material=out.get('material.html'),marker='<ol class="lw-material-list">';if(!material?.includes(marker))throw Error('M07-Materialzugang fehlt');
 out.set('material.html',material.replace(marker,'<nav class="lw-reading-links" aria-label="Bibliotheksvergleich"><a href="bild-vergleich.html">Bibliotheksvergleich einzeln öffnen →</a></nav>'+marker));
 return out;
}
module.exports={validate,card,render,modelFrom,integrate};
