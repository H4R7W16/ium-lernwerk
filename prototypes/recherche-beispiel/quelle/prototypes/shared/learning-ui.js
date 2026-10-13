/* Kleine gemeinsame Darstellungsbausteine, ohne eigenen Lern- oder Speicherzustand. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.LernwerkUI=factory();})(globalThis,function(){
'use strict';
const e=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function navigation(title,steps,current){const index=Math.max(0,steps.findIndex(s=>s.id===current));return '<div class="lw-step-location"><span>'+e(title)+'</span><b>'+e(steps[index].short||steps[index].title)+' · Schritt '+(index+1)+' von '+steps.length+'</b></div><details class="lw-step-menu" data-lw-menu><summary>Alle Schritte <span aria-hidden="true">⌄</span></summary><div class="lw-step-options">'+steps.map((s,i)=>'<a href="#'+e(s.id)+'" data-step="'+e(s.id)+'"'+(i===index?' aria-current="step"':'')+'><span>'+String(i+1).padStart(2,'0')+'</span>'+e(s.short||s.title)+'</a>').join('')+'</div></details>';}
function intro(title,task){return '<header class="lw-lesson-intro"><h1>'+e(title)+'</h1><p><b>Dein Auftrag</b> '+e(task)+'</p></header>';}
function criteria(items,outcome){return '<section class="lw-self-check"><div><p class="lw-eyebrow">Jetzt erklärst du</p><h2>Prüfe dein Ergebnis</h2><p>'+e(outcome)+'</p><p class="lw-small">Vergleiche deine eigene Erklärung mit den Kriterien. Du kannst hier, mündlich oder im Heft arbeiten.</p></div><ul>'+items.map(t=>'<li>'+e(t)+'</li>').join('')+'</ul></section>';}
function back(other='material'){return '<nav class="lw-return" aria-label="Zurück und weiter"><a href="index.html" data-lw-return>← Zurück zu deiner Aufgabe</a><a href="'+other+'.html">'+(other==='material'?'Unterrichtsmaterial':'Wissen und Beispiele')+' →</a></nav>';}
return {escape:e,navigation,intro,criteria,back};
});
