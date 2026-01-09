import pandas as pd
import numpy as np
from functools import reduce
import math
from typing import List, Tuple, Iterable, Any

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

def get_processed_csv_2024() -> pd.DataFrame:
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

# Verbesserte Auflistung für 2d
def pretty_printing_results(resulting_array: Iterable[Iterable[Any]]) -> None:
    for row in resulting_array:
        for value in row:
            print(value, end=' ')
        print('')

# Funktionale Auflistung für Straftaten mit mehr als 2000 Vorkommnissen
def haeufigste_straftaten(straftaten_anzahl: List[Tuple[str, float]]) -> None:
    straftaten_mehr_als_2000 = list(filter(lambda row: row[1]>2000, straftaten_anzahl))
    print('\n--- 1. HÄUFIGSTE DELIKTKATEGORIEN (> 2000 FÄLLE) ---')
    pretty_printing_results(straftaten_mehr_als_2000)

# Funktionale Auflistung für totale Delikte pro Altergruppe
def totale_delikte(totale_anzahl_delikte_pro_altersgruppe: List[Tuple[str, float]]) -> float:
    totale_anzahl_delikte = reduce(lambda acc, tup: tup[1]+acc , totale_anzahl_delikte_pro_altersgruppe, 0)
    print(f'\n--- 2. GESAMTZAHL ALLER ERFASSTEN STRAFTATEN --- \n {totale_anzahl_delikte}')
    return totale_anzahl_delikte

# Funktionale Auflistung für Prozentualer Anteil der Delikte pro Altergruppe
def delikte_prozentual(
    totale_anzahl_delikte_pro_altersgruppe: List[Tuple[str, float]],
    totale_anzahl_delikte: float
) -> None:
    prozentualer_anteil_delikte = list(map(lambda tup: (tup[0], str(round(tup[1]/totale_anzahl_delikte*100, 2))+'%'), totale_anzahl_delikte_pro_altersgruppe))
    print("\n--- 3. PROZENTUALE VERTEILUNG DER BESCHULDIGTEN NACH ALTERSGRUPPEN ---")
    pretty_printing_results(prozentualer_anteil_delikte)

# Funktionale Auflistung für Ratio bei Delikten von Mann und Frau. Aufgelistet werden die Ausreisser.
def delikte_maenner_frauen(delikte_mann_frau: List[Tuple[str, float, float]]) -> None:
    delikte_anz_mann_pro_frau = list(map(lambda tup: (tup[0], round(tup[1]/tup[2], 5)), delikte_mann_frau))
    ratios_sorted = sorted(delikte_anz_mann_pro_frau, key=lambda x: (x[1] is None, x[1]), reverse=True)
    print('\n--- 4. EXTREMWERTE IM GESCHLECHTERVERHÄLTNIS (MÄNNER PRO FRAU) ---')
    print(f'\nThe least women are in the category {ratios_sorted[0]}, and the most are in {ratios_sorted[-1]}')

# Funktionale Auflistung für Ratio bei Delikten von Mann und Frau. Aufgelistet werden die Ausreisser.
def delikte_total_schweizer_und_auslaender(delikte_schweizer_und_auslaender: List[Tuple[str, float, float]]) -> None:
    delikte_total_schweizer_auslaender = reduce(lambda acc, tup: [acc[0]+tup[1], acc[1]+tup[2]], delikte_schweizer_und_auslaender, [0,0])
    ratio = round(delikte_total_schweizer_auslaender[0]/delikte_total_schweizer_auslaender[1],2)
    print('\n--- 5. VERHÄLTNIS DER STRAFTATEN NACH HERKUNFT (SCHWEIZ VS. AUSLAND) ---')
    print(f"\nSchweizer {delikte_total_schweizer_auslaender[0]} und Ausländer: {delikte_total_schweizer_auslaender[1]} | Ratio: {ratio}")


def main() -> None:
    df_2024 = get_processed_csv_2024()

    straftaten_anzahl = list(df_2024['Straftaten'].to_dict().items())
    haeufigste_straftaten(straftaten_anzahl)

    totale_anzahl_delikte_pro_altersgruppe = list(df_2024[['<10', '10-14', '15-17', '18, 19','20-24', '25-29', '30-34', '35-39', '40-49', '50-59', '60-69', '70+']].sum().to_dict().items())
    totale_anzahl_delikte = totale_delikte(totale_anzahl_delikte_pro_altersgruppe) 

    # Wir nutzen totale_anzahl_delikte von zuvor, um den prozentualen Anteil auszurechnen. String formatting findet auch gleich in der lambda Funktion statt.
    delikte_prozentual(totale_anzahl_delikte_pro_altersgruppe, totale_anzahl_delikte)

    delikte_mann_frau = list(df_2024[['männlich', 'weiblich']].itertuples(name=None))
    delikte_mann_frau = list(filter(lambda tup: tup[2] != 0 and not math.isnan(tup[2]), delikte_mann_frau))
    delikte_maenner_frauen(delikte_mann_frau)

    df_einwohner = df_2024[['Ständige Wohnbev.', 'Asyl-Bevölkerung', 'Übrige Ausländer']].dropna()
    df_einwohner['Summe_Asyl_Ausländer'] = df_einwohner[['Asyl-Bevölkerung', 'Übrige Ausländer']].sum(axis=1)
    delikte_schweizer_und_auslaender = list(df_einwohner.drop(columns=['Asyl-Bevölkerung', 'Übrige Ausländer']).itertuples(name=None))
    delikte_total_schweizer_und_auslaender(delikte_schweizer_und_auslaender)


if __name__ == '__main__':
    main()
