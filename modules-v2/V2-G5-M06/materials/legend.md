# MAT-02 - Befehle, Körper und Spur

## Raster und Zustand

- `(Spalte, Zeile)` bezeichnet ein Feld. Spalten zählen von links, Zeilen von oben.
- Die Blickrichtung gehört zum Zustand: oben, rechts, unten oder links.
- `vor` geht genau ein Feld in Blickrichtung.
- `links` und `rechts` drehen am selben Ort um 90 Grad.
- Eine Bewegung über die Rastergrenze stoppt. Der fehlerhafte Schritt verändert den Zustand nicht.

## Feste Wiederholung

`wiederhole Anzahl [Körper]` führt den **ganzen eingerahmten Körper** so oft aus, wie die Anzahl angibt. Der Körper enthält ein bis fünf Grundanweisungen. Er wird nicht verschachtelt. Die Klammer ist keine zusätzliche Aktion.

Lineare Textform: „Wiederhole viermal. Körper beginnt. Vor. Links. Körper endet.“ Diese Form bewahrt Anzahl, Reihenfolge und Gruppierung.

## Ablaufgrafik, Code und Spur

- Deine Ablaufgrafik ist ein eigener Entwurf: Start, geordnete Anweisungen, sichtbarer Körperrahmen, Anzahl und Ende.
- Dein Code ist die tatsächlich ausführbare Anweisungsfolge. Er darf von der Grafik abweichen; dann prüfst und erklärst du die Abweichung.
- Die Spur verbindet Schrittnummer, Anweisung, Wiederholungsdurchlauf, Zustand vorher und Zustand nachher.
- Eine alte Spur gehört zu ihrem alten Code. Nach einer Codeänderung wird sie nicht automatisch zum Beleg für den neuen Code.

Nutze Pfeile zusammen mit Richtungswörtern. Farbe kann unterstützen, ist aber nie die einzige Kennzeichnung.
