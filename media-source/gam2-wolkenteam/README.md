# GAM-2 · Wolkenteam-Shopfolge

Editierbare Quelle des stillen 24-Sekunden-Films und der drei SVG-Einzelzustände. episode.json ist die gemeinsame fachliche Datenquelle. build.cjs erzeugt die HyperFrames-Komposition und Vektoransichten. Preise sind Modellangaben aus der bestehenden Karte C.

Lokal erzeugen:

    node media-source/gam2-wolkenteam/build.cjs ABSOLUTER_LOKALER_RENDERORDNER

Der Erzeuger übernimmt die vorhandene GSAP-Datei aus recherchefilm-1.1 ausschließlich in den lokalen Renderordner. Auf der Lernseite werden keine neue Laufzeit und keine externen Dienste benötigt.

Die geprüfte Produktion verwendet die vorhandene HyperFrames-CLI 0.8.114 und lokales FFmpeg. Diese CLI bietet usage nicht an; ein Planverbrauch wird nicht behauptet. Keine Cloud- oder KI-Provideraufrufe nötig.

Reihenfolge: check, snapshot, Sichtprüfung, lokale Vorschau, render mit 24 s/30 fps, FFprobe, vollständige Dekodierung und Sichtung der tatsächlichen Filmframes. Technische Bäume, Logs und Zwischenstände bleiben außerhalb OneDrive. Nur fertiges MP4 und drei SVGs werden nach prototypes/klasse7-gaming/inhalt/material übernommen und im Quellenmanifest gebunden.

In der vorhandenen gelenkten Übung wahlweise Textkarte oder Shopfolge verwenden. Drei ruhende Ansichten haben vollständige auswählbare Textbeschreibungen. Ende vor dem Kauf; Film zeigt weder Rechnung, Rest noch Urteil.

Eigene Medien: IuM-Lernwerk, mit KI-Unterstützung erstellt, 2026, CC BY-SA 4.0. Code: MIT gemäß Projektstandard. Systemschriften werden nicht mitgeliefert. Keine realen Shops, Marken, Spielenden oder Kundendaten.

Plan und vollständige Lernwegbilanz: docs/produktion/2026-11-09-gam2-shopfolge-*.
