(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.LernwerkWorkProjects = factory();
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  function createSession(options) {
    const M = options.model;
    let bridge = null, cardId = null, pending = false;
    const now = options.now || (() => new Date().toISOString());
    const card = () => options.getStore().cards.find(c => c.id === cardId && c.taskId === 'alg-5');
    function available() { if (!bridge || !bridge.ready) throw Error('Der Editor wird noch vorbereitet. Bitte warte kurz.'); if (!card()) throw Error('Die zugehörige ALG-5-Karte fehlt.'); }
    function project(xml, filename) { return {format:'snap-project',version:1,xml,filename,savedAt:now()}; }
    return {
      connect(value, id) { bridge = value; cardId = id; pending = false; },
      disconnect() { bridge = null; cardId = null; pending = false; },
      noteChange() { pending = true; },
      hasChanges() { return Boolean(bridge && (pending || bridge.isDirty())); },
      async openStored() {
        available(); const saved = card().project;
        if (!saved) throw Error('In dieser Karte ist noch kein Projektstand enthalten.');
        await bridge.openProject(saved.xml, {discardChanges:true}); pending = false;
        return saved;
      },
      async openFile(xml, filename) {
        available(); const checked = M.validateProject(project(xml, filename));
        if (!checked.ok) throw Error(checked.error);
        await bridge.openProject(xml, {discardChanges:true}); pending = true;
      },
      start() { available(); pending = true; },
      capture(filename) {
        try {
          available(); const snapshot = bridge.getSnapshot();
          const result = M.setProject(options.getStore(), cardId, project(snapshot.xml, filename), options.catalog);
          if (!result.ok) return result;
          const state = options.commit(result.store);
          const stored = state?.store?.cards.find(c => c.id === cardId)?.project;
          if (!stored || stored.xml !== snapshot.xml || stored.filename !== filename || stored.savedAt !== result.card.project.savedAt) {
            return {ok:false,error:'Der Projektstand konnte nicht übernommen werden. Dein Projekt bleibt im Editor geöffnet.'};
          }
          const marked = bridge.markSaved(snapshot.revision); pending = !marked;
          return {ok:true,card:result.card,volatile:Boolean(state.volatile),changedAgain:!marked};
        } catch (error) { return {ok:false,error:error.message}; }
      }
    };
  }
  function createUI(options) {
    const M = options.model, doc = options.document || document, win = options.window || window;
    const session = createSession(options);
    const date = value => new Date(value).toLocaleString('de-DE', {dateStyle:'medium',timeStyle:'short'});
    const el = (tag, text, attrs = {}) => {
      const node = doc.createElement(tag); if (text != null) node.textContent = text;
      Object.entries(attrs).forEach(([key,value]) => node.setAttribute(key,value)); return node;
    };
    const button = (text, action) => { const node = el('button',text,{type:'button'}); node.addEventListener('click',action); return node; };
    let dialog = null, frame = null, bridge = null, activeId = null, poll = null, busy = false, opened = false, status = null, recovery = null;
    function offerRecovery(error) {
      const copy=error?.recoverySnapshot || bridge?.recoverySnapshot;
      if(!copy)return; recovery=copy;
      if(!doc.getElementById('work-project-recovery')) {
        const rescue=button('Vorherigen Projektstand als Rettungskopie herunterladen',()=>{options.download(recovery.xml,'ALG-5_Rettungskopie.xml','application/xml;charset=utf-8');say('Rettungsdownload angeboten. Prüfe die Datei an deinem Ablageort, bevor du den Editor schließt.');});
        rescue.id='work-project-recovery';status.after(rescue);
      }
    }
    const find = id => options.getStore().cards.find(c => c.id === id);
    function say(text, error = false) { status.textContent = text; status.classList.toggle('work-error',error); status.setAttribute('role',error?'alert':'status'); }
    function hasChanges() { return Boolean(dialog && (busy || recovery || (opened && session.hasChanges()))); }
    function close() {
      if (busy) { say('Bitte warte, bis die Datei vollständig geöffnet ist.'); return; }
      if (hasChanges() && !win.confirm('Dieser Projektstand ist noch nicht in deine Übersicht übernommen. Schließen und diese Änderungen verwerfen?')) return;
      clearInterval(poll); session.disconnect(); bridge = null; opened = false;
      const id = activeId; dialog.close(); dialog.remove(); dialog = null; frame = null; activeId = null;
      doc.querySelector('[data-card-id="'+id+'"] h3')?.focus();
    }
    async function waitForEditor() {
      for (let i=0;i<600;i++) {
        if (!dialog) throw Error('Editor geschlossen.');
        const api = frame.contentWindow?.LernwerkProjectBridge;
        if (api?.ready) return api;
        await new Promise(resolve=>setTimeout(resolve,100));
      }
      throw Error('Der Editor konnte nicht geladen werden. Prüfe die Verbindung und öffne ihn erneut. Deine gespeicherte Projektkopie bleibt erhalten.');
    }
    async function open(id) {
      const card = find(id); if (!card || card.taskId !== 'alg-5' || dialog) return;
      activeId = id; opened = false; busy = true; recovery = null;
      dialog = el('dialog',null,{class:'work-project-dialog','aria-labelledby':'work-project-heading'});
      const top = el('div',null,{class:'work-project-top'});
      const heading = el('h2','ALG-5 · Dein eigenes Projekt',{id:'work-project-heading',tabindex:'-1'});
      top.append(heading,button('Zur Übersicht',close));
      const intro = el('p','Öffne deine eigene XML-Datei oder beginne mit dem Startprojekt. Übernimm deinen Stand nach dem Bearbeiten in die Übersicht. Lade die Übersicht anschließend zum Mitnehmen herunter.');
      status = el('p','Der Editor wird vorbereitet …',{id:'work-project-status',class:'work-context',role:'status','aria-live':'polite'});
      const stateText = el('p','',{id:'work-project-state',class:'work-project-state',role:'status','aria-live':'polite'});
      const choices = el('div',null,{class:'work-actions'});
      const input = el('input',null,{id:'work-project-file',type:'file',accept:'.xml,application/xml,text/xml'});
      const fileLabel = el('label','Eigene XML-Datei öffnen',{class:'work-file'}); fileLabel.append(input); input.disabled = true;
      const start = button('Mit Startprojekt beginnen',()=>{if(busy)return;session.start();opened=true;cover.hidden=true;frame.inert=false;start.hidden=true;take.disabled=false;say('Du siehst das Startprojekt für ALG-5. Baue deinen eigenen Rover. Übernimm deinen Stand anschließend in die Übersicht.');});
      start.disabled = true; start.hidden = Boolean(card.project);
      choices.append(fileLabel,start);
      const label = el('label',null,{class:'work-field'});
      const name = el('input',null,{id:'work-project-filename',type:'text',maxlength:'160'}); name.value = card.project?.filename || 'ALG-5_Mein-Rover.xml';
      label.append(el('span','Dateiname für deine Projektkopie (.xml)'),name);
      const actions = el('div',null,{class:'work-actions'});
      const take = button('Projektstand übernehmen',()=>{
        if (busy || !opened) return;
        const filename = name.value.trim(); const result = session.capture(filename);
        if (!result.ok) { say(result.error,true); return; }
        name.value = result.card.project.filename;
        const note = result.volatile ? 'Nur auf dieser geöffneten Seite verfügbar. Lade die Übersicht jetzt herunter, bevor du sie verlässt.' : 'Zum Mitnehmen oder vor dem Schließen lade die Übersicht herunter.';
        say('Projektstand übernommen: '+name.value+' · '+date(result.card.project.savedAt)+'. '+note+(result.changedAgain?' Im Editor gibt es bereits weitere Änderungen.':''),result.volatile);
        pack.disabled=false; refreshState();
      }); take.id='work-project-take'; take.className='work-primary'; take.disabled=true;
      const pack = button('Übersicht mit Projekt herunterladen',()=>{
        if(hasChanges()){say('Übernimm zuerst deinen aktuellen Projektstand. Danach enthält die Datei genau diesen Stand.',true);return;}
        if(options.exportOverview()===false){say('Die Übersicht konnte nicht heruntergeladen werden. Dein Projekt bleibt geöffnet. Prüfe den Speicherhinweis in der Übersicht und versuche den Download erneut.',true);return;}say('Download angeboten. Prüfe die Datei an deinem Ablageort. Zum Wiederöffnen: Deine Arbeit → Übersichtsdatei laden → Mein Projekt weiterbearbeiten.');
      }); pack.id='work-project-pack'; pack.disabled=!card.project;
      actions.append(take,pack);
      const help = el('p','„Projektstand übernehmen“ ersetzt die Projektkopie dieser Karte. Heftnotizen, Bilder und andere externe Dateien nimmst du weiterhin gesondert mit.',{class:'work-help'});
      frame = el('iframe',null,{class:'work-project-frame',title:'Snap-Editor für dein ALG-5-Projekt',src:'programmieren/snap/arbeit.html?aufgabe=alg-5'}); frame.inert=true;
      const editorWrap=el('div',null,{class:'work-project-editor'});
      const cover=el('div','Der Editor wird vorbereitet …',{class:'work-project-cover'});
      editorWrap.append(frame,cover);
      dialog.append(top,intro,status,choices,label,actions,stateText,help,editorWrap);
      dialog.addEventListener('cancel',event=>{event.preventDefault();close();});
      doc.body.append(dialog); dialog.showModal(); heading.focus();
      name.addEventListener('input',()=>{if(opened){session.noteChange();refreshState();}});
      function refreshState() {
        if(!dialog || !opened)return;
        const current=find(id)?.project;
        stateText.textContent=session.hasChanges()?'Im Editor gibt es einen Stand, der noch nicht in deiner Übersicht übernommen ist.':current?'In deiner Übersicht enthalten: '+current.filename+' · übernommen '+date(current.savedAt)+'.':'Noch kein Projektstand in deiner Übersicht.';
      }
      input.addEventListener('change',async()=>{
        const file=input.files[0];input.value='';if(!file || busy)return;
        if(opened&&session.hasChanges()&&!win.confirm('Den noch nicht übernommenen Editorstand durch die ausgewählte Datei ersetzen?'))return;
        if(file.size>M.MAX_PROJECT_BYTES){say('Diese Projektdatei ist größer als 10 MiB. Dein bisheriger Stand bleibt erhalten.',true);return;}
        busy=true;input.disabled=true;start.disabled=true;take.disabled=true;name.disabled=true;frame.inert=true;cover.hidden=false;cover.textContent='Deine Datei wird geöffnet …';
        try {
          const before=opened?bridge.getSnapshot():null;
          const text=await file.text();
          if(before && bridge.getSnapshot().xml!==before.xml && !win.confirm('Dein Projekt hat sich während des Dateilesens geändert. Diese neuen Änderungen verwerfen und die Datei öffnen?')){say('Öffnen abgebrochen. Dein aktueller Editorstand bleibt erhalten.');return;}
          await session.openFile(text,file.name);name.value=file.name;
          opened=true;cover.hidden=true;frame.inert=false;start.hidden=true;say('Eigene Datei geöffnet: '+file.name+'. Prüfe deinen Code und Testfall. Mit „Projektstand übernehmen“ kommt dieser Stand in deine Übersicht.');
        }catch(error){say(error.message,true);offerRecovery(error);}finally{busy=false;input.disabled=!bridge?.ready;start.disabled=!bridge?.ready;take.disabled=!opened||!bridge?.ready;name.disabled=false;frame.inert=!(opened&&bridge?.ready);cover.hidden=opened&&Boolean(bridge?.ready);if(!cover.hidden)cover.textContent=bridge?.ready?'Wähle deine eigene XML-Datei oder beginne mit dem Startprojekt.':'Die Editoransicht konnte nicht wiederhergestellt werden. Sichere die angebotene Rettungskopie.';refreshState();}
      });
      try {
        bridge=await waitForEditor();session.connect(bridge,id);
        if(card.project){await session.openStored();opened=true;cover.hidden=true;frame.inert=false;take.disabled=false;say('Dein gespeicherter Projektstand ist geöffnet: '+card.project.filename+'. Prüfe deinen Testfall und arbeite weiter.');}
        else {say('Wähle deine eigene XML-Datei. Wenn du neu beginnst, wähle „Mit Startprojekt beginnen“.');cover.textContent='Wähle deine eigene XML-Datei oder beginne mit dem Startprojekt.';}
        input.disabled=false;start.disabled=false;poll=setInterval(refreshState,700);refreshState();
      }catch(error){say(error.message,true);offerRecovery(error);input.disabled=!bridge?.ready;}
      finally{busy=false;}
    }
    function decorateCard(card,article,actions) {
      if(card.taskId!=='alg-5')return;
      const saved=card.project;
      const meta=el('p',saved?'Projektkopie enthalten: '+saved.filename+' · übernommen '+date(saved.savedAt)+'.':'Hier kannst du dein eigenes Snap-Projekt zusammen mit der Übersicht sichern.',{class:'work-project-meta'});
      article.append(meta);
      actions.append(button(saved?'Mein Projekt weiterbearbeiten':'Snap-Projekt hinzufügen',()=>open(card.id)));
      if(saved){
        actions.append(button('Projektdatei herunterladen',()=>options.download(saved.xml,saved.filename,'application/xml;charset=utf-8')));
        actions.append(button('Projektkopie entfernen',()=>{
          if(!win.confirm('Die enthaltene Projektkopie aus dieser Karte entfernen? Lade sie vorher herunter, wenn du sie behalten möchtest.'))return;
          const result=M.removeProject(options.getStore(),card.id,options.catalog,new Date().toISOString());
          if(!result.ok){options.feedback(result.error,true);return;}
          options.commit(result.store);options.feedback('Projektkopie aus der Karte entfernt. Deine bereits heruntergeladenen Dateien bleiben erhalten.');
        }));
      }
    }
    return {decorateCard,hasChanges,open};
  }
  return {createSession,createUI};
}));
