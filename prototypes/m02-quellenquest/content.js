(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.QuestContent=factory();})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const sources={
 A:{id:'A',kind:'Chatnachricht',title:'Schon beschlossen?',author:'Mila, Klasse 5b',date:'23. September 2026 · 16:10 Uhr',purpose:'Mila erzählt weiter, was sie gehört hat.',context:'Erfundener Klassenchat · Nachricht an die Klasse',lines:[
 {id:'A1',text:'Jetzt ist es sicher: Ab Montag wird unsere ganze Pausenwiese zum Schulgarten!'},
 {id:'A2',text:'Das hat die Garten-AG doch angekündigt. Dann können wir da gar nicht mehr spielen!'}]},
 B:{id:'B',kind:'Vorschlag der Garten-AG',title:'Unsere Idee für die Wiese',author:'Garten-AG der Schule',date:'10. Juni 2026',purpose:'Die AG möchte andere von ihrer Idee überzeugen.',context:'Erfundener Aushang der AG · Vorschlag für die Schulleitung',lines:[
 {id:'B1',text:'Wir wünschen uns einen Schulgarten auf der ganzen Pausenwiese.'},
 {id:'B2',text:'Dort könnten wir Gemüse und Blumen pflanzen. Wir haben der Schulleitung einen Vorschlag geschickt.'},
 {id:'B3',text:'Noch ist nicht entschieden, ob unser Vorschlag umgesetzt wird.'}]},
 C:{id:'C',kind:'Mitteilung der Schulleitung',title:'Zwei Beete zum Ausprobieren',author:'Frau Kaya, Schulleiterin',date:'22. September 2026',purpose:'Die Schulleitung informiert darüber, was beschlossen wurde.',context:'Erfundene Mitteilung auf der Schulwebseite · an Kinder und Eltern',lines:[
 {id:'C1',text:'Am Montag, 28. September, stellen wir zwei Hochbeete am Rand der Pausenwiese auf.'},
 {id:'C2',text:'Die übrige Wiese bleibt zum Spielen frei.'},
 {id:'C3',text:'Wir probieren den Garten bis Ende November aus. Über einen größeren Garten im nächsten Jahr ist noch nicht entschieden.'}]},
 D:{id:'D',kind:'Mitteilung der Bibliothek',title:'Kurze Pause für den Regalumbau',author:'Herr Yilmaz, Leiter der Schulbibliothek',date:'7. Oktober 2026',purpose:'Das Bibliotheksteam teilt die Öffnungszeiten während des Umbaus mit.',context:'Erfundener Aushang am Eingang der Schulbibliothek',lines:[
 {id:'D1',text:'Am Montag, 12. Oktober, bleibt die Schulbibliothek von 10 bis 11 Uhr wegen eines Regalumbaus geschlossen.'},
 {id:'D2',text:'Ab 11 Uhr ist sie wieder geöffnet. Ihr könnt dann wie gewohnt Bücher ausleihen.'}]},
 E:{id:'E',kind:'Chatnachricht',title:'Am Montag geschlossen?',author:'Noah, Klasse 5a',date:'9. Oktober 2026 · 17:05 Uhr',purpose:'Noah gibt eine gehörte Nachricht weiter.',context:'Erfundener Klassenchat',lines:[
 {id:'E1',text:'Ich habe gehört, die Bibliothek ist am Montag den ganzen Tag zu. Da brauchen wir gar nicht hinzugehen!'}]}
};
const verdicts=[{id:'belegt',label:'Belegt',meaning:'Eine passende Textstelle stützt die Aussage.'},{id:'widerlegt',label:'Widerlegt',meaning:'Eine passende Textstelle sagt das Gegenteil.'},{id:'offen',label:'Offen',meaning:'Mit diesen Quellen lässt sich das noch nicht entscheiden.'}];
const claims=[
 {id:'beete',text:'Am Montag werden zwei Hochbeete aufgestellt.',answer:'belegt',evidence:['C1'],feedback:'C1 nennt den Montag und die zwei Hochbeete. Das ist der angekündigte Beschluss.'},
 {id:'wiese',text:'Die ganze Pausenwiese wird jetzt zum Garten.',answer:'widerlegt',evidence:['C2'],feedback:'C2 sagt ausdrücklich: Die übrige Wiese bleibt zum Spielen frei. Der Wunsch der AG ist kein Beleg für einen Beschluss.'},
 {id:'wunsch',text:'Im Juni wünschte sich die Garten-AG einen Garten auf der ganzen Wiese.',answer:'belegt',evidence:['B1'],feedback:'B1 belegt den damaligen Wunsch. Eine ältere Quelle kann genau zu dieser Frage passen.'},
 {id:'zukunft',text:'Im nächsten Jahr wird der Garten größer.',answer:'offen',evidence:['C3'],feedback:'C3 sagt, dass darüber noch nicht entschieden ist. Das heißt weder „Ja“ noch „Nein“. Wir müssen die spätere Entscheidung abwarten.'}
];
const transfer=[
 {id:'tag',text:'Die Bibliothek ist am Montag den ganzen Tag geschlossen.',answer:'widerlegt',evidence:['D2'],feedback:'D2 nennt die Öffnung ab 11 Uhr. Noahs neuere Nachricht lässt diese wichtige Angabe weg.'},
 {id:'elf',text:'Am Montag kann man ab 11 Uhr Bücher ausleihen.',answer:'belegt',evidence:['D2'],feedback:'D2 sagt das ausdrücklich. Der Leiter informiert über die Öffnungszeiten seiner Bibliothek.'},
 {id:'computer',text:'Beim Umbau bekommt die Bibliothek neue Computer.',answer:'offen',evidence:['none'],feedback:'Weder die Mitteilung noch der Chat sagen etwas über neue Computer. Fehlende Angaben sind kein Gegenbeweis.'}
];
const sourceQuestions=[
 {id:'beschluss',question:'Was ist für kommenden Montag beschlossen? Welche Quelle hilft dir am direktesten?',answer:'C',feedback:'C kommt von der Schulleitung, die den Beschluss mitteilt. Inhalt, Zuständigkeit und Datum passen zu dieser Frage. Das neuere Datum allein reicht als Grund nicht.'},
 {id:'wunsch',question:'Was wollte die Garten-AG im Juni? Welche Quelle hilft dir am direktesten?',answer:'B',feedback:'B stammt von der AG und beschreibt ihren damaligen Wunsch. Für diese Frage ist gerade der ältere Vorschlag die passende Quelle.'}
];
const steps=[
 {id:'auftrag',short:'Auftrag',title:'Was wird aus unserer Pausenwiese?',goal:'Du findest heraus, welche Behauptung du prüfen sollst.',task:'Die Klasse ist wegen Milas Nachricht unsicher. Prüfe, was wirklich beschlossen wurde, und verfasse eine kurze Antwort mit Belegen.',sources:['A'],time:5,
 knowledge:'Eine Behauptung ist eine Aussage, die jemand für richtig hält. Bevor du sie weitergibst, prüfst du, was dafür oder dagegen spricht.',
 hint:'Achte auf die Wörter „sicher“, „Montag“ und „ganze“. Was behauptet Mila damit?',
 help:'Es geht nicht nur darum, ob es einen Garten gibt. Entscheidend ist, ob wirklich die ganze Wiese ab Montag zum Garten wird.',
 outcome:'Eine genaue Prüffrage, zunächst mündlich oder in einem Satz.',
 expected:'Wird ab Montag wirklich die ganze Pausenwiese zum Schulgarten?',
 teacher:'Zeigen Sie den Chat. Sammeln Sie zuerst Prüffragen, keine Wahrheitsabstimmung. Markieren Sie „ganze“ und „ab Montag“. Das Fragezeichen in der Materialüberschrift verrät noch kein Urteil.',
 criteria:['Die Prüffrage nennt die ganze Wiese und den Zeitpunkt.','Ein erster Eindruck wird noch nicht als geprüfte Tatsache behandelt.']},
 {id:'quellen',short:'Quellen',title:'Wer kann das wissen?',goal:'Du unterscheidest Nachricht, Vorschlag und Beschluss.',task:'Lies die drei Quellen. Achte darauf, wer den Text geschrieben hat, wann und wozu. Entscheide dann, welche Quelle zu welcher Frage passt.',sources:['A','B','C'],time:10,
 knowledge:'Eine Quelle gibt dir Informationen. Frage: Wer hat das geschrieben? Wann? Wozu? Woher kann die Person das wissen? Eine schöne Gestaltung oder ein neueres Datum machen eine Aussage noch nicht richtig.',
 hint:'Vergleiche die Wörter „wünschen“, „noch nicht entschieden“ und „stellen wir auf“.',
 help:'Die Garten-AG kann ihren Wunsch erklären. Die Schulleitung informiert hier über den Beschluss. Der Chat erzählt eine Nachricht weiter.',
 outcome:'Zwei passende Quellen und eine mündliche Begründung für deine Auswahl.',
 expected:'Für den aktuellen Beschluss nutze ich C von der Schulleitung. Für den Wunsch im Juni nutze ich B von der Garten-AG.',
 teacher:'Lesen Sie auf Wunsch eine Quelle gemeinsam vor. Lassen Sie zu derselben Quelle unterschiedliche Fragen stellen. So wird keine allgemeine Rangliste „Chat schlecht, Schulleitung immer richtig“ gelernt.',
 criteria:['Die Auswahl wird aus Frage, Inhalt und Urheberschaft begründet.','Der ältere AG-Text wird für die Frage nach dem Wunsch richtig genutzt.']},
 {id:'belege',short:'Belege',title:'Welche Stelle zeigt das?',goal:'Du unterscheidest belegt, widerlegt und offen und nennst einen passenden Textbeleg.',task:'Prüfe die vier Aussagen. Wähle jeweils ein Urteil und die Textstelle, die dazu passt. Verbessere deine Zuordnung nach der Rückmeldung.',sources:['B','C'],time:15,
 knowledge:'Ein Beleg ist eine konkrete Stelle, die dein Urteil stützt. „Widerlegt“ braucht einen Gegenbeleg. Wenn etwas nicht in den Quellen steht oder noch nicht entschieden ist, bleibt es offen.',
 hint:'Lies nicht nur einzelne Wörter. Ein Wunsch ist etwas anderes als eine Entscheidung.',
 help:'„Noch nicht entschieden“ bedeutet: Es könnte später so kommen, aber auch anders. „Die übrige Wiese bleibt frei“ spricht dagegen, dass die ganze Wiese zum Garten wird.',
 outcome:'Vier Zuordnungen. Erkläre eine davon zusätzlich in eigenen Worten.',
 expected:'Zwei Beete: belegt, C1. Ganze Wiese jetzt: widerlegt, C2. Wunsch im Juni: belegt, B1. Größerer Garten nächstes Jahr: offen, C3.',
 teacher:'Modellieren Sie bei Bedarf die erste Aussage. Danach bearbeiten die Kinder die übrigen selbst. Lassen Sie ein Kind den Unterschied zwischen C2 und C3 erklären; eine richtige Auswahl allein genügt nicht.',
 criteria:['Urteil und Textstelle passen zusammen.','Widerlegung und fehlende Entscheidung werden unterschieden.','Mindestens eine Zuordnung wird eigenständig erklärt.']},
 {id:'antwort',short:'Antwort',title:'Deine Antwort an die Klasse',goal:'Du schreibst eine sachliche Antwort mit Quellenbeleg und einer Wissensgrenze.',task:'Antworte Mila in drei bis vier Sätzen. Erkläre, was beschlossen ist, worauf du dich stützt und was noch offen bleibt. Prüfe und verbessere deinen Text.',sources:['A','B','C'],time:15,
 knowledge:'Eine hilfreiche Antwort nennt das Ergebnis, eine konkrete Textstelle und die Quelle. Sie sagt auch, was noch nicht bekannt ist. Du kannst eine Aussage korrigieren, ohne die Person anzugreifen.',
 hint:'Beginne mit „Nicht die ganze Wiese …“. Nenne dann die Mitteilung und eine passende Stelle.',
 help:'Satzanfänge: „Laut … vom …“ / „Dort steht …“ / „Der Vorschlag der AG war …“ / „Noch offen ist …“. Du darfst deine Antwort auch erst mündlich formulieren.',
 outcome:'Deine begründete Antwort und eine konkrete Verbesserung oder begründete Beibehaltung.',
 expected:'Nicht die ganze Wiese wird zum Garten. Laut Mitteilung der Schulleitung vom 22. September werden am Montag zwei Hochbeete aufgestellt; die übrige Wiese bleibt frei (C1/C2). Der AG-Vorschlag war ein Wunsch. Ob der Garten nächstes Jahr größer wird, ist noch offen (C3).',
 teacher:'Für einen Lehrvortrag können Sie die schwache und die stärkere Antwort vergleichen. Lassen Sie Beleg, Herkunft und offene Frage farblich unterscheiden. In Partnerarbeit fragt das andere Kind: „Welche Stelle belegt diesen Satz?“',
 criteria:['Das Ergebnis unterscheidet zwei Beete und ganze Wiese.','Quelle und konkrete Stelle werden genannt.','Die offene Entscheidung wird benannt.','Der Ton bleibt sachlich und eine Überarbeitung wird begründet.']},
 {id:'transfer',short:'Neuer Fall',title:'Neue Nachricht. Gleicher prüfender Blick.',goal:'Du prüfst selbstständig einen neuen Fall und begründest, welche Quelle zu deiner Frage passt.',task:'Kannst du am Montag um 12 Uhr ein Buch ausleihen? Untersuche den Aushang und den neueren Chat. Prüfe die Aussagen und begründe deine Antwort.',sources:['D','E'],time:10,
 knowledge:'Prüfe die Quelle zur konkreten Frage. Auch eine neuere Nachricht kann wichtige Angaben weglassen. Fehlende Informationen bleiben offen.',
 hint:'Vergleiche die Zeitangaben genau. Wer informiert über die Öffnungszeiten, wer erzählt etwas weiter?',
 help:'„Von 10 bis 11 Uhr geschlossen“ und „den ganzen Tag geschlossen“ bedeuten nicht dasselbe. Über Computer steht in beiden Quellen nichts.',
 outcome:'Eine Antwort mit Textbeleg, Quellenbegründung und einer offenen Information.',
 expected:'Nach dem Aushang kann ich um 12 Uhr ein Buch ausleihen: D2 sagt, dass die Bibliothek ab 11 Uhr geöffnet ist. Der Bibliotheksleiter informiert über die Öffnungszeiten. Der neuere Chat lässt die Uhrzeiten weg. Neue Computer sind nicht belegt.',
 teacher:'Lassen Sie diesen Fall möglichst vor einer gemeinsamen Erklärung individuell bearbeiten. Fragen Sie danach: „Warum hilft uns der ältere Aushang hier mehr?“ Bei Schwierigkeiten gemeinsam Zeitangaben markieren und mit einem weiteren kurzen Fall nachsichern.',
 criteria:['Die Antwort nennt 12 Uhr und D2 als Beleg.','Die ältere Quelle wird aus Inhalt und Zuständigkeit begründet.','Zu den Computern wird keine unbelegte Entscheidung behauptet.']}
];
return {sources,steps,claims,transfer,verdicts,sourceQuestions};
});
