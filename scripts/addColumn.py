import pandas as pd


def add_incrementing_column(file_path, output_path):
    # CSV-Datei einlesen
    df = pd.read_csv("C:\\Users\\jan\\Desktop\\WP Stores\\Store_CA Überarbeitet.csv")


    # Überprüfen, ob eine ID-Spalte existiert, wenn nicht, erstellen
    if 'ID' not in df.columns:
        df.insert(len(df.columns), 'ID', range(1, len(df) + 1))
    else:
       # df['ID'] = df['ID'] + 1
        df.insert(len(df.columns), 'New_Column', df['ID'] + 1)


    # Aktualisierte CSV speichern
    df.to_csv(output_path, index=False)
    print(f"Datei wurde erfolgreich aktualisiert und gespeichert unter: {output_path}")


# Beispielaufruf
eingabe_datei = 'Store_CA Überarbeitet'  # Ersetze dies mit dem tatsächlichen Dateipfad
ausgabe_datei = 'output.csv'
add_incrementing_column(eingabe_datei, ausgabe_datei)
