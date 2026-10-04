/* Keyboard and touch use native controls; no drag-only action. */
document.addEventListener('DOMContentLoaded',()=>{
'use strict';
const root=document.querySelector('[data-net-tool]');if(!root)return;
const M=window.NetModel,V=window.NetView,$=id=>document.getElementById(id);
let state=M.create();
const e=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const resultNames={answered:'Dateiantwort bei K angekommen',blocked:'Gewählter Weg unterbrochen','wrong-target':'Anderer Endpunkt erreicht','no-service':'Ziel erreicht, keine Dateiantwort',stopped:'Versuch vorzeitig beendet'};
function draw(){
 const t=state.current,r=t?M.observe(t):null,c=t?t.config:state.draft;
 $('net-diagram').innerHTML=V.svg(c.disabled,r?.at||'',true);
 $('net-connections').textContent=M.edges().map(x=>x+': '+(c.disabled.includes(x)?'unterbrochen':'aktiv')).join(' · ');
 $('net-trial').textContent='Ziel '+c.target+' · Dienst '+(c.service?'bereit':'nicht bereit')+' · Unterbrochen: '+(c.disabled.join(', ')||'keine');
 $('net-path').textContent=r?'Bisheriger Anfrageweg: '+r.path.join(' → '):'';
 $('net-current-trace').hidden=!t;
 if(t)$('net-settings').open=false;
 $('net-config').disabled=!!t;
 $('net-target').value=state.draft.target;$('net-service').checked=state.draft.service;$('net-prediction').value=state.draft.prediction;
 root.querySelectorAll('[data-net-edge]').forEach(n=>n.checked=c.disabled.includes(n.dataset.netEdge));
 $('net-actions').innerHTML=t?(r.phase==='reply'?'<button class="lw-button" data-net-move="reply">Antwort: einen Schritt zurück</button>':M.neighbors(r.at).filter(n=>!r.path.includes(n)).map(n=>'<button class="lw-button secondary" data-net-move="'+n+'">Anfrage von '+r.at+' nach '+n+'</button>').join(''))+'<button class="lw-button secondary" id="net-stop">Versuch beenden</button>':state.history.length?'<button class="lw-button secondary" id="net-prepare">Nächsten Versuch vorbereiten</button>':'';
 $('net-trace').innerHTML=(r?.trace||[]).map(x=>'<li>'+e(x)+'</li>').join('');$('net-count').textContent=state.history.length;
 $('net-records').innerHTML=state.history.map((h,i)=>'<article><h3>Versuch '+(i+1)+' · '+e(resultNames[M.observe(h).outcome])+'</h3><p>Ziel '+h.config.target+' · Unterbrochen: '+e(h.config.disabled.join(', ')||'keine')+' · Dienst '+(h.config.service?'bereit':'nicht bereit')+'</p><p><b>Deine ursprüngliche Vermutung:</b> '+e(h.prediction)+'</p><ol>'+M.observe(h).trace.map(x=>'<li>'+e(x)+'</li>').join('')+'</ol><details><summary>Nach dem Versuch: erreichbare Knoten vergleichen</summary><p>Über alle möglichen aktiven Wege von K erreichbar: '+M.reachable(h.config).join(', ')+'. Das sagt noch nicht, ob der Dateidienst bereit ist. Begründe mit Verbindungen, weshalb weitere Knoten erreichbar oder abgetrennt sind.</p></details></article>').join('');
}
function update(fn,message,focus=false){
 try{state=fn(state);draw();$('net-message').textContent=typeof message==='function'?message():message;window.LernwerkMantel.changed();if(focus){$('net-message').focus({preventScroll:true});$('net-workbench').scrollIntoView({block:'start'});}}
 catch(err){$('net-message').textContent=err.message;$('net-message').focus();}
}
$('net-config').addEventListener('input',ev=>{
 const patch=ev.target.id==='net-prediction'?{prediction:ev.target.value}:ev.target.id==='net-target'?{target:ev.target.value}:ev.target.id==='net-service'?{service:ev.target.checked}:{disabled:[...root.querySelectorAll('[data-net-edge]:checked')].map(n=>n.dataset.netEdge)};
 state=M.configure(state,patch);if(ev.target.id!=='net-prediction')draw();window.LernwerkMantel.changed();
});
$('net-start').onclick=()=>update(M.start,'Anfrage steht bei K. Wähle den nächsten Knoten.',true);
$('net-reset').onclick=()=>update(M.reset,'Grundnetz wieder aktiv. Bisherige Protokolle bleiben erhalten.');
root.addEventListener('click',ev=>{
 const b=ev.target.closest('button');
 if(b?.dataset.netMove)update(s=>M.move(s,b.dataset.netMove),()=>state.current?'Jetzt bei '+M.observe(state.current).at+'. Wähle den nächsten Schritt.':resultNames[M.observe(state.history.at(-1)).outcome]+'. Spur in den Versuchsprotokollen; erkläre deine Beobachtung.',true);
 if(b?.id==='net-prepare'){$('net-settings').open=true;$('net-prediction').focus();}
 if(b?.id==='net-stop')update(M.stop,'Versuch beendet und protokolliert. Ein vorzeitiger Stopp beweist keine Unerreichbarkeit.',true);
});
window.LernwerkMantel.register({capture:()=>({family:'content',kind:'network',state:M.valid(state)?structuredClone(state):null}),restore(tool){if(!M.valid(tool.state))throw new Error('Netzstand ungültig');state=structuredClone(tool.state);draw();if(state.current)$('net-message').textContent='Versuch fortsetzen: bei '+M.observe(state.current).at+'. Wähle den nächsten Schritt.';}});
draw();
});
