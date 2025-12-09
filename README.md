# modi-operandi-accused
Projekttitel:
Digitale Kriminalität: Modi Operandi der digitalen Kriminalität und beschuldigte Personen
 
Ausgangssituation / Problembeschreibung:
Die digitale Kriminalität steigt in den letzten Jahren eindrücklich. Mit diesem Projekt analysieren wir genauer beschuldigte Personen von digitalen Straftaten und ihre Arbeitsweise.

Obwohl die absoluten Zahlen der digitalen Kriminalität bekannt sind, fehlt es an einer direkten, effizienten Aufschlüsselung der Täterprofile. Die rohen BFS-Daten sind für Analysten, die schnell wissen müssen, ob Phishing eher von einer bestimmten Altersgruppe oder von Personen mit spezifischem Aufenthaltsstatus begangen wird, zu grob.  
Datengrundlage:
Die Datengrundlage ist die Tabelle "Modi Operandi der digitalen Kriminalität und beschuldigte Personen" des BFS.

1. Dimension: Die Liste der Modi Operandi (Kriminalitätskategorien). Die Hauptkategorien werden in Unterkategorien aufgegliedert.

2. Dimension: Die statistische Aufschlüsselung pro Kategorie: Anzahl Fälle, Total beschuldigte Personen, Aufschlüsselung nach 10 Altersgruppen, Geschlecht (m/w/unbekannt) und Aufenthaltsstatus (z.B. CH, Ständige Ausländer).


Produktfunktionen:
Das Programm generiert Berichte, indem es Filter-, Map- und Reduce-Operationen auf die Liste der Kriminalitätskategorien anwendet.
filterSevereOffenses(minCases): Filtert alle Deliktkategorien heraus, deren Anzahl der Straftaten einer bestimmten Fallzahl (z.B. > 500) überschreitet, um sich auf die häufigsten Delikte zu konzentrieren. 
mapCalculateYouthShare(): Berechnet für jede Deliktskategorie den Gesamtanteil der unter 25-Jährigen (Summe der Altersgruppen 10-14, 15-19, 20-24) und fügt diesen Wert als neue Kennzahl hinzu. 
filterByHighYouthInvolvement(minPercentage): Filtert (basierend auf dem Ergebnis von Map 2) die Delikte, bei denen der Anteil der unter 25-Jährigen über einem definierten Prozentsatz (z.B. 60%) liegt.
reduceOffensesByHighMaleShare(): Reduziert die Liste auf Delikte mit einem Geschlechterverhältnis (Männer zu Frauen) über 10:1, um männlich dominierte Tatbereiche zu identifizieren. 
reduceSumByAgeGroup(ageGroup): Berechnet die Gesamtzahl der Beschuldigten für eine bestimmte Altersgruppe (z.B. 40-49) über alle gefilterten Deliktkategorien hinweg. 
mapNormalizeSwissRatio(): Berechnet den Anteil beschuldigter Schweizer Bürger pro Delikt. 
reduceTotalCasesOverTime(startYear, endYear): Berechnet die Gesamtzahl der Straftaten für jedes Jahr im gegebenen Zeitraum (2020 bis 2024). Das Ergebnis ist eine Liste von Jahres-Summen, die die Entwicklung der digitalen Kriminalität visualisiert und die Veränderung zum Vorjahr vergleicht.
Technologien:
Programmiersprache: Python
Frameworks: -
UI: Output auf die Konsole mit integrierten Mitteln
Art der Applikation: Konsolenapplikation
Funktionale Elemente: Datensatz (Download)
Output:
Formatierter Output auf die Konsole

Machen Sie ein konkretes Beispiel / Mockup.

================================================== 
PROJEKTARBEIT M323
================================================== 
DATUM: 2025-12-02 
SCHWERPUNKT: Digitale Kriminalität - Demografie der Beschuldigten ----------------------------------------------------------------------------------

---------------------------------------------- 
1. ZEITLICHE ENTWICKLUNG DER GESAMTZAHL STRAFTATEN (Funktion 7) -------------------------------------------------- 
Vergleich der Gesamtfallzahlen der Digitalen Kriminalität (Summe aller Delikte). Jahr | Gesamtzahl Straftaten (Summe) | Veränderung zum Vorjahr -------|-----------|--------------------|------------------------ 
2020 | 12'500 | - 
2021 | 15'300 | + 22.4%
2022 | 18'981 | + 24.1%
2023 | 22'100 | + 16.4%
2024 | 24'500 | + 10.9% 
BEOBACHTUNGEN: 

 -------------------------------------------------- 
2. HÖCHSTE RELATIVE BETEILIGUNG DER SCHWEIZER (Funktion 6) -------------------------------------------------- 
Diese Liste zeigt den Anteil beschuldigter Schweizer Bürger pro Delikt (Top 5 nach Anteil): 
Deliktkategorie | Anteil Schweizer Bürger 
Hacking | XY%
Cyberstalking | XY%
Malware | XY%
Grooming | XY%
Phishing | XY%

 -------------------------------------------------- 
3. MÄNNLICH DOMINIERT (Funktion 4) 
-------------------------------------------------- 
Delikte mit Geschlechterverhältnis (M:W) über 10:1: 
- Hacking (Verhältnis: ca. X:Y)
- Malware (Verhältnis: ca.  X:Y) ================================================== 


Projektgruppe
Dominé Célia, Bülk Anna-Maria
Unterschrift /
Abnahme
Lehrperson
Dieter Kopp

_________________________
Teammitglieder
Ihre Namen

__________________________________


# modi-operandi-accused
