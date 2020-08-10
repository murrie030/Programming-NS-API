___name__ = 'NS_API_v3'

import requests
import xmltodict

auth_details = ('rafael.milia@student.hu.nl', 'hUa9Z7yk919i1VVQVsRO7uCclKYixkBIP7yosvccztUYlijuGd5iWg')

def stationslijst_ophalen():
    """Checkt of er een xml met stations bestaat en zo niet, dan haalt ie deze op via de NS API"""
    try:
        with open('stationslijst.xml', 'r') as file:
            stationsxml = xmltodict.parse(file.read())
        print('Stationslijst geopend.')
    except:
        print('Stationslijst niet gevonden, wordt binnengehaald.')
        # xml gegevens to dict
        api_url = 'http://webservices.ns.nl/ns-api-stations-v2?_ga=2.244245893.1804166528.1539937355-205946361.1539937355'
        response = requests.get(api_url, auth=auth_details)
        stationsxmlstring = response.text
        stationsxml = xmltodict.parse(stationsxmlstring)
        with open('stationslijst.xml', 'wb') as file:
            file.write(stationsxmlstring.encode('utf-8'))
        print('De stationslijst is binnengehaald!')
    return stationsxml


def stationscode(ingevoerd_station):
    """Deze functie haalt de stationscode op aan de hand van de stationsnaam, en voert de code in op de ophaalfunctie"""
    code = ''
    if ingevoerd_station == '':
        print('Voer een geldige stationsnaam in.')

    # vragen om invoer
    stationsxml = stationslijst_ophalen()
    # doorloopen opzoek naar naam
    for stations in stationsxml['Stations']['Station']:
        # zoeken in de namen
        if ingevoerd_station == stations['Namen']['Kort'] or ingevoerd_station == stations['Namen']['Middel'] or ingevoerd_station == stations['Namen']['Lang']:
            code = stations['Code']
            break
        # zoeken in de synoniemen
        elif stations['Synoniemen'] is not None:
            synoniemen_list = stations['Synoniemen']['Synoniem']
            if ingevoerd_station in synoniemen_list:
                code = stations['Code']
                break
    return vertrektijden_ophalen(code)


def vertrektijden_ophalen(code):
    """Deze functie haalt de vertrektijden op aan de hand van de stationscode en return deze als lijst"""
# inloggen
    api_url = 'http://webservices.ns.nl/ns-api-avt?station={}'.format(code)
# response in variabele
    response = requests.get(api_url, auth=auth_details)
# parsen
    vertrekxml = xmltodict.parse(response.text)
    try:
        vertrek_overzicht_list = []
        for vertrek in vertrekxml['ActueleVertrekTijden']['VertrekkendeTrein']:

            # vertrektijd in isoleren aan de hand van indexen op de string
            vertrektijd = vertrek['VertrekTijd']      # 2016-09-27T18:36:00+0200
            vertrektijd = vertrektijd[11:16]          # 18:36

            # soms is er geen vertrekspoor beschikbaar omdat er bussen worden in gezet ipv treinen
            # daarom moet er eerst gecheckt worden óf er wel een vertrekspoor is
            # zo niet moet gemeld worden dat er geen trein vertrekt
            try:
                vertrek_overzicht_list.append('Om {} vertrekt van spoor {} een {} naar {}.'.format(vertrektijd, vertrek['VertrekSpoor']['#text'], vertrek['TreinSoort'], vertrek['EindBestemming']))
                if vertrek['VertrekSpoor']['@wijziging'] == 'True':
                    vertrek_overzicht_list.append('Let op! Dit is een gewijzigd vertrek spoor!')
            except KeyError:
                vertrek_overzicht_list.append('Om {} vertrekt er een {} naar {}'.format(vertrektijd, vertrek['TreinSoort'], vertrek['EindBestemming']))
        return vertrek_overzicht_list
    except:
        return ['Ingevoerde naam is niet gevonden.', 'Controleer de spelling.']