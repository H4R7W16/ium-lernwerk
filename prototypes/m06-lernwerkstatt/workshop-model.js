'use strict';
(function(root){
 const M=typeof module!=='undefined'&&module.exports?require('../m06-selbstlernen/model.js'):root.Lesson;
 const lessons=[
 {id:'start',group:'Entdecken',title:'Wo kommt der Roboter an?',short:'Fahren & drehen',room:{width:3,height:2,start:[1,2,1]},code:'vor\nlinks\nvor',predict:true,
 goal:'Unterscheide Standort und Blickrichtung.',
 task:'Nach dem Basteln liegen Krümel auf dem Boden. Der Roboter folgt genau deinem Programm. Tippe zuerst auf seine vermutete Endkachel und wähle die Blickrichtung.',
 question:'Was hat die Drehung verändert – und was blieb gleich?',
 hints:['Schau aus Sicht des Roboters: Sein Pfeil zeigt zuerst nach rechts.','Nach vor steht er in der Mitte unten. links dreht ihn dort nach oben.'],
 solution:'Er endet in Spalte 2, Reihe 1 und blickt nach oben. Nur vor verändert den Ort. links verändert den Blick um eine Vierteldrehung; dabei bleibt er auf derselben Kachel.',
 explain:'<h3>Drei Befehle, zwei verschiedene Wirkungen</h3><p><b>vor</b> fährt eine Kachel in Blickrichtung. <b>links</b> und <b>rechts</b> drehen den Roboter um eine Vierteldrehung auf seiner Kachel. Links ist also nicht automatisch die linke Seite deines Bildschirms.</p><p>Denke dich hinter seinen Pfeil. Blickt er nach rechts, zeigt sein Pfeil nach einer Linksdrehung nach oben. Erst das nächste vor bewegt ihn dorthin. Beim Prüfen brauchst du deshalb immer beides: <b>Wo steht er? Wohin blickt er?</b></p><p>Das ist ein Modell: Die Startkachel gilt schon als sauber. Eine besuchte Kachel wird sauber; Drehen erreicht keine neue. Der Roboter erkennt keine Hindernisse. Ein Versuch über den Rand hält das Programm an.</p>'},
 {id:'loop',group:'Verstehen',title:'Eine Klammer. Vier ganze Runden.',short:'Der Schleifenkörper',room:{width:2,height:2,start:[1,2,1]},code:'wiederhole 4 [vor; links]',sequence:['vor','links','vor','links'],
 goal:'Erkenne, was in jedem Durchlauf zusammengehört.',
 task:'Untersuche erst einen Durchlauf, dann den nächsten. Beobachte, wann die Markierung zur ersten Anweisung zurückspringt.',
 question:'Schreibe die ersten zwei Durchläufe mit den Bausteinen aus. Wie viele Aktionen braucht die ganze Schleife?',
 hints:['Ein Durchlauf ist erst beendet, wenn alles in der Klammer dran war.','Die Reihenfolge ist vor → links | vor → links. Vier solcher Paare haben acht Aktionen.'],
 solution:'Zwei Durchläufe: vor → links → vor → links. Insgesamt sind es 4 × 2 = 8 Aktionen. Der Roboter erreicht alle vier Kacheln und endet links unten mit Blick nach rechts.',
 explain:'<h3>Die ganze Gruppe wiederholen</h3><p>Eine <b>Schleife</b> wiederholt Anweisungen. Die Zahl 4 bedeutet insgesamt viermal, nicht einmal plus viermal. Alles zwischen den Klammern gehört zum <b>Wiederholungskörper</b>. Das Semikolon trennt seine Anweisungen.</p><p>Ein <b>Durchlauf</b> führt den ganzen Körper einmal in seiner Reihenfolge aus: erst vor, dann links. Nach vor ist dieser Durchlauf noch nicht fertig. Erst nach links beginnt der nächste.</p><p>Vier Durchläufe mit je zwei Anweisungen ergeben acht Aktionen. Die Schleife spart Schreibarbeit, <b>verkürzt aber nicht die Fahrt</b>. Mit „Ein Durchlauf“ kannst du genau bis zum Ende der aktuellen Klammergruppe fahren.</p>'},
 {id:'after',group:'Verstehen',title:'Und nach der Schleife?',short:'Danach geht es weiter',room:{width:2,height:2,start:[1,2,1]},code:'wiederhole 4 [vor; links]\nvor',predict:true,
 goal:'Trenne den Schleifenkörper von der folgenden Anweisung.',
 task:'Eine Anweisung steht unter der Schleife. Geh den Weg im Kopf durch und markiere das Ende des ganzen Programms. Prüfe dann, wann die zweite Zeile ausgeführt wird.',
 question:'Warum wird das letzte vor nur einmal ausgeführt?',
 hints:['Achte auf die schließende Klammer. Die zweite Zeile steht dahinter.','Die Schleife endet nach acht Aktionen links unten. Jetzt folgt noch ein vor.'],
 solution:'Die Fahrt endet rechts unten, Blick rechts. Die zweite Zeile kommt erst nach allen vier Durchläufen genau einmal dran. Das ganze Programm hat neun Aktionen.',
 explain:'<h3>Die Klammer legt den Umfang fest</h3><p>Nur die Anweisungen <b>in der Klammer</b> werden wiederholt. Eine Anweisung danach gehört nicht zur Schleife. Sie wird erst ausgeführt, wenn alle Durchläufe beendet sind.</p><p>Hier: viermal vor → links, <b>danach einmal vor</b>. Die Schleife hat acht Aktionen, das ganze Programm neun. Die zuletzt besuchte Kachel war bereits sauber; eine weitere Fahrt muss also nicht die Zahl sauberer Kacheln erhöhen.</p><p>Kontrolliere drei Dinge getrennt: Ist die Schleife zu Ende? Gibt es danach noch Code? Ist der ganze Boden sauber? Diese Fragen haben nicht automatisch dieselbe Antwort.</p>'},
 {id:'repair',group:'Verstehen',title:'Die Drehung steht am falschen Platz.',short:'Einen Fehler finden',room:{width:2,height:2,start:[1,2,1]},code:'wiederhole 4 [vor]\nlinks',editable:true,
 goal:'Repariere den Wiederholungskörper gezielt.',
 task:'Dieser Plan soll eine Runde fahren. Untersuche, wo er stoppt. Ändere dann die Bausteine: In jedem Durchlauf soll er fahren und sich drehen.',
 question:'Warum hilft es nicht, nur die Zahl 4 zu ändern?',
 hints:['Der Roboter fährt geradeaus, solange die Drehung außerhalb der Klammer steht.','Bearbeite die Schleife: Körper vor → links. Entferne danach die einzelne Drehung, wenn er wie am Start blicken soll.'],
 solution:'wiederhole 4 [vor; links] fährt die Runde und endet mit der ursprünglichen Blickrichtung. Beim fehlerhaften Programm würde schon das zweite vor über den Rand führen; links wird deshalb gar nicht mehr erreicht.',
 explain:'<h3>Den Fehler am Ablauf finden</h3><p>Viermal vor bedeutet vier Fahrten geradeaus. Es bedeutet nicht: vier Kacheln nacheinander entlang eines Quadrats besuchen. Erst eine Drehung ändert die nächste Fahrtrichtung.</p><p>Beim ursprünglichen Plan steht links <b>hinter</b> der Schleife. Ein Wandstopp bricht aber das Programm ab, bevor diese Drehung drankommt. Gehe zum letzten sicheren Zustand zurück und prüfe den Pfeil.</p><p>Ein guter Reparaturversuch ändert die Ursache: Die Drehung muss in den Körper. Vergleiche danach Standort <b>und</b> Blickrichtung mit dem Auftrag.</p>'},
 {id:'example',group:'Planen',title:'Erst eine Reihe. Dann die nächste.',short:'Einen Musterweg verstehen',room:{width:3,height:2,start:[1,2,1]},code:'wiederhole 2 [vor]\nlinks\nvor\nlinks\nwiederhole 2 [vor]',
 goal:'Untersuche, wie Teilpläne zu einem ganzen Weg werden.',
 task:'Dieser Musterweg reinigt zwei Reihen. Prüfe zuerst die untere Reihe, dann den Übergang und zuletzt die obere Reihe. Beobachte den Blick an den Übergängen.',
 question:'Welche drei Teilpläne erkennst du? Erkläre, warum der mittlere Teil zwei Drehungen braucht.',
 hints:['Der erste und der letzte Teil sind gerade Fahrten. Dazwischen muss der Roboter die Reihe wechseln.','Die erste Drehung zeigt nach oben. Nach vor steht er in der oberen Reihe. Die zweite Drehung zeigt nach links, entlang dieser Reihe.'],
 solution:'Untere Reihe: zweimal vor. Übergang: links → vor → links. Obere Reihe: zweimal vor. Sieben Aktionen erreichen sechs Kacheln. Ende links oben, Blick links.',
 explain:'<h3>Einen vollständigen Beispielweg verstehen</h3><p>Die Fläche hat drei Spalten und zwei Reihen. Starte links unten mit Blick nach rechts. <b>wiederhole 2 [vor]</b> erreicht die beiden anderen Kacheln der unteren Reihe. Drei Kacheln brauchen nur zwei Fahrten: Die Startkachel zählt schon mit.</p><p>Am rechten Rand kommt der Übergang. <b>links</b> richtet den Roboter nach oben, <b>vor</b> fährt in die obere Reihe, <b>links</b> richtet ihn nach links aus. Die beiden Drehungen ändern nur den Blick, die Fahrt dazwischen nur den Ort.</p><p>Jetzt passt die gerade Fahrt erneut: <b>wiederhole 2 [vor]</b> erreicht die restlichen oberen Kacheln. Der ganze Weg hat sieben Aktionen, obwohl die Fläche sechs Kacheln hat. Aktionen und neue Kacheln sind verschiedene Größen.</p><p>Im nächsten Auftrag ist jede Reihe eine Kachel länger. Übernimm das Prinzip und entscheide selbst, welche Zahlen sich ändern müssen.</p>'},
 {id:'rows',group:'Planen',title:'Vier Kacheln. Wie viele Fahrten?',short:'Zwei Reihen verbinden',room:{width:4,height:2,start:[1,2,1]},code:'wiederhole 2 [vor]\nlinks\nvor\nlinks\nwiederhole 2 [vor]',editable:true,
 goal:'Verbinde Teilpläne zu einem vollständigen Weg.',
 task:'Das Gerüst ist vorbereitet. Ergänze die Schleifenzahlen, sodass beide Reihen sauber werden. Tippe einen Baustein an, um ihn zu ändern.',
 question:'Warum passt deine Schleifenzahl zu einer Reihe mit vier Kacheln?',
 hints:['Die Startkachel ist schon erreicht. Zähle die Wege zwischen den Kacheln.','Vier Kacheln haben drei Zwischenräume. Am rechten Rand verbindet links → vor → links die beiden Reihen.'],
 solution:'wiederhole 3 [vor] → links → vor → links → wiederhole 3 [vor]. Der Plan erreicht acht Kacheln mit neun Aktionen und endet links oben, Blick links.',
 explain:'<h3>Erst Teilprobleme lösen</h3><p>Teile die Fläche in Reihen. Für jede Reihe brauchst du eine gerade Fahrt, dazwischen einen Übergang. Du musst so nicht zwölf oder mehr einzelne Bewegungen gleichzeitig im Kopf halten.</p><p>Bei vier Kacheln sind nur <b>drei Fahrten</b> nötig, weil die erste Kachel schon erreicht ist. Das lässt sich am Boden zählen: vier Orte, drei Verbindungen. wiederhole 4 [vor] würde am rechten Rand gegen die Wand führen.</p><p>Nach der unteren Reihe blickt der Roboter nach rechts. links dreht ihn nach oben, vor führt in die obere Reihe, links richtet ihn nach links aus. Erst dann passt der gerade Teilplan erneut.</p>'},
 {id:'switch',group:'Planen',title:'Der nächste Übergang ist anders.',short:'Den Blick mitdenken',room:{width:4,height:3,start:[1,2,3]},prior:['1,2','2,2','3,2','4,2','1,3','2,3','3,3','4,3'],code:'links\nvor\nlinks',editable:true,
 goal:'Wähle Drehungen aus der aktuellen Blickrichtung.',
 task:'Zwei Reihen sind schon sauber. Er steht links in der Mitte und blickt nach links. Plane den Übergang nach links oben – dort soll er nach rechts blicken.',
 question:'Warum brauchst du hier andere Drehungen als am rechten Rand?',
 hints:['Sein Blick zeigt jetzt nach links. Welche Vierteldrehung zeigt von dort nach oben?','rechts → vor → rechts erreicht die obere Reihe und richtet ihn nach rechts aus.'],
 solution:'rechts → vor → rechts. Nach der ersten Rechtsdrehung blickt er nach oben. Nach vor steht er links oben. Die zweite Rechtsdrehung richtet ihn nach rechts aus. Die drei übrigen oberen Kacheln sind noch nicht erreicht.',
 explain:'<h3>Ein Übergang hängt vom Startzustand ab</h3><p>Am rechten Rand führte links → vor → links nach oben. Diesen Übergang kannst du nicht unverändert an jedem Rand verwenden: Jetzt blickt der Roboter nach links.</p><p>Von diesem Blick aus dreht <b>rechts</b> nach oben. links würde nach unten zeigen und zurück in die bereits gereinigte Reihe führen. Standort und Blick bilden zusammen den <b>Zustand</b>, von dem der nächste Teilplan ausgeht.</p><p>Der Auftrag hier ist nur der Übergang. Die acht schon sauberen Kacheln stammen aus den vorigen Teilplänen. Nach dem Übergang sind neun von zwölf sauber; für den Rest folgt eine neue gerade Fahrt.</p>'},
 {id:'own',group:'Planen',title:'Jetzt gehört der Plan dir.',short:'Die ganze Fläche',room:{width:4,height:3,start:[1,3,1]},code:'',editable:true,
 goal:'Entwickle und begründe einen eigenen Algorithmus.',
 task:'Reinige alle zwölf Kacheln ohne Wandstopp. Verwende mindestens eine Schleife. Baue deinen Weg aus Teilplänen; mehrere Lösungen sind möglich.',
 question:'Erkläre deinen Plan: Welche Teilflächen bearbeitest du, und warum bleibt keine Kachel übrig?',
 hints:['Plane erst eine Reihe, dann den Übergang. Nutze die Start- und Endrichtung jedes Teilplans.','Reihenweise geht es unten nach rechts, in der Mitte nach links und oben wieder nach rechts. Die beiden Übergänge sind verschieden.'],
 solution:'Ein möglicher Weg:\nwiederhole 3 [vor]\nlinks\nvor\nlinks\nwiederhole 3 [vor]\nrechts\nvor\nrechts\nwiederhole 3 [vor]\nAuch ein spaltenweiser Weg ist gültig. Entscheidend sind alle zwölf Kacheln, kein Wandstopp und mindestens eine Schleife.',
 explain:'<h3>Vom Weg zum Algorithmus</h3><p>Ein <b>Algorithmus</b> ist eine eindeutige, geordnete Folge von Anweisungen zur Lösung eines Problems. Dein Programm beschreibt einen solchen Plan in der vereinbarten Schreibweise.</p><p>Entwirf zuerst Teilflächen. Du kannst Reihen oder Spalten wählen. Verfolge anschließend für jeden Übergang Ort und Blick. Baue den Plan, prüfe die Fahrt, finde die erste Abweichung und ändere gezielt diesen Teil.</p><p><b>Drei Kriterien:</b> Das Programm ist ausführbar, es erreicht alle zwölf Kacheln ohne Wandstopp, und es enthält eine Schleife. Eine andere Reihenfolge als die Musterlösung kann alle Kriterien erfüllen. Weniger Code bedeutet nicht automatisch weniger Aktionen.</p><p>Die Simulation prüft den Weg. Deine Begründung zeigt zusätzlich, ob du das Prinzip erklären kannst: Warum diese Anzahl? Warum diese Drehung? Warum bleibt nichts übrig?</p>'},
 {id:'check',group:'Übertragen',title:'Zurück am Start. Ist alles sauber?',short:'Eine Behauptung prüfen',room:{width:4,height:3,start:[1,3,1]},code:'wiederhole 3 [vor]\nlinks\nwiederhole 2 [vor]\nlinks\nwiederhole 3 [vor]\nlinks\nwiederhole 2 [vor]\nlinks',editable:true,
 goal:'Prüfe eine Behauptung an sichtbaren Kriterien.',
 task:'„Er kommt wieder am Start an. Also ist der ganze Boden sauber.“ Prüfe diese Behauptung. Finde die übrigen Krümel und ergänze den Plan.',
 question:'Warum reicht die Rückkehr zum Start als Beweis nicht aus?',
 hints:['Vergleiche den Rand mit dem Inneren. Welche Kacheln hat die Spur nicht erreicht?','Spalte 2 und 3 in Reihe 2 fehlen. Ab dem ursprünglichen Endstand kannst du vor → links → vor → rechts → vor ergänzen.'],
 solution:'Die Randrunde erreicht nur zehn Kacheln. (2,2) und (3,2) bleiben offen. Die angegebene Ergänzung fährt gezielt durch die Mitte. Zurück am Start und ganze Fläche sauber sind zwei verschiedene Kriterien.',
 explain:'<h3>Eine plausible Behauptung prüfen</h3><p>Ein geschlossenes Bild kann vollständig wirken. Trotzdem kann ein Weg eine Fläche nur umranden. Prüfe deshalb die <b>besuchten Kacheln</b>, nicht nur den Endpunkt oder die Form der Spur.</p><p>Hier stimmen Start und Ende überein. Innen liegen aber noch zwei schmutzige Kacheln. Das ist ein Gegenbeispiel zur Behauptung.</p><p>Verbessere den Plan mit einem gezielten Teilweg. Du musst nicht alles neu bauen. Nutze im Endzustand die Blickrichtung, um die beiden offenen Kacheln zu erreichen.</p>'},
 {id:'transfer',group:'Übertragen',title:'Gleiche Befehle. Gleicher Ablauf?',short:'Eine andere Maschine',station:true,
 goal:'Übertrage den Schleifenkörper auf einen neuen Fall.',
 task:'Eine Prüfstation hat Platz für genau ein Werkstück. Vergleiche beide Pläne: Erst aufnehmen, dann prüfen, dann ablegen. Welcher Plan bearbeitet drei Werkstücke?',
 question:'Warum funktioniert nur einer der Pläne, obwohl beide jeden Befehl dreimal enthalten?',
 hints:['Die Station muss frei sein, bevor sie etwas aufnehmen kann.','Plan B will ein zweites Werkstück aufnehmen, obwohl das erste noch auf der Station liegt.'],
 solution:'Plan A: dreimal [aufnehmen; prüfen; ablegen]. Nach jedem Durchlauf ist die Station frei. Plan B stoppt beim zweiten Aufnehmen. Nicht nur die Anzahl, auch Gruppierung und Reihenfolge sind entscheidend.',
 explain:'<h3>Das Prinzip gilt über den Roboter hinaus</h3><p>Plan A wiederholt den <b>ganzen Arbeitsablauf</b>. Jeder Durchlauf nimmt ein Werkstück auf, prüft es und legt es ab. Danach kann der nächste beginnen.</p><p>Plan B bündelt gleiche Befehle: erst dreimal aufnehmen, dann dreimal prüfen, dann dreimal ablegen. Schon beim zweiten Aufnehmen ist der einzige Platz belegt. Dieselben Befehle mit denselben Anzahlen ergeben deshalb nicht automatisch denselben Ablauf.</p><p>Auch dieses Modell hat Grenzen. Es kennt genau einen Platz und feste Arbeitsschritte. Ein echter Reinigungsroboter hat Sensoren; unser Bodenmodell reagiert nicht selbstständig auf einen neu aufgestellten Stuhl. Ein Bild des Weges ist eine Darstellung, keine Steuerung.</p>'},
 {id:'return',group:'Wiederkommen',title:'Neuer Start. Kannst du es noch?',short:'Nach einer Pause',room:{width:2,height:2,start:[1,1,2]},code:'wiederhole 3 [vor; links]\nrechts',predict:true,sequence:['vor','links','vor','links','vor','links','rechts'],
 goal:'Rufe das Prinzip ohne deinen alten Plan ab.',
 task:'Bearbeite diese Aufgabe nach einer Pause noch einmal. Neuer Start: links oben, Blick unten. Sage das Ende voraus und schreibe die ganze Folge aus, bevor du prüfst.',
 question:'Was gehört zum Körper, was kommt danach? Erkläre den Unterschied ohne die Hilfe.',
 hints:['Beginne mit der Blickrichtung nach unten. Das erste vor fährt links nach unten.','Dreimal das Paar vor → links, danach einmal rechts: insgesamt sieben Aktionen.'],
 solution:'vor → links | vor → links | vor → links | rechts. Ende rechts oben, Blick oben. Drei Durchläufe haben sechs Aktionen; die einzelne Rechtsdrehung macht die siebte.',
 explain:'<h3>Prüfe, was du selbst erklären kannst</h3><p>Abrufen ist mehr als Wiederlesen: Verdecke deine alten Notizen und löse die neue Aufgabe zuerst selbst. Der neue Start hilft dabei zu prüfen, ob du das Prinzip anwenden kannst.</p><p>Vergleiche danach Folge, Endort und Blick. Falls etwas nicht passt, gehe zur ersten Abweichung zurück. Nutze eine Hilfe und löse die Aufgabe später erneut.</p><p><b>Dein Lernprodukt:</b> ein geprüfter eigener Flächenplan und eine Erklärung seiner Teilpläne. Du solltest außerdem einen Schleifenkörper ausschreiben, eine Anweisung danach unterscheiden und die Grenzen der Simulation benennen können.</p>'}
 ];
 function lesson(id){const l=lessons.find(x=>x.id===id);if(!l)throw new Error('Unbekannte Station');return l;}
 function blocks(text){if(!text.trim())return [];const syntax=M.inspectProgram(text);if(!syntax.ok)throw new Error(syntax.message||'Nutze ein Semikolon zwischen den Befehlen.');return syntax.blocks.map(b=>({body:[...b.body],count:b.count,repeat:b.repeat}));}
 function code(bs){return bs.map(b=>b.repeat?'wiederhole '+b.count+' ['+b.body.join('; ')+']':b.body[0]).join('\n');}
 function run(id,text){const l=lesson(id),r=M.simulate(l.room,text);
 if(l.prior){for(const s of r.trace)s.cleaned=[...new Set([...l.prior,...s.cleaned])];r.cleaned=r.trace.at(-1).cleaned;r.missing=r.missing.filter(c=>!r.cleaned.includes(c));r.success=r.status==='complete'&&!r.missing.length;}
 return r;
 }
 function assess(id,text){
 const l=lesson(id);let r;try{r=run(id,text);}catch(e){return {ok:false,kind:'syntax',title:'Der Plan braucht noch eine Änderung.',message:e.message};}
 if(r.status==='wall')return {ok:false,kind:'wall',title:'Hier trifft der Plan auf den Rand.',message:'Aktion '+(r.trace.length-1)+' würde aus dem Raum führen. Geh einen Schritt zurück und prüfe dort den Blick. Ändere den passenden Baustein.'};
 if(r.status!=='complete')return {ok:false,kind:'limit',title:'Der Plan ist zu lang.',message:'Nach 100 Aktionen wird angehalten. Prüfe kürzere Teilpläne.'};
 if(id==='switch'){const ok=r.end.join() === '1,1,1';return {ok,kind:ok?'success':'target',title:ok?'Der Übergang passt.':'Prüfe Zielkachel und Blick.',message:ok?'Links oben, Blick rechts. Neun Kacheln sind jetzt sauber; die restliche obere Reihe folgt erst im nächsten Teilplan.':'Das Ziel ist links oben mit Blick nach rechts. Beim Start zeigt der Pfeil nach links: Welche Drehung führt von dort nach oben?'};}
 if(id==='repair'&&!blocks(text).some(b=>b.repeat&&b.body.includes('vor')&&b.body.some(a=>a==='links'||a==='rechts')))return {ok:false,kind:'body',title:'Fahren und Drehen gehören in denselben Körper.',message:'Die Fahrt allein reicht für diesen Auftrag nicht. In einem wiederholten Durchlauf sollen Fahren und Drehen zusammen vorkommen. Bearbeite die Schleife und prüfe die Runde erneut.'};
 if(['own','rows','check','repair'].includes(id)){
  const all=r.missing.length===0,loop=blocks(text).some(b=>b.repeat),direction=id!=='repair'||r.end.join()==='1,2,1';
  const ok=all&&loop&&direction;return {ok,kind:ok?'success':!all?'incomplete':!loop?'missing-loop':'direction',title:ok?'Dein Plan erfüllt den Auftrag.':!all?'Ein Teil des Bodens ist noch offen.':!loop?'Der Weg passt. Ergänze eine Schleife.':'Der Weg passt. Prüfe noch den Blick.',
  message:ok?r.cleaned.length+' Kacheln erreicht, kein Wandstopp, Schleife enthalten. Begründe jetzt, warum dein Weg die Fläche abdeckt.':!all?'Noch Krümel auf '+r.missing.map(s=>'('+s+')').join(', ')+'. Suche den passenden Übergang und verbessere nur diesen Teil.':!loop?'Der Auftrag verlangt mindestens eine Wiederholung. Fasse eine passende Gruppe zusammen.':'Die Runde soll am Start mit Blick nach rechts enden. Ist eine Drehung zu viel im Plan?'};
 }
 return {ok:true,kind:'observed',title:'Die Fahrt ist zu Ende.',message:'Vergleiche deine Vermutung mit dem Ergebnis. Erkläre, wie die Anweisungen zu diesem Ende führen.'};
 }
 function station(plan){
 const actions=plan==='A'?Array.from({length:3},()=>['aufnehmen','prüfen','ablegen']).flat():['aufnehmen','aufnehmen','aufnehmen','prüfen','prüfen','prüfen','ablegen','ablegen','ablegen'];
 let state='frei',completed=0,error=null;const trace=[{state,completed,action:'Start'}];
 for(const action of actions){
  const allowed=action==='aufnehmen'?state==='frei':action==='prüfen'?state==='belegt':state==='geprüft';
  if(!allowed){error={step:trace.length,action};trace.push({state,completed,action,error:true});break;}
  if(action==='aufnehmen')state='belegt';else if(action==='prüfen')state='geprüft';else{state='frei';completed++;}
  trace.push({state,completed,action});
 }
 return {trace,completed,error};
 }
 const api={lessons,lesson,blocks,code,run,assess,station};
 if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.Workshop=api;
})(globalThis);
