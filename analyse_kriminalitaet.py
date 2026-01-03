import pandas as pd
import numpy as np
from functools import reduce
import math

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

# Einlesen der Daten
def get_processed_csv_2024():
    df_2024 = pd.read_csv("data/data_2024.csv", skiprows=3, index_col=0, skipfooter=8, engine='python')
    df_2024.columns = ['Straftaten', 'Aufgeklärte_Sraftaten', 'Aufklärungsrate in %',
        'Total beschuldigte Personen', '<10', '10-14', '15-17', '18, 19',
        '20-24', '25-29', '30-34', '35-39', '40-49', '50-59', '60-69', '70+',
        's.n.', 'männlich', 'weiblich', 'juristische Personen', 'o.A.', 'Total',
        'Ständige Wohnbev.', 'Asyl-Bevölkerung', 'Übrige Ausländer'] # Columns werden umbenannt
    df_2024.index.name = "Deliktkategorie"

    df_2024 = df_2024.drop(columns=['o.A.']) # Alle Werte in der Spalte waren 0, weshalb diese für die Analyse entfernt werden
    remove_list = ["Andere", "Darknet","Cyber Rufschädigung und unlauteres Verhalten", "Cyberbetrug", "Cyber Wirtschaftskriminalität", 'Total digitale Kriminalität'] 
    df_2024.drop(index=remove_list, inplace=True) # Entfernung der Totalen Kategoriewerte

    for column_name in df_2024.columns:
        df_2024[column_name] = df_2024[column_name].str.strip()
        df_2024[column_name] = df_2024[column_name].replace("X", np.nan) # X werden mit nan ersetzt anstatt 0, da X Werte sind, die aus Datenschutzgründen nicht gezeigt werden.
        df_2024[column_name] = df_2024[column_name].replace("", "0")
        df_2024[column_name] = df_2024[column_name].str.strip("%").str.replace("\xa0", "").str.replace(" ", "").str.replace("-", "0").astype(float) # Wegen nan wird es einfachheitshalber as float abgespeichert anstatt int
    return df_2024

# Verbesserte Auflistung fuer 2d
def pretty_printing_results(resulting_array):
    for row in resulting_array:
        for value in row:
            print(value, end=' ')
        print('')

# Funktionale und Imperative Auflistung für Straftaten mit mehr als 2000 vorkommnissen
def straftaten_functional(straftaten_anzahl):
    straftaten_mehr_als_2000_funktional = list(filter(lambda row: row[1]>2000, straftaten_anzahl))
    print('\n > 1 Resultate Funktional')
    pretty_printing_results(straftaten_mehr_als_2000_funktional)

def straftaten_imperativ(straftaten_anzahl):
    straftaten_mehr_als_2000_imperativ = []
    for row in straftaten_anzahl:
        if row[1]>2000:
            straftaten_mehr_als_2000_imperativ.append(row)
    print('\n > 1 Resultate Imperativ')
    pretty_printing_results(straftaten_mehr_als_2000_imperativ)

# Funktionale und Imperative Auflistung für totale Delikte pro Altergruppe
def totale_delikte_functional(totale_anzahl_delikte_pro_altersgruppe):
    totale_anzahl_delikte_funktional = reduce(lambda acc, tup: tup[1]+acc , totale_anzahl_delikte_pro_altersgruppe, 0)
    print(f'\n2 Totale Anzahl Delikte berechnet mit Reduce (Funktional): {totale_anzahl_delikte_funktional}')
    return totale_anzahl_delikte_funktional

def totale_delikte_imperativ(totale_anzahl_delikte_pro_altersgruppe):
    totale_anzahl_delikte_imperativ = 0
    for tup in totale_anzahl_delikte_pro_altersgruppe:
        totale_anzahl_delikte_imperativ += tup[1]
    print(f'2 Totale Anzahl Delikte berechnet mit einer for loop (Imperativ): {totale_anzahl_delikte_imperativ}')

# Funktionale und Imperative Auflistung für Prozentualer Anteil der Delikte pro Altergruppe
def percentual_delikte_functional(totale_anzahl_delikte_pro_altersgruppe, totale_anzahl_delikte_imperativ):
    prozentualer_anteil_delikte_funktional = list(map(lambda tup: (tup[0], str(round(tup[1]/totale_anzahl_delikte_imperativ*100, 2))+'%'), totale_anzahl_delikte_pro_altersgruppe))
    print("\n > 3 Funktional ausgerechneter prozentualer Anteil")
    pretty_printing_results(prozentualer_anteil_delikte_funktional)

def percentual_delikte_imperativ(totale_anzahl_delikte_pro_altersgruppe, totale_anzahl_delikte_imperativ):
    prozentualer_anteil_delikte_imperativ = []
    for tup in totale_anzahl_delikte_pro_altersgruppe:
        prozentualer_anteil_delikte_imperativ.append((tup[0], str(round(tup[1]/totale_anzahl_delikte_imperativ*100, 2))+'%'))
    print("\n > 3 Imperativ ausgerechneter prozentualer Anteil")
    pretty_printing_results(prozentualer_anteil_delikte_imperativ)


# Funktionale und Imperative Auflistung für Ratio bei Delikten von Mann und Frau. Aufgelistet werden die Ausreisser.
def delikte_men_women_functional(delikte_mann_frau):
    delikte_anz_mann_pro_frau_funktional = list(map(lambda tup: (tup[0], round(tup[1]/tup[2], 5)), delikte_mann_frau))

    ratios_sorted = sorted(delikte_anz_mann_pro_frau_funktional, key=lambda x: (x[1] is None, x[1]), reverse=True)
    print(f'\n4 Funktional: The least woman are in the category {ratios_sorted[0]}, and the most are in {ratios_sorted[-1]}')

def delikte_men_women_imperative(delikte_mann_frau):
    delikte_anz_mann_pro_frau_imperativ = []
    for tup in delikte_mann_frau:
        ratio = tup[1]/tup[2]
        delikte_anz_mann_pro_frau_imperativ.append((tup[0], round(ratio, 5)))

    ratios_sorted = sorted(delikte_anz_mann_pro_frau_imperativ, key=lambda x: (x[1] is None, x[1]), reverse=True)
    print(f'4 Imperativ: The least woman are in the category {ratios_sorted[0]}, and the most are in {ratios_sorted[-1]}')


# Funktionale und Imperative Auflistung, was die Ratio zwischen Schweizer und Ausländer Delikte sind
def delikte_total_swiss_and_foreign_functional(delikte_schweizer_und_auslaender):
    delikte_total_schweizer_auslaender_funktional = reduce(lambda acc, tup: [acc[0]+tup[1], acc[1]+tup[2]], delikte_schweizer_und_auslaender, [0,0])
    ratio = round(delikte_total_schweizer_auslaender_funktional[0]/delikte_total_schweizer_auslaender_funktional[1],2)
    print(f"\n5 Funktional: Schweizer {delikte_total_schweizer_auslaender_funktional[0]} und Ausländer: {delikte_total_schweizer_auslaender_funktional[1]} | Ratio: {ratio}")

def delikte_total_swiss_and_foreign_imperativ(delikte_schweizer_und_auslaender):
    delikte_total_schweizer_auslaender_imperativ = [0,0]
    for tup in delikte_schweizer_und_auslaender:
        delikte_total_schweizer_auslaender_imperativ[0]+=tup[1]
        delikte_total_schweizer_auslaender_imperativ[1]+=tup[2]
    ratio = round(delikte_total_schweizer_auslaender_imperativ[0]/delikte_total_schweizer_auslaender_imperativ[1],2)
    print(f"5 Imperativ: Schweizer {delikte_total_schweizer_auslaender_imperativ[0]} und Ausländer: {delikte_total_schweizer_auslaender_imperativ[1]} | Ratio: {ratio}")


def main():
    df_2024 = get_processed_csv_2024()
    straftaten_anzahl = list(df_2024['Straftaten'].to_dict().items())
    straftaten_functional(straftaten_anzahl)
    straftaten_imperativ(straftaten_anzahl)

    totale_anzahl_delikte_pro_altersgruppe = list(df_2024[['<10', '10-14', '15-17', '18, 19','20-24', '25-29', '30-34', '35-39', '40-49', '50-59', '60-69', '70+']].sum().to_dict().items())
    totale_anzahl_delikte_imperativ = totale_delikte_functional(totale_anzahl_delikte_pro_altersgruppe) # Ausnahmsweise mit returnwert
    totale_delikte_imperativ(totale_anzahl_delikte_pro_altersgruppe)

    # Wir nutzen totale_anzahl_delikte_imperativ von zuvor, um den prozentualen Anteil auszurechnen. String formatting findet auch gleich in der lambda Funktion statt.
    percentual_delikte_functional(totale_anzahl_delikte_pro_altersgruppe, totale_anzahl_delikte_imperativ)
    percentual_delikte_imperativ(totale_anzahl_delikte_pro_altersgruppe, totale_anzahl_delikte_imperativ)

    delikte_mann_frau = list(df_2024[['männlich', 'weiblich']].itertuples(name=None))
    delikte_mann_frau = list(filter(lambda tup: tup[2] != 0 and not math.isnan(tup[2]), delikte_mann_frau))
    # ('Phishing', 128.0, 51.0) bedeutet, Kategorie Phishing gab es 128 Delikte von Männern und 51 von Frauen.
    delikte_men_women_functional(delikte_mann_frau)
    delikte_men_women_imperative(delikte_mann_frau)

    df_einwohner = df_2024[['Ständige Wohnbev.', 'Asyl-Bevölkerung', 'Übrige Ausländer']].dropna()
    df_einwohner['Summe_Asyl_Ausländer'] = df_einwohner[['Asyl-Bevölkerung', 'Übrige Ausländer']].sum(axis=1)
    delikte_schweizer_und_auslaender = list(df_einwohner.drop(columns=['Asyl-Bevölkerung', 'Übrige Ausländer']).itertuples(name=None))
    # ('Phishing', 112.0, 67.0) bedeutet, Kategorie Phishing gab es 112 Delikte von Schweizern und 67 von Ausländer/Asylanten.
    delikte_total_swiss_and_foreign_functional(delikte_schweizer_und_auslaender)
    delikte_total_swiss_and_foreign_imperativ(delikte_schweizer_und_auslaender)

if __name__ == '__main__':
    main()
