'use strict';
// Additional derived ALG-5 host; preserved Snap sources and engine remain byte-identical.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const ROOT='klasse7/programmieren/snap/';
const sha=value=>crypto.createHash('sha256').update(value).digest('hex');
function once(text,marker,replacement){if(text.split(marker).length!==2)throw Error('Erwarteter Snap-Quellmarker fehlt oder ist mehrfach vorhanden: '+marker);return text.replace(marker,replacement);}
function addSnapProjectEditor(source){
 const pages=new Map(source);
 for(const file of ['arbeit.html','arbeit-editor.js','arbeit-bridge.js','arbeit-herkunft.json'])if(pages.has(ROOT+file))throw Error('ALG-5-Editorziel bereits vorhanden: '+file);
 const originalHTML=source.get(ROOT+'lernwerk.html'),originalJS=source.get(ROOT+'lernwerk-editor.js');
 if(typeof originalHTML!=='string'||typeof originalJS!=='string')throw Error('Gebundene Lernwerk-Editorquellen fehlen.');
 let html=once(originalHTML,'<script src="lernwerk-editor.js?v=20261025-2" defer></script>','<script src="arbeit-bridge.js" defer></script><script src="arbeit-editor.js" defer></script>');
 html=once(html,'<title>Programmieren · Klasse 7 · Lernwerk</title>','<title>Mein ALG-5-Projekt · Klasse 7 · Lernwerk</title>');
 // The parent supplies navigation; prevent a second grade-menu transformation of this frame.
 const brand=html.match(/<a class="(lw-shell-brand|brand)"/g);
 if(!brand||brand.length!==1)throw Error('Erwarteter Snap-Kopfmarker fehlt oder ist mehrfach vorhanden.');
 html=html.replace(/<a class="(lw-shell-brand|brand)"/,'<a class="$1 snap-project-brand"');
 // Leaving a link in the frame must never discard its open project.
 html=html.replace(/<a\b([^>]*?)>/g,(whole,attrs)=>{
  const href=attrs.match(/\bhref="([^"]*)"/);if(!href||href[1].startsWith('#'))return whole;
  return '<a'+attrs.replace(/\s(?:target|rel)="[^"]*"/g,'')+' target="_blank" rel="noopener">';
 });
 // Runs inside the existing closure and reuses its original-visibility serialization.
 const hook=`    window.LernwerkProjectBridge = window.LernwerkProjectBridgeFactory({
        ready: () => ready,
        scene: () => ide.scene,
        revision: () => ide.version,
        name: () => ide.getProjectName(),
        xml: projectXML,
        dirty: () => ide.hasUnsavedEdits(),
        stop: () => { ide.stop(); updateState(); },
        markSaved: () => ide.recordSavedChanges(),
        markDirty: () => ide.recordUnsavedChanges(),
        cancelLoad: () => { ide.onNextStep = null; },
        openXML: (text, done) => { ide.stop(); ide.openProjectString(text, done); },
        afterOpen: () => { Process.prototype.enableJS = false; setStepping(false); applyView(); updateState(); }
    });
`;
 let script=originalJS.replace(/\r\n/g,'\n');
 script=once(script,'const task = model.resolveTask(location.search, location.hash);',"const task = model.resolveTask('?aufgabe=alg-5', '');");
 script=once(script,"    window.addEventListener('load', boot, {once: true});",hook+"    window.addEventListener('load', boot, {once: true});");
 script=once(script,'if (ready && ide.hasUnsavedEdits()) {','if (window.parent === window && ready && (window.LernwerkProjectBridge ? window.LernwerkProjectBridge.isDirty() : ide.hasUnsavedEdits())) {');
 script=once(script,"if (ide.hasUnsavedEdits() && !confirm(","if (window.LernwerkProjectBridge.isDirty() && !confirm(");
 const nativeOpen=`            const previousScene = ide.scene;
            ide.stopAllScripts();
            ide.openProjectString(text, () => {
                if (ide.scene === previousScene) { notice('Die Datei konnte nicht geöffnet werden. Prüfe, ob sie aus Snap! stammt.'); return; }
                setStepping(false);
                applyView();
                updateState();
                notice('Datei geöffnet: ' + file.name + '. Prüfe jetzt deinen Testfall erneut.');
            });`;
 script=once(script,nativeOpen,`            await window.LernwerkProjectBridge.openProject(text, {discardChanges: true});
            ide.recordUnsavedChanges();
            ide.stop();
            notice('Datei geöffnet: ' + file.name + '. Prüfe deinen Testfall und übernimm den Stand anschließend in deine Arbeitskarte.');`);
 const bridge=fs.readFileSync(path.join(__dirname,'snap-projekt-bridge.js'),'utf8');
 pages.set(ROOT+'arbeit.html',html);pages.set(ROOT+'arbeit-editor.js',script);pages.set(ROOT+'arbeit-bridge.js',bridge);
 const manifest={version:1,taskId:'alg-5',license:'AGPL-3.0-or-later',scope:'Zusätzliche abgeleitete Hülle für bewusst gesicherte ALG-5-Projektstände; ursprüngliche Engine und Lernwerk-Ansicht unverändert.',sources:{'lernwerk.html':sha(originalHTML),'lernwerk-editor.js':sha(originalJS)},derivation:'prototypes/klasse7-jahrgang/snap-projekt-adapter.cjs und snap-projekt-bridge.js',files:{'arbeit.html':sha(html),'arbeit-editor.js':sha(script),'arbeit-bridge.js':sha(bridge)}};
 pages.set(ROOT+'arbeit-herkunft.json',JSON.stringify(manifest,null,2)+'\n');return pages;
}
module.exports={addSnapProjectEditor};

