
## Digitale Kriminalität: Modi Operandi der digitalen Kriminalität und beschuldigte Personen
 
### Ausgangssituation / Problembeschreibung:
Die digitale Kriminalität steigt in den letzten Jahren eindrücklich. Mit diesem Projekt analysieren wir genauer beschuldigte Personen von digitalen Straftaten und ihre Arbeitsweise.

Obwohl die absoluten Zahlen der digitalen Kriminalität bekannt sind, fehlt es an einer direkten, effizienten Aufschlüsselung der Täterprofile. Die rohen BFS-Daten sind für Analysten, die schnell wissen müssen, ob Phishing eher von einer bestimmten Altersgruppe oder von Personen mit spezifischem Aufenthaltsstatus begangen wird, zu grob.  

  
### Datengrundlage:
Die Datengrundlage ist die Tabelle "Modi Operandi der digitalen Kriminalität und beschuldigte Personen" des BFS.

1. Dimension: Die Liste der Modi Operandi (Kriminalitätskategorien). Die Hauptkategorien werden in Unterkategorien aufgegliedert.

2. Dimension: Die statistische Aufschlüsselung pro Kategorie: Anzahl Fälle, Total beschuldigte Personen, Aufschlüsselung nach 10 Altersgruppen, Geschlecht (m/w/unbekannt) und Aufenthaltsstatus (z.B. CH, Ständige Ausländer).


### Produktfunktionen: 
Das Programm generiert Berichte, indem es Filter-, Map- und Reduce-Operationen auf die Liste der Kriminalitätskategorien anwendet.

#### straftaten_functional / straftaten_imperativ

Filtert alle Deliktkategorien heraus, deren Anzahl der Straftaten mehr als 2000 beträgt.

Ziel:
Fokussierung auf die häufigsten Deliktfelder.


#### totale_delikte_functional / totale_delikte_imperativ

Berechnet die Gesamtsumme der Straftaten über alle Altersgruppen hinweg mittels reduce.

Ziel:
Ermittlung der Gesamtbelastung je Altersgruppe.


#### percentual_delikte_functional / percentual_delikte_functional_imperativ

Berechnet den prozentualen Anteil der Delikte pro Altersgruppe.

Ziel:
Vergleich der Verteilung der Straftaten auf Altersgruppen.


#### delikte_men_women_functional / delikte_men_women_imperative

Berechnet für jede Deliktkategorie das Verhältnis Männer zu Frauen.

Ziel:
Erkennung stark männlich vs weiblich dominierter Deliktfelder.


#### delikte_total_swiss_and_foreign_functional / delikte_total_swiss_and_foreign_imperative

Berechnet die Gesamtzahl der Straftaten von Schweizern im Vergleich zu Ausländern/Asylbewerbern.

Ziel:
Analyse der Deliktverteilung nach Staatsangehörigkeit.


### Technologien:
**Programmiersprache:** Python  
**UI:** Output auf die Konsole mit integrierten Mitteln  
**Art der Applikation:** Konsolenapplikation  
**Funktionale Elemente:** Lambda-Funktionen, map, reduce, filter
**Output:**  
1 Resultate Funktional
Phishing 5930.0 
davon: Kleinanzeigeplattformen – Ware nicht geliefert 10625.0 
davon: Missbrauch von Online-Zahlungssyst./Wertkarten oder einer fremden Identität, um einen Betrug zu begehen 22293.0 
davon: Online Anlagebetrug 2974.0 
Money/Package Mules 3757.0 
Cyber Sexualdelikte 2922.0 
Verbotene Pornografie 2705.0 

1 Resultate Imperativ
Phishing 5930.0 
davon: Kleinanzeigeplattformen – Ware nicht geliefert 10625.0 
davon: Missbrauch von Online-Zahlungssyst./Wertkarten oder einer fremden Identität, um einen Betrug zu begehen 22293.0 
davon: Online Anlagebetrug 2974.0 
Money/Package Mules 3757.0 
Cyber Sexualdelikte 2922.0 
Verbotene Pornografie 2705.0 

2 Totale Anzahl Delikte berechnet mit Reduce (Funktional): 8711.0
2 Totale Anzahl Delikte berechnet mit einer for loop (Imperativ): 8711.0

3 Funktional ausgerechneter prozentualer Anteil
<10 0.41%
10-14 11.26%
15-17 12.64%
18, 19 6.52%
20-24 11.8%
25-29 9.48%
30-34 8.68%
35-39 8.06%
40-49 12.54%
50-59 10.04%
60-69 5.68%
70+ 2.88%

3 Imperativ ausgerechneter prozentualer Anteil
<10 0.41%
10-14 11.26%
15-17 12.64%
18, 19 6.52%
20-24 11.8%
25-29 9.48%
30-34 8.68%
35-39 8.06%
40-49 12.54%
50-59 10.04%
60-69 5.68%
70+ 2.88%

4 Funktional: The least women are in the category ('Grooming', 11.83333), and the most are in ('Malware – Rogueware/Scareware', 1.25)
4 Imperativ: The least women are in the category ('Grooming', 11.83333), and the most are in ('Malware – Rogueware/Scareware', 1.25)

5 Funktional: Schweizer 7401.0 und Ausländer: 1314.0 | Ratio: 5.63
5 Imperativ: Schweizer 7401.0 und Ausländer: 1314.0 | Ratio: 5.63