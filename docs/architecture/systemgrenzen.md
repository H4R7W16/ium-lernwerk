# Systemgrenzen der Learning Experience

## Eigentum und Abhängigkeitsrichtung

`@ium/learning-experience` besitzt den versionierten Inhaltsvertrag `ExperienceContentV1`, semantische Oberflächenrollen, Komponenten, Fokus- und Resilienzadapter sowie die ruhige visuelle Grundlage. Das Paket hat keine Abhängigkeit zu IUM5, Astro-Laufzeitdiensten, IndexedDB oder einem Backend.

`@ium/ium-5-core-05` besitzt Befehle, Algorithmen, Interpreter, Szenarien, Laufspuren, Payloadvalidierung und Migration. Es bleibt framework-, DOM- und Experience-frei. `apps/lernwerk-portal` darf beide Pakete gerichtet zusammenführen, Browserfakten lesen und die lokale Zustandsportierung anschließen.

```text
@ium/learning-experience ─┐
                          ├─> @ium/lernwerk-portal
@ium/ium-5-core-05 ───────┘

@ium/local-state ─────────> @ium/lernwerk-portal
```

Die Pfeile zeigen zum Verbraucher. Zwischen dem generischen Experience-Paket und dem IUM5-Fachkern besteht keine Importkante.

## Vertragsversionen

- Inhalt und Komponenten: `ExperienceContentV1`, Version 1.
- IUM5-Zustand: `stateSchemaVersion 2` mit expliziter Migration `stateSchemaVersion 1 → 2`.
- Technische Resilienzmeldungen und fachliche Lernrückmeldung bleiben getrennte Ausgabekanäle.

## Nicht-Generalisierungen

Nicht in das generische Paket verschoben werden IUM5-Raster, Editor, Befehlskatalog, Laufspursemantik, Szenario-IDs, fachliche Sprache oder Checkpoint-Platzierung. Ebenso entstehen weder ein beliebiger Seitenbaukasten noch ein Schema-Renderer für offene Domänenmodelle. Neue Module müssen eigene Fachadapter und Portabilitätsnachweise liefern.
