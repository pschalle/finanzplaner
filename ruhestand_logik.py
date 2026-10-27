def berechne_verlauf(vermoegen, rendite, sparrate, jahre):
    verlauf = []
    verlauf.append(vermoegen)
    kapital = vermoegen
    for jahr in range(1, jahre + 1):
        kapital = kapital * (1+rendite)+ 12 * sparrate  # K_t = K_(t-1) * (1 + r) + 12 * S
        verlauf.append(kapital)

    return verlauf

def fruehestes_rentenalter(aktuelles_alter, vermoegen, zielvermoegen, rendite, sparrate):
    cash_assets = vermoegen
    jahre_bis_ziel = 0
    while cash_assets < zielvermoegen and jahre_bis_ziel + aktuelles_alter < 100:
        cash_assets = cash_assets * (1 + rendite) + 12 * sparrate
        jahre_bis_ziel += 1

    frueheste_rentenalter = aktuelles_alter + jahre_bis_ziel

    # Unterscheiden, warum die Schleife geendet hat
    if cash_assets >= zielvermoegen:
        return frueheste_rentenalter

    else:
        return None

def zusaetzliche_sparrate(luecke, rendite, n):

    if n == 0:
        return None

    elif rendite == 0:
        # Ohne Zinsen: Lücke gleichmäßig auf Jahre und Monate verteilen
        zusaetzliche_sparrate_pro_monat = (luecke / n) / 12
        return zusaetzliche_sparrate_pro_monat

    else:
        # Pro Jahr: Lücke * r / ((1 + r)^n - 1), danach / 12 für pro Monat
        zusaetzliche_sparrate_pro_monat = (luecke * rendite / ((1 + rendite) ** n - 1)) / 12
        return zusaetzliche_sparrate_pro_monat

