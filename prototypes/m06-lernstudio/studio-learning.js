'use strict';
(function(root) {
  const node = typeof module !== 'undefined' && module.exports;
  const W = node ? require('../m06-lernwerkstatt/workshop-model.js') : root.Workshop;
  const S = node ? require('./studio-model.js') : root.Studio;
  const examples = {
    rows: 'wiederhole 3 [vor]\nlinks\nvor\nlinks\nwiederhole 3 [vor]\nrechts\nvor\nrechts\nwiederhole 3 [vor]',
    columns: 'links\nwiederhole 2 [vor]\nrechts\nvor\nrechts\nwiederhole 2 [vor]\nlinks\nvor\nlinks\nwiederhole 2 [vor]\nrechts\nvor\nrechts\nwiederhole 2 [vor]'
  };
  // Studio-specific teaching layer: the other versions keep their own content.
  const content = {
    start: {
      title: 'Fahren oder drehen?',
      core: 'vor fährt eine Kachel. links und rechts drehen den Roboter auf derselben Kachel um eine Vierteldrehung.',
      entry: 'Du brauchst noch kein Vorwissen. Der kleine Pfeil am Roboter zeigt, wohin er blickt. Seine Startkachel ist schon sauber.',
      task: 'Lies die drei Befehle von oben nach unten. Wo endet der Roboter? Tippe auf die Endkachel und wähle seinen Blick. Prüfe dann mit „Ein Befehl“.',
      explain: '<h3>Denke aus der Sicht des Roboters</h3><p><b>vor</b> bedeutet: Fahre eine Kachel in deine Blickrichtung. Das ist nicht immer nach oben auf dem Bildschirm.</p><p><b>links</b> und <b>rechts</b> bedeuten: Drehe dich auf der Stelle um eine Vierteldrehung. Dabei bleibt deine Kachel gleich. Erst das nächste <b>vor</b> fährt in die neue Richtung.</p><p>Lies das Programm von oben nach unten. Zeige nach jedem Befehl auf seine Kachel und in seine Blickrichtung. Am Rand stoppt unser Roboter. Er sucht sich keinen anderen Weg.</p>',
      criteria: ['Ich sage nach jedem Befehl, wo der Roboter steht.', 'Ich zeige, wohin er blickt, auch wenn er sich nur dreht.'],
      prompt: 'Nach vor steht er … und blickt … Nach links …',
      teach: 'Mit einem Pfeil auf einem 3 × 2-Raster beginnen: links unten, Blick rechts. Die drei Befehle vor – links – vor einzeln ansagen. Lernende zeigen jeweils Kachel und Blick. Alternativ eine Person auf der Stelle drehen lassen.',
      discuss: 'Muss sich bei „links“ auch die Kachel ändern? Was bedeutet „vor“, wenn der Pfeil nach links zeigt?'
    },
    loop: {
      title: 'Vier Durchläufe – immer die ganze Gruppe',
      core: 'Eine Schleife wiederholt alle Befehle in der Klammer. Ein Durchlauf ist die ganze Gruppe, hier vor und links.',
      entry: 'Du brauchst die drei Grundbefehle. Die Zahl 4 sagt, wie oft die ganze Gruppe ausgeführt wird.',
      task: 'Schreibe zuerst die Befehle für zwei Durchläufe aus. Starte dann das Programm. Beobachte, wie sich die ganze Gruppe viermal wiederholt.',
      explain: '<h3>Eine Klammer hält die Gruppe zusammen</h3><p><b>wiederhole 4 [vor; links]</b> heißt: erst vor, dann links. Danach beginnt dasselbe Paar von vorn. Insgesamt wird es viermal ausgeführt.</p><p>Die Gruppe in der Klammer heißt <b>Schleifenkörper</b>. Einmal die ganze Gruppe ausführen heißt <b>ein Durchlauf</b>. Der Roboter macht hier zwei Aktionen pro Durchlauf.</p><p>Vier Durchläufe sind also acht Aktionen: vor – links | vor – links | vor – links | vor – links. Erst alle vier Durchläufe zusammen führen einmal um den kleinen Boden.</p>',
      criteria: ['Ich nenne beide Befehle des Schleifenkörpers.', 'Ich erkläre: 4 Durchläufe mit je 2 Aktionen ergeben 8 Aktionen.'],
      prompt: 'Ein Durchlauf besteht aus … Die Zahl 4 bedeutet …',
      teach: 'Vier Kartenpaare „vor – links“ auslegen und dann durch „wiederhole 4 [vor; links]“ ersetzen. Mit Finger oder Figur auf einem 2 × 2-Raster vorführen: Start links unten, Blick rechts.',
      discuss: 'Was zählt die 4: einzelne Befehle, ganze Paare oder Runden um den Boden?'
    },
    after: {
      title: 'Was kommt nach der Schleife?',
      core: 'Erst laufen alle Wiederholungen in der Klammer. Danach geht es einmal mit dem nächsten Befehl weiter.',
      entry: 'Ein Durchlauf führt die ganze Gruppe in der Klammer aus. Der zusätzliche Befehl vor steht hier außerhalb der Klammer.',
      task: 'Sage Endkachel und Blick voraus. Prüfe mit „Ein Durchlauf“ die vier Wiederholungen. Untersuche dann den letzten Befehl mit „Ein Befehl“.',
      criteria: ['Ich unterscheide die Befehle in der Klammer vom Befehl danach.', 'Ich erkläre, warum dieses Programm 9 Aktionen hat.'],
      prompt: 'In der Klammer … Nach der vierten Wiederholung …',
      teach: 'Den Plan wiederhole 4 [vor; links] und darunter ein einzelnes vor an die Tafel schreiben. Die Klammer farbig markieren. Lernende zuerst das Ende nach der Schleife, dann nach dem ganzen Programm zeigen lassen.',
      discuss: 'Warum wird das letzte vor nur einmal ausgeführt? Was wäre anders, wenn es in der Klammer stünde?'
    },
    repair: {
      title: 'Finde den Fehler in der Gruppe',
      core: 'Wenn nach jeder Fahrt gedreht werden soll, müssen vor und links gemeinsam in die Schleife.',
      entry: 'Du brauchst den Schleifenkörper: Alle Befehle in seiner Klammer werden gemeinsam wiederholt.',
      task: 'Dieser Plan stoppt am Rand. Ändere ihn so, dass der Roboter alle vier Kacheln erreicht und am Start wieder nach rechts blickt. Fahren und Drehen sollen gemeinsam wiederholt werden.',
      criteria: ['Ich zeige den ersten falschen Schritt.', 'Ich erkläre, warum eine andere Zahl allein den Fehler nicht behebt.'],
      prompt: 'Der Fehler beginnt bei … In die Klammer gehört …, weil …',
      teach: 'Zunächst wiederhole 4 [vor], danach links zeigen. Vor Ausführung den zweiten Fahrbefehl untersuchen. Dann die Drehkarte in die Klammer schieben und beide Abläufe vergleichen.',
      discuss: 'Brauchen wir eine andere Zahl oder eine andere Gruppe? Was passiert jeweils beim zweiten Schritt?'
    },
    example: {
      title: 'Ein Weg aus drei Teilplänen',
      core: 'Erst eine Reihe, dann der Übergang, dann die nächste Reihe: Kleine Teilpläne machen den ganzen Weg übersichtlich.',
      entry: 'Die Fläche hat zwei Reihen mit je drei Kacheln. Die erste Kachel ist bereits sauber. Eine Drehung reinigt keine neue Kachel.',
      task: 'Untersuche den Beispielweg. Zeige die untere Reihe, den Übergang und die obere Reihe im Programm. Erkläre, wozu beide Drehungen im Übergang dienen.',
      criteria: ['Ich finde die drei Teilpläne im Programm.', 'Ich erkläre, warum drei Kacheln nur zwei Fahrten brauchen.'],
      prompt: 'Zuerst … Der Übergang braucht zwei Drehungen, weil … Zum Schluss …',
      teach: 'Den 3 × 2-Boden und einen Weg in drei Farben zeichnen: unten nach rechts, links – vor – links, oben nach links. Neben jeden Teilweg den passenden Programmteil schreiben.',
      discuss: 'Warum stehen in jeder Schleife nur zwei Fahrten? Welche Aufgabe hat die zweite Drehung?'
    },
    rows: {
      title: 'Vier Kacheln: Wie viele Fahrten?',
      core: 'Die erste Kachel zählt schon mit. Für vier Kacheln in einer Reihe brauchst du drei Fahrten.',
      entry: 'Das Beispiel verbindet zwei Reihen mit links – vor – links am rechten Rand. Hier sind beide Reihen eine Kachel länger.',
      task: 'Passe beide Schleifenzahlen an. Dein Plan soll alle acht Kacheln ohne Wandstopp erreichen. Tippe auf einen Baustein, um ihn zu ändern.',
      criteria: ['Ich begründe beide Schleifenzahlen mit den Abständen zwischen den Kacheln.', 'Ich erkläre, warum der Übergang gleich bleiben kann.'],
      prompt: 'Vier Kacheln haben … Wege dazwischen. Ich ändere …',
      teach: 'Vier Felder und die drei Verbindungen dazwischen zeichnen. Lernende das bekannte Gerüst für zwei Reihen anpassen lassen, ohne den Übergang zu verändern.',
      discuss: 'Was bleibt beim breiteren Boden gleich, was muss sich an beiden geraden Fahrten ändern?'
    },
    switch: {
      title: 'Welche Drehung passt jetzt?',
      core: 'Links und rechts gelten aus der Sicht des Roboters. Prüfe vor jedem Übergang seinen aktuellen Blick.',
      entry: 'Zwei Reihen sind bereits sauber. Der Roboter steht links in der mittleren Reihe und blickt nach links. Hier geht es nur um den Übergang.',
      task: 'Ändere die drei Befehle. Der Roboter soll links oben ankommen und dort nach rechts blicken. Die übrigen oberen Kacheln sind erst später dran.',
      criteria: ['Ich leite die erste Drehung aus dem Blick nach links ab.', 'Ich zeige Endkachel und Endrichtung meines Übergangs.'],
      prompt: 'Er blickt nach links. Deshalb drehe ich zuerst … Nach vor …',
      teach: 'Auf einem 4 × 3-Raster einen Pfeil links in die Mitte setzen, Blick links. Zielpfeil links oben, Blick rechts. Die Lernenden drei Befehlskarten legen und jede Drehung begründen lassen.',
      discuss: 'Warum führt derselbe Übergang links – vor – links hier in die falsche Reihe?'
    },
    own: {
      title: 'Dein Plan für den ganzen Boden',
      core: 'Ein Algorithmus ist ein genauer Plan aus geordneten Anweisungen. Dein Plan soll das ganze Problem lösen.',
      entry: 'Du brauchst gerade Fahrten und Übergänge. Bei vier Kacheln genügen drei Fahrten. Der Roboter startet links unten mit Blick nach rechts.',
      task: 'Plane zuerst deinen Weg, zum Beispiel mit dem Finger. Baue dann das Programm: alle zwölf Kacheln sauber, kein Wandstopp und mindestens eine Schleife.',
      criteria: ['Ich zeige, welche Reihen oder Spalten meine Teilpläne reinigen.', 'Ich begründe die Schleifenzahlen und beide Arten von Übergängen.', 'Ich zeige an den erreichten Kacheln, warum nichts übrig bleibt.'],
      prompt: 'Ich teile den Boden in … Mein erster Teilplan … Beim Übergang … Keine Kachel bleibt übrig, weil …',
      teach: 'Leeres 4 × 3-Raster anbieten. Erst einen vollständigen Weg auf Papier entwickeln, dann in Teilpläne gliedern und codieren. Reihen- und Spaltenlösungen zulassen. Kriterien sichtbar lassen: zwölf Kacheln, kein Wandstopp, mindestens eine Schleife.',
      discuss: 'Wie beweist dein Weg, dass keine Kachel fehlt? Kann ein anderer Weg denselben Auftrag erfüllen?'
    },
    check: {
      title: 'Zurück am Start. Ist alles sauber?',
      solution: 'Die Randrunde erreicht nur zehn Kacheln. Spalte 2 und 3 in Reihe 2 bleiben offen. Ergänze nach dem vorhandenen Programm:\nvor\nlinks\nvor\nrechts\nvor\nSo fährt der Roboter durch die beiden fehlenden Kacheln. Die Rückkehr zum Start allein beweist nicht, dass die ganze Fläche sauber ist.',
      core: 'Ein passender Endpunkt beweist noch nicht, dass alle Kacheln erreicht wurden. Prüfe den ganzen Auftrag.',
      entry: 'Der vorgegebene Plan fährt einmal am Rand entlang. Untersuche die Spur und die noch schmutzigen Kacheln im Inneren.',
      criteria: ['Ich benenne die beiden fehlenden Kacheln.', 'Ich widerlege die Behauptung mit einem konkreten Gegenbeispiel.'],
      prompt: 'Er steht zwar wieder am Start, aber … Meine Ergänzung erreicht …',
      teach: 'Eine Randrunde auf einem 4 × 3-Raster zeichnen. Die Behauptung „Zurück am Start, also alles sauber“ zur Abstimmung stellen. Danach besuchte und unbesuchte Felder markieren lassen.',
      discuss: 'Welche zwei Kacheln widerlegen die Behauptung? Was muss ein zusätzlicher Teilweg leisten?'
    },
    transfer: {
      title: 'Eine Gruppe für eine andere Maschine',
      core: 'Die Reihenfolge und die Gruppe sind entscheidend. Gleiche Befehle mit gleicher Anzahl können anders wirken.',
      entry: 'Ein Werkstück ist ein Gegenstand, den eine Maschine bearbeitet. Unsere Prüfstation hat nur einen Platz: aufnehmen, prüfen, ablegen macht ihn wieder frei.',
      criteria: ['Ich erkläre den Stopp beim zweiten Aufnehmen in Plan B.', 'Ich zeige, wann Plan A den Platz für das nächste Werkstück frei macht.'],
      prompt: 'Plan A wiederholt … Bei Plan B ist nach dem ersten Aufnehmen …',
      teach: 'Drei Gegenstände und einen markierten Platz verwenden. Die Klasse beide Pläne mit Karten ausführen lassen: dreimal [aufnehmen; prüfen; ablegen] gegenüber dreimal aufnehmen, dreimal prüfen, dreimal ablegen.',
      discuss: 'Wieso ist die Anzahl der Befehle gleich, aber nur ein Ablauf möglich? Welche Grenze hat dieses Modell?'
    },
    return: {
      title: 'Neuer Start: Kannst du es noch?',
      core: 'Auch bei einem neuen Start gilt: zuerst die ganze Gruppe wiederholen, danach den einzelnen Befehl ausführen.',
      entry: 'Diese Aufgabe eignet sich nach einer Pause. Der Start ist jetzt links oben mit Blick nach unten. Versuche es zuerst ohne die alten Notizen.',
      criteria: ['Ich schreibe alle sieben Aktionen in der richtigen Reihenfolge auf.', 'Ich begründe Endkachel und Blick aus dem neuen Start.'],
      prompt: 'Die drei Durchläufe ergeben … Der Befehl danach verändert …',
      teach: 'Zu Beginn einer späteren Stunde den neuen 2 × 2-Start und wiederhole 3 [vor; links], danach rechts zeigen. Erst einzeln Folge, Endkachel und Blick notieren lassen, dann gemeinsam prüfen.',
      discuss: 'Welche sechs Aktionen gehören zur Schleife? Was ändert die siebte Aktion?'
    }
  };
  function lesson(id) { return {...W.lesson(id), ...content[id], group:S.chapters.find(c=>c.ids.includes(id)).title}; }
  function evidence(id, state) {
    const s = state || S.fresh(id), l = lesson(id);
    if (!s.observed) return {kind:'open', label: l.editable ? 'Plan noch prüfen' : 'Aufgabe noch offen'};
    if (l.station) return s.compared?.includes('A') && s.compared.includes('B')
      ? {kind:'compared', label:'Beide Pläne untersucht'} : {kind:'observed', label:'Ein Plan beobachtet'};
    if (l.editable) return W.assess(id, s.code).ok
      ? {kind:'task', label:'Plan erfüllt den Auftrag'} : {kind:'revise', label:'Plan weiter verbessern'};
    const prediction = !l.predict || S.prediction(id, s.prediction) === true;
    const sequence = !l.sequence || l.sequence.join() === s.sequence.join();
    return (l.predict || l.sequence) && prediction && sequence
      ? {kind:'task', label:l.predict?'Vorhersage stimmt':'Befehlsfolge stimmt'} : {kind:'observed', label:'Fahrt beobachtet'};
  }
  function compare(id, before, after, requestedStep) {
    const a = S.run(id, before), b = S.run(id, after);
    const max = Math.max(a.trace.length, b.trace.length) - 1;
    const step = Math.max(0, Math.min(max, Math.trunc(requestedStep) || 0));
    const at = r => ({step: Math.min(step, r.trace.length - 1), trace: r.trace[Math.min(step, r.trace.length - 1)], ended: step >= r.trace.length - 1});
    return {step, max, before:at(a), after:at(b)};
  }
  function primaryAction(id) {
    if (['start','repair','return'].includes(id)) return 'step';
    return id === 'after' ? 'cycle' : 'play';
  }
  const api = {lesson, examples, evidence, compare, primaryAction};
  if (node) module.exports = api; else root.StudioLearning = api;
})(globalThis);
