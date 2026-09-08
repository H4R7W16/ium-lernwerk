# MAT-08 - S4 Transfer und S5 Systeme

## P5 - S4: Eine Prüfstation mit neuem Zustand

Vereinfachtes Modell: Die Station ist zuerst **frei**. `aufnehmen` braucht eine freie Station und macht sie **belegt**. `prüfen` braucht ein aufgenommenes Werkstück und macht den Zustand **geprüft**. `ablegen` braucht ein geprüftes Werkstück und macht die Station wieder **frei**.

Prüfe zwei Gruppierungen für drei Werkstücke:

- A: dreimal den ganzen Körper `[aufnehmen; prüfen; ablegen]`
- B: dreimal `[aufnehmen]`, danach dreimal `[prüfen]`, danach dreimal `[ablegen]`

Erstelle für beide Fassungen eine Zustandsfolge. Entscheide, welche ausführbar ist. Benenne bei der anderen die erste unmögliche Aktion und begründe die passende Körpergrenze. Dies ist eine manuelle Modellprüfung, kein programmierter realer Prüfautomat.

## P6 - S5: Vier Funktionsbriefe

**A - Digitale Zeitsteuerung:** Ein digitales System erhält eingestellte Zeitpunkte und einen aktuellen Zeitwert. Es vergleicht diese Eingaben und löst bei erfüllter Bedingung eine festgelegte Aktion aus.

**B - Digitale Wegberechnung:** Ein digitales System erhält Start, Ziel und eine interne Darstellung möglicher Verbindungen. Es verarbeitet diese Daten und gibt einen berechneten Weg aus. Der Brief beschreibt keine konkrete App und keinen bestimmten Suchalgorithmus.

**C - Vorschrift auf Papier:** Auf einem Blatt steht eine eindeutige Schrittfolge zum Sortieren von Karten. Die Vorschrift kann algorithmisch sein; das Papier verarbeitet sie nicht selbst als digitales System.

**D - Isoliertes Standbild:** Ein einzelnes Bildschirmbild zeigt Symbole und Zahlen. Ohne Eingaben, Zustandsänderungen oder Verarbeitungsregeln lässt sich daraus die wesentliche Funktion des Gesamtsystems nicht bestimmen.

Ordne A bis D begründet ein. Nenne für A und B je einen notwendigen Verarbeitungsablauf. Erkläre für C und D die Grenze deiner Aussage. Recherchiere keine private Mediennutzung und erfinde keine Details realer Anwendungen.
