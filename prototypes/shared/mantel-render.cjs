'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {catalog,orderUnits}=require('./class5-catalog.cjs');
const learningPages=require('./learning-pages.cjs'),teacherPages=require('./class5-teacher-pages.cjs');
const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function terminology(html){return html.replace(/eine einzelne Station/g,'einen einzelnen Schritt').replace(/Vorige Station/g,'Voriger Schritt').replace(/Station (?=\d)/g,'Schritt ').replace(/target="_blank"\s*rel="noopener"/g,'').replace(/\bStationen\b/g,'Schritte').replace(/\bEtappen\b/g,'Lernweg').replace(/\bEtappe\b/g,'Schritt').replace(/\bETAPPE\b/g,'SCHRITT').replace(/Tipp 1/g,'Ein Hinweis').replace(/Tipp 2/g,'Eine genauere Hilfe').replace(/Einen Hinweis/g,'Ein Hinweis').replace(/öffnen ↗/g,'öffnen').replace(/dazu ↗/g,'dazu');}
function header(units,unit,file,up){
 const target=unit?unit.area+'/':'',prefix=unit? '../':'';
 const topics=units.map((u,i)=>'<a href="'+prefix+u.area+'/index.html"><strong>0'+(i+1)+' · '+e(u.topic)+'</strong><small>'+e(u.title)+'</small></a>').join('');
 const nav=[['wissen.html','Wissen'],['material.html','Unterrichtsmaterial'],['arbeit.html','Deine Arbeit']];
 return '<header class="lw-shell-header"><div class="lw-shell-identity"><a class="lw-shell-brand" href="'+up+'index.html" aria-label="Lernwerk Übersicht">Lernwerk<span>.</span></a><span class="lw-shell-location">Klasse 5'+(unit?'<b>'+e(unit.topic)+'</b>':'')+'</span></div><nav class="lw-shell-nav" aria-label="Lernwerk"><details data-lw-menu><summary>Themen ▾</summary><div class="lw-shell-topics">'+topics+'<button type="button" data-lw-close-menu>Schließen</button></div></details>'+nav.map(([f,l])=>'<a href="'+(f==='arbeit.html'?up:unit?'':up)+f+'"'+(file===f?' aria-current="page"':'')+'>'+l+'</a>').join('')+'</nav></header>';
}
function printControls(file){return /material|baustein/.test(file)?'<div class="lw-print-controls no-print"><label for="lw-print-mode">Druckansicht</label><select id="lw-print-mode"><option value="learner">Lernendenblatt</option><option value="helpers">Mit Hilfen</option><option value="solutions">Mit Hilfen und Lösungen</option></select><button id="lw-print" class="lw-button secondary">Gewählte Ansicht drucken</button><p>Eigene Antworten und private Notizen werden nicht mitgedruckt.</p></div>':'';}
function foot(up){return '<footer class="lw-footer"><span>IuM · Klasse 5</span><span><a href="'+up+'lehrkraft.html">Für Lehrpersonen</a> · <a href="'+up+'informationen.html">Quellen, Lizenz und Bedienhilfe</a></span></footer>';}
function sharedScripts(up){return ['learning-ui.js','selbstlernen/cleaning-core.js','selbstlernen/model.js','lernwerkstatt/workshop-model.js','lernstudio/studio-model.js','mantel-model.js','mantel-runtime.js'].map(f=>'<script src="'+up+f+'"></script>').join('');}
function storageStatus(){return '<p class="lw-state-status" id="lw-storage-status" role="status">Deine Lernwerk-Antworten und Werkzeugstände bleiben zunächst in diesem Browsertab.</p><p class="lw-storage-warning" id="lw-storage-warning" role="alert"></p><button id="lw-emergency-export" class="lw-button secondary lw-emergency-export" hidden>Arbeitsdatei sichern</button>';}
function page(title,body,units,unit=null,file='index.html'){
 const up=unit?'../':'';
 return '<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>'+e(title)+' · IuM Lernwerk</title><link rel="stylesheet" href="'+up+'mantel.css"><link rel="stylesheet" href="'+up+'learning-ui.css"><link rel="manifest" href="'+up+'manifest.webmanifest"><meta name="theme-color" content="#24543e">'+sharedScripts(up)+'<script type="application/json" id="lw-catalog">'+JSON.stringify(units).replaceAll('<','\\u003c')+'</script></head><body class="lw-mantel" data-lw-print="learner" data-lw-area="'+(unit?unit.area:'')+'" data-lw-page="'+file+'"><a class="skip" href="#main">Zum Inhalt</a>'+header(units,unit,file,up)+''+storageStatus()+'<main id="main" tabindex="-1" class="lw-page">'+body+printControls(file)+'</main>'+foot(up)+'</body></html>';
}
function cards(units,target){return learningPages.cards(units,target);}
function teacherPreparation(){return '<section class="lw-notice"><h2>Vor dem Einsatz an Ihrer Schule</h2><p>Prüfen Sie Geräte, Zugänge und benötigte Sozialphasen. Bei sensiblen Themen klären Sie die zuständigen schulischen Hilfe- und Meldewege, prüfen deren Aktualität und machen sie den Lernenden passend zugänglich. Das schulübergreifende Lernwerk enthält keine lokalen Kontakte.</p><p>Persönliche Anliegen werden nicht als Lernantwort verlangt. Eine harmlose eigene Erfahrung oder Nichtnutzung kann privat reflektiert werden. Neutrale Fälle ersetzen einen geforderten Eigenbezug nicht automatisch. Hilfe bei einem Anliegen und fachliche Selbstprüfung bleiben getrennt.</p></section>';}
function retrieval(unit,units){
 const cases={
 algorithm:['Ein Roboter startet in Spalte 2, Reihe 2 und blickt nach oben. Das Programm lautet: rechts; vor; links. Wo endet er und wohin blickt er? Erkläre bei jeder Drehung, was gleich bleibt.','Nach rechts dreht er auf der Stelle und blickt rechts. Er fährt zur Spalte 3, Reihe 2. Die Linksdrehung lässt ihn dort stehen und nach oben blicken.'],
 media:['Eine Bildunterschrift behauptet: „Niemand nutzt unsere Bibliothek.“ Auf dem Ausschnitt sind leere Sessel zu sehen. Was kannst du belegen, was bleibt offen und welches Material würdest du zusätzlich prüfen?','Der Ausschnitt zeigt leere Sessel an diesem Ort und Zeitpunkt. Er belegt nicht, dass niemand die gesamte Bibliothek nutzt. Prüfe das ganze Bild, weitere Orte/Zeiten und eine passende Quelle.'],
 source:['Die Schülervertretung schlägt einen Lesetag vor. Die Schulleitung bestätigt später einen Bücherflohmarkt. Ein Chat nennt den Lesetag bereits beschlossen. Welches Urteil passt? Erkläre Beleg und Wissensgrenze.','Der Vorschlag belegt den Wunsch, keinen Beschluss. Die spätere Mitteilung bestätigt den Flohmarkt. Ein Beschluss zum Lesetag ist damit nicht belegt; kläre, ob dazu noch eine andere Entscheidung vorliegt.']
 };
 const c=cases[unit.family];
 return page('Später wieder aufgreifen','<div class="lw-readable"><p class="lw-eyebrow">'+e(unit.topic)+' · Wiederaufnahme</p><h1>Was kannst du noch erklären?</h1><p class="lw-lead">Greife den Gedanken in einer späteren Stunde wieder auf. Erkläre zuerst selbst, bevor du eine frühere Lösung öffnest.</p><p>'+e(c[0])+'</p><label for="lw-retrieval">Deine Erklärung</label><textarea id="lw-retrieval" maxlength="10000"></textarea><details><summary>Jetzt mit einer möglichen Erklärung vergleichen</summary><p>'+e(c[1])+'</p><p>Welche Stelle hast du richtig rekonstruiert? Ergänze oder verbessere deine Erklärung.</p></details><p>Die eigene Erklärung wird nicht automatisch bewertet. Du kannst auch mündlich oder im Heft antworten.</p><a class="lw-button" href="index.html">Zur Lerneinheit</a></div>',units,unit,'wiederaufnahme.html');
}
function decorate(html,units,unit,file){
 html=terminology(html).replace(/href="\.\.\/(selbstlernen|lernwerkstatt|lernfassung-3|reinigungsfall-v2|reinigungsfall\.html)/g,'href="../../$1');
 const old=html.match(/<header class="lw-header">[\s\S]*?<\/header>/)||html.match(/<header class="topbar">[\s\S]*?<\/header>/);
 if(!old)throw new Error('Fehlender gemeinsamer Kopf: '+unit.area+'/'+file);
 const tools=unit.area==='lernstudio'?'':(old[0].match(/<button\b[\s\S]*?<\/button>/g)||[]).filter(x=>!x.includes('data-action="settings"')).join('');
 html=html.replace(old[0],header(units,unit,file,'../')+(tools?'<div class="lw-toolstrip">'+tools+'</div>':'')+storageStatus());
 html=html.replace(/<body([^>]*)>/,(_,attrs)=>'<body'+attrs.replace(/class="([^"]*)"/,(_,c)=>'class="'+c+' lw-mantel"')+(!attrs.includes('class=')?' class="lw-mantel"':'')+' data-lw-area="'+unit.area+'" data-lw-page="'+file+'">');
 if(unit.area==='lernstudio')html=html.replace('</head>','<link rel="stylesheet" href="../algorithmus.css"></head>');
 html=html.replace('</head>','<link rel="stylesheet" href="../mantel.css"><link rel="stylesheet" href="../learning-ui.css"><link rel="manifest" href="../manifest.webmanifest"><meta name="theme-color" content="#24543e">'+sharedScripts('../')+'<script type="application/json" id="lw-catalog">'+JSON.stringify(units).replaceAll('<','\\u003c')+'</script></head>');
 html=html.replace(/Wissen nachlesen ↗/g,'Wissen nachlesen').replace(/\bStationen\b/g,'Schritte');
 html=html.replace(/target="_blank"\s*rel="noopener"/g,'');
 const seriesLink=unit.area==='medienanalyse'?'<p class="lw-unit-support"><a href="../medienwirkung/index.html">Diese Bildwerkstatt gehört zur Reihe Medienwirkungen →</a></p>':'';
 const extra=seriesLink+(file!=='index.html'?'<p class="lw-unit-support"><a href="index.html" data-lw-return>Zurück zu deiner Aufgabe</a></p>':'')+printControls(file)+'<aside class="lw-unit-support"><a href="'+(unit.area==='medienanalyse'?'../medienwirkung/schritt-erinnern.html':'wiederaufnahme.html')+'">Später wieder aufgreifen</a> · <a href="../arbeit.html">Deine Arbeit sichern oder weiterführen</a>'+ (file==='lehrkraft.html'?teacherPreparation():'')+'</aside>';
 return html.replace('</body>',extra+foot('../')+'</body>');
}
function augment(assets){
 const A=require('./class5-content.cjs'),packs=A.load(),units=orderUnits([...catalog(assets),...packs.map(A.unit)]),created=new Map();
 if(new Set(units.map(u=>u.area)).size!==units.length||new Set(units.map(u=>u.id)).size!==units.length)throw new Error('Doppelter Inhalt im Klasse-5-Katalog');
 const keep=new Set(units.map(u=>u.area));
 for(const [name,value]of assets){const area=name.split('/')[0];if(keep.has(area))created.set(name,typeof value==='string'&&name.endsWith('.js')?terminology(value).replace(/\bStationen\b/g,'Schritte').replace(/href="\.\.\/(selbstlernen|lernwerkstatt|lernfassung-3|reinigungsfall-v2)/g,'href="../../$1'):value);}
 for(const n of ['lernwerkstatt/workshop-model.js','selbstlernen/model.js','selbstlernen/cleaning-core.js','prototype-navigation.css'])created.set(n,assets.get(n));
 for(const unit of units.filter(u=>u.family!=='content')){
  for(const [name,source]of [...created])if(name.startsWith(unit.area+'/')&&name.endsWith('.html'))created.set(name,decorate(source,units,unit,name.split('/').pop()));
  if(unit.area==='lernstudio'){
   const algorithm=require('./algorithmus-pages.cjs');
   created.set(unit.area+'/wissen.html',decorate(algorithm.knowledge(),units,unit,'wissen.html'));
   created.set(unit.area+'/material.html',decorate(algorithm.materials(),units,unit,'material.html'));
   for(const step of unit.steps.filter(s=>s.id!=='wiederaufnahme'))created.set(unit.area+'/baustein-'+step.id+'.html',decorate(algorithm.material(step.id),units,unit,'baustein-'+step.id+'.html'));
  }
  if(['medienanalyse','quellenquest'].includes(unit.area)){
   if(unit.area==='quellenquest')created.set(unit.area+'/index.html',decorate(require('../m02-quellenquest/render.cjs').index({mantel:true}),units,unit,'index.html'));
   created.set(unit.area+'/wissen.html',decorate(learningPages.knowledge(unit.area),units,unit,'wissen.html'));
   created.set(unit.area+'/material.html',decorate(learningPages.materials(unit.area),units,unit,'material.html'));
   for(const step of unit.steps.filter(s=>s.id!=='wiederaufnahme'))created.set(unit.area+'/baustein-'+step.id+'.html',decorate(learningPages.material(unit.area,step.id),units,unit,'baustein-'+step.id+'.html'));
  }
  created.set(unit.area+'/wiederaufnahme.html',retrieval(unit,units));
 }
 for(const pack of packs){
  if(pack.authorVersion===2){
   const u=units.find(x=>x.id===pack.id);
   for(const [file,body] of require('./class5-author-render.cjs').render(pack))created.set(u.area+'/'+file,page(pack.title,body,units,u,file));
   for(const [file,data] of A.assets(pack))created.set(u.area+'/'+file,data);
   continue;
  }
  const u=units.find(x=>x.id===pack.id),steps='<nav class="lw-actions" aria-label="Alle Schritte">'+pack.steps.map(s=>'<a href="schritt-'+s.id+'.html">'+e(s.title)+'</a>').join('')+'</nav>';
  const welcome='<p class="lw-eyebrow">'+e(u.topic)+'</p><h1>'+e(u.title)+'</h1><p class="lw-lead">'+e(u.description)+'</p><p><b>Du erarbeitest:</b> '+e(u.product)+'</p><p><b>Das brauchst du:</b> '+e(u.prerequisites.join(' · ')||'Kein besonderes Vorwissen.')+'</p>';
  created.set(u.area+'/index.html',page(u.title,welcome+steps+'<a class="lw-button" href="schritt-'+u.steps[0].id+'.html">Beginnen</a>',units,u));
  for(const step of pack.steps){
   created.set(u.area+'/schritt-'+step.id+'.html',page(step.title,steps+'<p class="lw-eyebrow">'+e(u.title)+'</p><h1>'+e(step.title)+'</h1><p><b>Du lernst:</b> '+e(step.goal)+'</p>'+A.renderBlocks(step)+'<section><h2>So prüfst du dein Ergebnis</h2><ul>'+step.criteria.map(c=>'<li>'+e(c)+'</li>').join('')+'</ul></section>',units,u,'schritt-'+step.id+'.html'));
   const material=A.renderBlocks({...step,blocks:step.blocks.filter(b=>b.type!=='private')}).replace(/<textarea[^>]*><\/textarea>/g,'<div class="lw-answer-space">________________________________<br>________________________________<br>________________________________</div>');
   created.set(u.area+'/baustein-'+step.id+'.html',page('Material: '+step.title,'<h1>'+e(step.title)+'</h1>'+material,units,u,'baustein-'+step.id+'.html'));
  }
  const materialLinks=pack.steps.map(s=>'<li><a href="baustein-'+s.id+'.html">'+e(s.title)+'</a></li>').join('');
  for(const file of ['wissen.html','material.html'])created.set(u.area+'/'+file,page(file==='wissen.html'?'Wissen':'Unterrichtsmaterial',welcome+'<ul>'+materialLinks+'</ul>',units,u,file));
  created.set(u.area+'/lehrkraft.html',page('Hinweise für Lehrpersonen',welcome+pack.teacher.map(p=>'<p>'+e(p)+'</p>').join('')+teacherPreparation()+steps,units,u,'lehrkraft.html'));
 }
 const intro='<section class="lw-hero"><p class="lw-eyebrow">Informatik und Medienbildung · Klasse 5</p><h1>Entdecken, prüfen,<br>selbst gestalten.</h1><p class="lw-lead">Lerne dein Gerät kennen, ordne Dateien und finde gute Informationen. Danach untersuchst du Bilder und entwickelst eigene Abläufe. Wähle dein Thema.</p></section>';
 created.set('index.html',page('Klasse 5',intro+cards(units,'index.html')+'<section class="lw-notice"><h2>Dein Weg durch das Lernwerk</h2><p>Die Themen sind in einer empfohlenen Lernfolge angeordnet. Du kannst jedes Angebot auch direkt öffnen. „Quellen prüfen“ gehört zur Recherche; die Bildwerkstatt gehört zu Medienwirkungen. Beide Werkstätten sind zusätzlich einzeln erreichbar. Erklärungen und Beispiele findest du bei deiner Aufgabe und im Wissen. Hilfen kannst du jederzeit nutzen. Deine eigenen Ergebnisse kannst du unter „Deine Arbeit“ weiterführen und sichern.</p><a href="lehrkraft.html">Mit dem Lernwerk unterrichten</a></section>',units));
 for(const [file,title,target]of [['wissen.html','Wissen und Beispiele','wissen.html'],['material.html','Unterrichtsmaterial','material.html']]){
 const text='<p class="lw-lead">Wähle einen Bereich. Die Bausteine sind auch ohne einen vorherigen Arbeitsstand nutzbar.</p>';
 created.set(file,page(title,'<p class="lw-eyebrow">Klasse 5</p><h1>'+title+'</h1>'+text+cards(units,target),units,null,file));
 }
 created.set('lehrkraft.html',page('Für Lehrpersonen',teacherPages.overview(units),units,null,'lehrkraft.html'));
 created.set('stoffverteilung.html',page('Stoffverteilung Klasse 5',teacherPages.distribution(),units,null,'stoffverteilung.html'));
 for(const s of teacherPages.allSeries())created.set(s.file,page('Reihe '+s.label,teacherPages.series(s.moduleId),units,null,s.file));
 created.set('arbeit.html',page('Deine Arbeit','<p class="lw-eyebrow">Arbeitsstände · auf diesem Browser</p><h1>Hier kannst du weiterarbeiten.</h1><p class="lw-lead">Sichere ein Ergebnis oder kehre zu einer Aufgabe zurück. „Begonnen“ beschreibt deine Arbeit; es ist keine Bewertung deines Könnens.</p><p id="lw-work-message" role="status"></p><div id="lw-work-list"></div><noscript><p>Die Verwaltung eigener Arbeit benötigt JavaScript. Wissen und Unterrichtsmaterial sind ohne JavaScript lesbar.</p></noscript><section class="lw-notice"><h2>Was wird hier gesichert?</h2><p>Hier sicherst du deine Antworten und Werkzeugstände im Lernwerk. Deine echten Übungsdateien liegen gesondert in „Dateien“ oder im Datei-Explorer. Eine Lernwerk-Arbeitsdatei enthält diese Dateien nicht.</p><p>Für den Gerätewechsel: Sichere deine Lernwerk-Antworten als Arbeitsdatei. Nimm echte Übungsdateien über den mit der Schule vereinbarten Weg gesondert mit.</p><h3>Antworten und Werkzeugstände speichern</h3><label><input id="lw-persist" type="checkbox">Meine Lernwerk-Antworten und Werkzeugstände auf diesem Gerät speichern</label><p>Ohne diese Wahl bleiben Antworten und Werkzeugstände in diesem Browsertab. Andere Personen im selben Browserprofil können Gerätekopien öffnen. Ausschalten beendet neue Schreibvorgänge; eine ältere Kopie bleibt, bis du sie ausdrücklich löschst.</p><div class="lw-actions"><label class="lw-button secondary" for="lw-file">Arbeitsdatei öffnen</label><input class="no-print" id="lw-file" type="file" accept=".json,application/json"><button id="lw-delete-device" class="lw-button secondary">Gerätekopie löschen</button><button id="lw-delete-all" class="lw-button secondary">Alle eigenen Lernwerkstände löschen</button></div></section><section><h2>Offline arbeiten</h2><p>Bereite den Mantel und seine Materialien bei vorhandener Internetverbindung vor. Reale Internetrecherche bleibt eine Onlinehandlung.</p><button id="lw-offline" class="lw-button secondary">Offlinepaket vorbereiten</button><button id="lw-update" class="lw-button secondary" hidden>Neue Fassung übernehmen</button><button id="lw-install" class="lw-button secondary" hidden>Lernwerk installieren</button><p id="lw-offline-message" role="status">Offlineverfügbarkeit noch nicht geprüft.</p></section><dialog id="lw-import-dialog" aria-labelledby="lw-import-title"><h2 id="lw-import-title">Arbeitsdatei prüfen</h2><div id="lw-import-preview"></div><label><input name="lw-import-mode" type="radio" value="separate" checked>Als eigenen neuen Stand übernehmen</label><label><input name="lw-import-mode" type="radio" value="replace">Einen vorhandenen Stand ausdrücklich ersetzen</label><select id="lw-replace-target" aria-label="Zu ersetzender Stand"></select><div class="lw-actions"><button id="lw-import-confirm" class="lw-button">Übernehmen</button><button id="lw-import-cancel" class="lw-button secondary">Abbrechen</button></div></dialog>',units,null,'arbeit.html'));
 created.set('informationen.html',page('Informationen zum Lernwerk','<div class="lw-readable"><p class="lw-eyebrow">Bedienung · Herkunft · Grenzen</p><h1>Gut zu wissen.</h1><h2>Arbeiten und sichern</h2><p>„Deine Arbeit“ sammelt tatsächliche eigene Antworten und Werkzeugstände. Im selben Tab bleiben sie beim Wechsel der Lernwerksseiten erhalten. Schließen, Browserbereinigung oder Einschränkungen können sie entfernen. Für Gerätewechsel lade eine Lernwerk-Arbeitsdatei herunter und öffne sie im anderen Browser. Sie enthält Antworten und Werkzeugstände; echte Übungsdateien aus „Dateien“ oder dem Datei-Explorer nimmt sie nicht mit. Ein angebotenes Download belegt nicht, dass eine Datei außerhalb des Browsers gesichert ist.</p><h2>Aufgaben und Rückmeldung</h2><p>Geschlossene Prüfungen beziehen sich auf eine konkrete Auswahl. Eigene Erklärungen werden nicht automatisch bewertet. Vergleiche mit den Kriterien und überarbeite dein Produkt. Hilfen sind jederzeit erreichbar.</p><h2>Quellen und Rechte</h2><p>Eigene Lerninhalte: CC BY-SA 4.0. Eigener Code: MIT. Herkunft und gesonderte Rechte von Medien stehen bei den Materialien. Schulische Quellenfälle sind erfunden; die Bildmaterialien sind als KI-Illustrationen ausgewiesen. Unterrichtsplanung auf Grundlage der IuM-Anhörungsfassung vom 21.09.2026.</p><p>Diese Fassung ist zur Sichtung und Erprobung bestimmt. Sie behauptet keine gemessene Lernwirkung und keine abgeschlossene Prüfung aller Schulgeräte. Das Lernwerk verwendet keine Konten oder zentrale Lernanalyse.</p><p><a href="lehrkraft.html">Hinweise zur schulischen Vorbereitung</a></p></div>',units,null,'informationen.html'));
 for(const name of ['mantel.css','algorithmus.css','learning-ui.css','learning-ui.js','mantel-model.js','mantel-runtime.js'])created.set(name,fs.readFileSync(path.join(__dirname,name),'utf8'));
 const icon=path.join(__dirname,'../../apps/lernwerk-portal/public/icons');
 for(const size of [192,512])created.set('icon-'+size+'.png',fs.readFileSync(path.join(icon,'pwa-'+size+'x'+size+'.png')));
 created.set('manifest.webmanifest',JSON.stringify({name:'IuM Lernwerk – Klasse 5',short_name:'Lernwerk',lang:'de',start_url:'./',scope:'./',display:'standalone',background_color:'#f5f4ed',theme_color:'#24543e',icons:[192,512].map(size=>({src:'icon-'+size+'.png',sizes:size+'x'+size,type:'image/png'}))}));
 const version=crypto.createHash('sha256');for(const value of created.values())version.update(value);const hash=version.digest('hex').slice(0,12);
 const worker=fs.readFileSync(path.join(__dirname,'mantel-sw.js'),'utf8').replace('__VERSION__',hash).replace('__FILES__',JSON.stringify([...created.keys()]));
 created.set('mantel-sw.js',worker);
 for(const [name,value]of created)assets.set('klasse5/'+name,value);
 return assets;
}
module.exports={augment,page,decorate};
