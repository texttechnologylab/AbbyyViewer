[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# AbbyyViewer
Einfache Web-App um den XML Output des AbbyyFineReaders zu visualisieren und annotieren. \
https://texttechnologylab.github.io/AbbyyViewer/index.html

## Funktionen
1. Es werden die erkannten Blöcke sowie Zeichen markiert.
2. Es können Teile der XML Datei gesondert betrachtet werden.
3. Es kann ein Gold-Standard erstellt werden.

## Anleitung

Um eine XML Datei zu inspizieren muss zunächst eine Bilddatei hochgeladen werden. \
Dazu klicken Sie auf den Button "open Image". Um jetzt die XML Datei hochzuladen klicken \
Sie auf den Button "Browse" in der oberen linken Ecke der rechten Bildschirmhälfte. \
\
Nun sollten die vom AbbyyReader erkannten Blöcke auf der linken Bildschirmhälfte eingezeichnet \
worden sein. Die Bedeutung der Farbe der Umrandung der Blöcke kann der Legende oben rechts \
entnommen werden. Sie können jetzt auf einen dieser Blöcke klicken, um dessen XML Beschreibung auf \
der rechten Bildschirmhälfte anzuzeigen. Um den erkannten Text anzuzeigen, wechseln Sie auf \
der rechten Bildschirmhäflte zu dem Reiter "text". Genauere Informationen zur Erkennung eines \
Buchstaben werden angezeigt, wenn Sie den Mauszeiger über einen Buchstaben bewegen. \
\
Um die Annotierfunktion zu nutzten wechseln Sie auf der rechten Bildschirmhälfte zu dem Reiter \
"gold". Durch das anklicken der Böcke wird der jeweilige Block zum gold-Standard hinzugefügt \
oder, falls er schon vorhanden ist, wieder entfernt. Es wird eine CSV-Datei angelegt in der \
die ersten beiden Werte die linke und obere Koordinate des jeweiligen Blockes sind und der \
dritte Wert (0|1) anzeigt ob der Block zum gold-Standard dazu gehört. Um Die erstellten Daten\
zu exportieren, markieren Sie den erstellten Text, kopieren ihn und fügen ihn anschließend in \
eine CSV-Datei ein.

unterstützte Bildformate: tif, tiff, png, jpg, jpeg
unterstützte FineReaderVersionen: 8.0
