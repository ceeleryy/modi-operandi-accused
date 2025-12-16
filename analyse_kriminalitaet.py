import csv
from pathlib import Path
# from functools import reduce # NICHT VERWENDET FÜR V1.0 (Imperativ)
import time 

# --- DEFINITION DER EXAKTEN SCHLÜSSEL AUS DER CSV ---
KEY_DELIKT = 'Modi operandi1)'
KEY_STRAFTATEN = 'Straftaten2)'
KEY_TOTAL_BESCHULDIGTE = 'Total beschuldigte Personen'
KEY_ALTER_10_14 = '10-14'
KEY_ALTER_15_17 = '15-17'
KEY_ALTER_18_19_RAW = '18, 19'
KEY_ALTER_20_24 = '20-24'
KEY_MAENNLICH = 'männlich'
KEY_WEIBLICH = 'weiblich'
KEY_CH = 'Ständige Wohnbev.' 
KEY_JAHR = 'Jahr'


# --- HILFSFUNKTIONEN (BEREINIGUNG & FORMATIERUNG) ---

def bereinige_schluessel(schluessel):
    """Bereinigt den Schlüssel von Leerzeichen, Kommas und Zeilenumbrüchen."""
    if isinstance(schluessel, str):
        return schluessel.strip().replace(',', ' ').replace('\n', ' ').replace('\r', '').replace('\xa0', ' ').strip()
    return schluessel

def format_number(n):
    """Formatiert eine Zahl mit Tausender-Trennzeichen (z.B. 12'500)"""
    return f"{n:,.0f}".replace(",", "'")


# --- 1. DATENLADEN ---

def lade_csv_daten(dateipfad_str, jahr=None):
    """
    Lädt die CSV-Datei und konvertiert Zahlen in Integer. 
    """
    daten_liste = []
    dateipfad = Path(dateipfad_str)
    
    if not dateipfad.exists():
        return []

    try:
        with open(dateipfad, mode='r', encoding='utf-8') as datei:
            inhalt = datei.read()
            delimiter = ',' if inhalt.count(',') > inhalt.count(';') else ';'
            datei.seek(0)
            
            # Überspringe die ersten 3 Metadaten-Zeilen damit es klappt
            next(datei) 
            next(datei) 
            next(datei) 
            
            csv_reader = csv.DictReader(datei, delimiter=delimiter)
            
            for zeile in csv_reader:
                bereinigte_daten = {}
                for schluessel, wert in zeile.items():
                    bereinigter_schluessel = bereinige_schluessel(schluessel)
                    if isinstance(wert, str) and wert.strip().upper() in ('X', '', 'NULL', '-'):
                        bereinigte_daten[bereinigter_schluessel] = 0
                    else:
                        try:
                            sauberer_wert = str(wert).replace('.', '').replace(',', '').replace('\xa0', '').strip()
                            bereinigte_daten[bereinigter_schluessel] = int(sauberer_wert) 
                        except ValueError:
                            bereinigte_daten[bereinigter_schluessel] = wert
                
                if jahr:
                    bereinigte_daten[KEY_JAHR] = jahr
                
                delikt_name = bereinigte_daten.get(bereinige_schluessel(KEY_DELIKT))
                if delikt_name and not delikt_name.startswith('Total') and delikt_name != bereinige_schluessel(KEY_DELIKT):
                    daten_liste.append(bereinigte_daten)
                    
    except Exception as e:
        return []
        
    return daten_liste


# ----------------------------------------------------------------------------------
# DIE 7 FUNKTIONEN (MAP / FILTER / REDUCE)
# ----------------------------------------------------------------------------------

# 1. FILTER: filterSevereOffenses(minCases) - Imperativ
def filterSevereOffenses(delikte_liste, minCases):
    resultierende_delikte = []
    key = bereinige_schluessel(KEY_STRAFTATEN) 
    for delikt in delikte_liste:
        if delikt.get(key, 0) > minCases:
            resultierende_delikte.append(delikt)
    return resultierende_delikte


# 2. MAP: mapCalculateYouthShare() - Imperativ
def mapCalculateYouthShare(delikte_liste):
    ergebnis_liste = []
    key_total = bereinige_schluessel(KEY_TOTAL_BESCHULDIGTE)
    key_a1 = bereinige_schluessel(KEY_ALTER_10_14)
    key_a2 = bereinige_schluessel(KEY_ALTER_15_17)
    key_a3 = bereinige_schluessel(KEY_ALTER_18_19_RAW)
    key_a4 = bereinige_schluessel(KEY_ALTER_20_24)

    for delikt in delikte_liste:
        jugend_summe = (
            delikt.get(key_a1, 0) + delikt.get(key_a2, 0) + 
            delikt.get(key_a3, 0) + delikt.get(key_a4, 0)   
        )
        gesamt_beschuldigte = delikt.get(key_total, 0) 
        
        if gesamt_beschuldigte > 0:
            jugend_anteil = (jugend_summe / gesamt_beschuldigte) * 100
        else:
            jugend_anteil = 0.0
        
        delikt['Jugendanteil_Prozent'] = round(jugend_anteil, 2)
        ergebnis_liste.append(delikt)
        
    return ergebnis_liste


# 3. FILTER: filterByHighYouthInvolvement(minPercentage) - Imperativ
def filterByHighYouthInvolvement(delikte_liste, minPercentage):
    delikte_mit_hohem_jugendanteil = []
    for delikt in delikte_liste:
        if delikt.get('Jugendanteil_Prozent', 0.0) > minPercentage:
            delikte_mit_hohem_jugendanteil.append(delikt)
    return delikte_mit_hohem_jugendanteil


# 4. REDUCE/FILTER: reduceOffensesByHighMaleShare() - Imperativ
def reduceOffensesByHighMaleShare(delikte_liste, minRatio=10.0):
    delikte_maennlich_dominiert = []
    key_maenner = bereinige_schluessel(KEY_MAENNLICH)
    key_frauen = bereinige_schluessel(KEY_WEIBLICH)

    for delikt in delikte_liste:
        maenner = delikt.get(key_maenner, 0)
        frauen = delikt.get(key_frauen, 0)
        
        if frauen == 0:
            if maenner > 0: 
                 delikte_maennlich_dominiert.append(delikt)
            continue
            
        verhaeltnis = maenner / frauen
        
        if verhaeltnis > minRatio:
            delikte_maennlich_dominiert.append(delikt)
            
    return delikte_maennlich_dominiert


# 5. REDUCE: reduceSumByAgeGroup(ageGroup) - Imperativ
def reduceSumByAgeGroup(delikte_liste, ageGroupKey):
    gesamt_summe = 0
    key = bereinige_schluessel(ageGroupKey)
    
    for delikt in delikte_liste:
        gesamt_summe += delikt.get(key, 0)
        
    return gesamt_summe


# 6. MAP: mapNormalizeSwissRatio() - Imperativ
def mapNormalizeSwissRatio(delikte_liste):
    ergebnis_liste = []
    key_total = bereinige_schluessel(KEY_TOTAL_BESCHULDIGTE)
    key_ch = bereinige_schluessel(KEY_CH)
    
    for delikt in delikte_liste:
        total = delikt.get(key_total, 0)
        ch_anteil = delikt.get(key_ch, 0)
        
        anteil_prozent = (ch_anteil / total) * 100 if total > 0 else 0.0
        
        delikt['Schweizer_Anteil_Prozent'] = round(anteil_prozent, 2)
        ergebnis_liste.append(delikt)
        
    return ergebnis_liste


# 7. REDUCE: reduceTotalCasesOverTime(startYear, endYear) - Imperativ
def reduceTotalCasesOverTime(alle_daten):
    jahres_summen = {}
    
    # 1. Sammle Summen pro Jahr
    for delikt in alle_daten:
        jahr = delikt.get(KEY_JAHR)
        straftaten = delikt.get(bereinige_schluessel(KEY_STRAFTATEN), 0)
        
        if jahr:
            if jahr in jahres_summen:
                jahres_summen[jahr] += straftaten
            else:
                jahres_summen[jahr] = straftaten
            
    # 2. Sortiere und berechne die prozentuale Veränderung
    sorted_years = sorted(jahres_summen.keys())
    ergebnis_liste = []
    
    letzte_summe = 0
    for jahr in sorted_years:
        aktuelle_summe = jahres_summen[jahr]
        
        if letzte_summe > 0:
            veraenderung = ((aktuelle_summe - letzte_summe) / letzte_summe) * 100
            veraenderung_str = f"+ {veraenderung:.1f}%" if veraenderung > 0 else f"{veraenderung:.1f}%"
        else:
            veraenderung_str = "-"
            
        ergebnis_liste.append({
            KEY_JAHR: jahr, 
            'Gesamtzahl Straftaten': aktuelle_summe, 
            'Veränderung zum Vorjahr': veraenderung_str
        })
        letzte_summe = aktuelle_summe
        
    return ergebnis_liste


# ----------------------------------------------------------------------------------
# HAUPT-REPORT-FUNKTION (Imperativ)
# ----------------------------------------------------------------------------------

def generate_report(daten_2024, daten_gesamt):
    
    # --------------------------------------------------
    # 1. ZEITLICHE ENTWICKLUNG (F7)
    # --------------------------------------------------
    
    zeit_entwicklung = reduceTotalCasesOverTime(daten_gesamt)
    
    report_output = "\n==================================================\n"
    report_output += "PROJEKTARBEIT M323\n"
    report_output += "==================================================\n"
    report_output += f"DATUM: {time.strftime('%Y-%m-%d')}\n" 
    report_output += "SCHWERPUNKT: Digitale Kriminalität - Demografie der Beschuldigten \n"
    report_output += "----------------------------------------------------------------------------------\n"
    
    report_output += "\n----------------------------------------------"
    report_output += "\n1. ZEITLICHE ENTWICKLUNG DER GESAMTZAHL STRAFTATEN (Funktion 7)"
    report_output += "\n--------------------------------------------------"
    report_output += "\nVergleich der Gesamtfallzahlen der Digitalen Kriminalität (Summe aller Delikte)."
    report_output += "\nJahr | Gesamtzahl Straftaten (Summe) | Veränderung zum Vorjahr"
    report_output += "\n-----|-------------------------------|------------------------"
    
    for jahr_daten in zeit_entwicklung:
        jahr = jahr_daten.get(KEY_JAHR)
        summe = format_number(jahr_daten.get('Gesamtzahl Straftaten'))
        veraenderung = jahr_daten.get('Veränderung zum Vorjahr')
        
        report_output += f"\n{jahr:<4} | {summe:>27} | {veraenderung:>22}"

    report_output += "\nBEOBACHTUNGEN: Die Fallzahlen sind über den gesamten Zeitraum signifikant gestiegen."
    
    # --------------------------------------------------
    # 2. HÖCHSTE RELATIVE BETEILIGUNG DER SCHWEIZER (F6)
    # --------------------------------------------------
    
    daten_mit_ch_anteil = mapNormalizeSwissRatio(daten_2024[:]) 
    
    # Imperatives Sortieren und Top 5 auswählen
    top_schweizer = sorted(
        daten_mit_ch_anteil, 
        key=lambda x: x.get('Schweizer_Anteil_Prozent', 0), 
        reverse=True
    )
    top_schweizer_5 = top_schweizer[:5]
    
    report_output += "\n\n----------------------------------------------"
    report_output += "\n2. HÖCHSTE RELATIVE BETEILIGUNG DER SCHWEIZER (Funktion 6)"
    report_output += "\n--------------------------------------------------"
    report_output += "\nDiese Liste zeigt den Anteil beschuldigter Schweizer Bürger pro Delikt (Top 5 nach Anteil):"
    report_output += "\nDeliktkategorie                          | Anteil Schweizer Bürger"
    report_output += "\n-----------------------------------------|------------------------"
    
    for delikt in top_schweizer_5:
        delikt_name = delikt.get(bereinige_schluessel(KEY_DELIKT), 'N/A')
        anteil = f"{delikt.get('Schweizer_Anteil_Prozent', 0.0):.1f}%"
        report_output += f"\n{delikt_name:<40} | {anteil:>22}"

    # --------------------------------------------------
    # 3. MÄNNLICH DOMINIERT (F4)
    # --------------------------------------------------
    
    maennlich_dominiert_delikte = reduceOffensesByHighMaleShare(daten_2024[:])
    
    report_output += "\n\n----------------------------------------------"
    report_output += "\n3. MÄNNLICH DOMINIERT (Funktion 4)"
    report_output += "\n--------------------------------------------------"
    report_output += "\nDelikte mit Geschlechterverhältnis (M:W) über 10:1:"
    
    key_maenner = bereinige_schluessel(KEY_MAENNLICH)
    key_frauen = bereinige_schluessel(KEY_WEIBLICH)
    
    if not maennlich_dominiert_delikte:
        report_output += "\n- Keine Delikte gefunden, bei denen das M:W-Verhältnis > 10:1 ist."
    else:
        for delikt in maennlich_dominiert_delikte:
            maenner = delikt.get(key_maenner, 0)
            frauen = delikt.get(key_frauen, 0)
            verhaeltnis_float = round(maenner / frauen, 2) if frauen > 0 else None
            
            verhaeltnis_str = f"{verhaeltnis_float}" if verhaeltnis_float is not None else "unendlich"
            
            report_output += f"\n- {delikt.get(bereinige_schluessel(KEY_DELIKT))} (Verhältnis: {verhaeltnis_str} [{maenner} Männer / {frauen} Frauen])"

    report_output += "\n=================================================="
    return report_output


# ----------------------------------------------------------------------------------
# HAUPTTEIL ZUR AUSFÜHRUNG
# ----------------------------------------------------------------------------------

if __name__ == '__main__':
    
    print("--- Start der Kriminalitätsanalyse V1.0 (Imperativ) ---")
    
    current_script_dir = Path(__file__).parent
    
    # Laden der Daten für alle Jahre (2020-2024)
    daten_gesamt = []
    daten_2024 = []
    jahre = range(2020, 2025)
    
    # Imperative Schleife zum Laden aller Daten
    for jahr in jahre:
        # Hier müssten Sie data_2020.csv, data_2021.csv etc. im 'data/' Ordner haben
        daten_pfad = current_script_dir / "data" / f"data_{jahr}.csv"
        geladene_daten = lade_csv_daten(str(daten_pfad), jahr=jahr)
        
        if not geladene_daten:
            # Falls nur eine Datei fehlt, soll die Analyse für die anderen Jahre weiterlaufen
            print(f"FEHLER: Daten für Jahr {jahr} konnten nicht geladen werden. Wird ignoriert, wenn es nicht 2024 ist.")
        else:
            daten_gesamt.extend(geladene_daten)
            if jahr == 2024:
                daten_2024 = geladene_daten 
                
    
    if not daten_2024 or not daten_gesamt:
        print("\nFATALER FEHLER: Mindestens die Daten für 2024 oder die Gesamtdaten fehlen. ")
        print("Stellen Sie sicher, dass alle data_2020.csv bis data_2024.csv im Ordner 'data' sind.")
        print("Analyse abgebrochen.")
    else:
        print(f"Daten geladen. Gesamtanzahl Delikt-Kategorien (2024): {len(daten_2024)}")
        
        # Generierung des Reports
        final_report = generate_report(daten_2024, daten_gesamt)
        print(final_report)
        
        print("Analyse V1.0 erfolgreich abgeschlossen.")