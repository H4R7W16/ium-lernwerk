'use strict';
// Unterrichtsspezifische Anordnung. Alle Antwortfelder bleiben normale Mantel-Felder.
const A=require('./class5-content.cjs'),e=A.esc;
const lookupSteps=new Set(['ueben','grenzen','nachricht','stoerung','revision','transfer']);
function reference(pack){
 const table=pack.steps.find(s=>s.id==='regeln').blocks.find(b=>b.table?.headers.includes('Code Z')).table;
 return '<details class="lw-code-reference" data-code-reference open><summary>Codetabelle Z und B</summary><p class="lw-small">Z: zwei Stellen · B: fünf Stellen. Die Tabelle darfst du jederzeit benutzen.</p><div class="lw-code-scroll" tabindex="0" role="region" aria-label="Codetabelle zum Nachschlagen"><table><thead><tr>'+table.headers.map(h=>'<th scope="col">'+e(h)+'</th>').join('')+'</tr></thead><tbody>'+table.rows.map(row=>'<tr>'+row.map(v=>'<td>'+e(v)+'</td>').join('')+'</tr>').join('')+'</tbody></table></div></details>';
}
function savedCodes(step){
 if(!['stoerung','revision'].includes(step.id))return '';
 const field=(id,title)=>'<label for="answer-nachricht-'+id+'">'+title+'</label><textarea id="answer-nachricht-'+id+'" readonly rows="2" maxlength="10000" aria-label="'+title+'"></textarea>';
 return '<details class="lw-code-saved" open><summary>Deine Codes aus Schritt 5</summary><p class="lw-small">Hier nur lesen. Wenn die Felder leer sind, <a href="schritt-nachricht.html">lege zuerst deine Nachricht an</a>. Auf Papier: deinen Codezettel bereitlegen.</p>'+field('code-z','Dein Z-Code aus Schritt 5')+field('code-b','Dein B-Code aus Schritt 5')+'<details><summary>Original zum Vergleichen öffnen</summary>'+field('akte','Deine ursprüngliche Nachricht')+'</details></details>';
}
function render(step,pack,options={}){
 const content=step.blocks.map(b=>{
  const html=A.renderBlocks({...step,blocks:[b]},pack,options);
  return !options.paper&&step.id==='nachricht'&&b.id==='akte'?'<details class="lw-code-original" data-code-original open><summary>Original ein-/ausblenden</summary>'+html+'</details>':html;
 }).join('');
 if(options.paper||!lookupSteps.has(step.id))return content;
 return '<div class="lw-code-work"><div class="lw-code-tasks">'+savedCodes(step)+content+'</div><aside class="lw-code-aids" aria-label="Beim Codieren nachschlagen">'+reference(pack)+'</aside></div>';
}
module.exports={render};
