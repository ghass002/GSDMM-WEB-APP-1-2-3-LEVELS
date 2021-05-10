# Import all libraries
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
import re
import streamlit as st
import pandas as pd
from HanTa import HanoverTagger as ht
import warnings

# Initialize the tagger tool
tagger = ht.HanoverTagger('morphmodel_ger.pgz')

# Ignore Warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

# Load the stopwords list for German langauge
stop_words_de = list(set(stopwords.words('german')))
stop_words_de.extend(['Ja','Nein','KI','Künstlicher','künsticher','Künstliche','künstiche','Intelligenz','AI','ki','kI','Ai','aI','Artifizielle','artifizielle','intelligenz','Darüber','darüber','taucto','TheCityGame','verbessern','Jahr','App','Aktivität','Auswirkung','Idee','Dokument','Datum','einschließlich','Gruppen','Gruppe','profitieren','Produkte','Produkt','Projekt','geben','mindestens','daraus','open','mögen','Aktivitäten','Projekt','euro','tiber', 'direkt','altern','erheblich','wodurch','jedoch','schließlich','lokale','Informationen','Daten','Ziel','Bürgern','bereits','Unternehmen','verschieden','theCityGame','Auswirkungen','nachhaltig','Verbraucher','lokal','Plattform','neu','neue','Menschen','Mensch','Bürger','Zielgruppe','eben','soziale','sozial','verwenden','Personen','Person','gut','bieten','Benutzer','einfach','leicht','groß','Produkt ', 'Produkte ', 'Aktie ', 'Anteile ', 'Dokument ', 'Unterlagen ', 'myevent ', 'Ziel ', 'Ziele ', 'datum ', 'Datum ', 'schließlich ', 'Vorteil ', 'benötigen ', 'erfordert ', 'Sozial ', 'Täglich ', 'verwalten ', 'verwaltet ', 'echt ', 'existieren ', 'existiert ', 'klein ', 'datum ', 'Datum ', 'benötigen ', 'erfordert ', 'zusätzlich ', 'zusätzlich ', 'niedrig ', 'absichtlich ', 'Veranstaltung ', 'Veranstaltungen ', 'Einschlag ', 'Auswirkungen ', 'App ', 'Apps ', 'erstellen ', 'Verbraucher', 'Verbraucherin', 'Verbraucher ', 'schafft ', 'Aktivität ', 'Aktivitäten ', 'Region ', 'Regionen ', 'Aktion ', 'Aktionen ', 'sich beteiligen ', 'nimmt teil ', 'Bedienung ', 'Dienstleistungen ', 'Ziel ', 'Ziele ', 'Projekt ', 'Projekte ', 'Plattform ', 'Plattformen ', 'Geschichte ', 'Geschichten ', 'Leben ', 'lebte ', 'Kunde', 'Kundin', 'Kunden ', 'Bürger', 'Bürgerin', 'Bürger ', 'Nutzer', 'Nutzerin', 'Benutzer ', 'Gruppe ', 'Gruppen ', 'Menschen ', 'Person ', 'Personen ', 'brauchen ', 'Bedürfnisse ', 'wollen ', 'will ', 'könnten ', 'geben ', 'gibt ', 'Jahr ', 'Jahre ', 'Zeit ', 'mal ', 'Situation ', 'Situationen ', 'Gruppen ', 'öffnen ', 'Ideen ', 'Unterstützung ', 'Personen ', 'öffnet ', 'unterstützt ', 'gut ', 'führen ', 'führt ', 'Werkzeug ', 'Werkzeuge ', 'Kunde', 'Kundin', 'Verbraucher', 'Verbraucherin', 'Kunden ', 'Verbraucher ', 'Datum ', 'Bürger ', 'Geräte ', 'Individuell ', 'Einzelpersonen ', 'Prozess ', 'Spieler', 'Spielerin', 'Spieler', 'Spielerinnen', 'Nutzer', 'Nutzerin', 'Benutzer ', 'Aktion ', 'Aktionen ', 'Veränderung ', 'sich beteiligen ', 'Dienstleistungen ', 'Ziel ', 'Gruppe ', 'Gemeinschaft ', 'Bürger', 'Bürgerin', 'erstellen ', 'Anwendung ', 'Leben ', 'Person ', 'verbessern ', 'Öffentlichkeit ', 'Punkt ', 'Region ', 'Dokument ', 'Einschlag ', 'Jahr ', 'datum ', 'Bedienung ', 'lokal ', 'Gruppe ', 'Niveau ', 'aktivieren ', 'Nutzer', 'Nutzerin', 'zur Verfügung stellen ', 'Problem ', 'Plattform ', 'Taucto ', 'Menschen ', 'Projekt ', 'Unternehmen ', 'Firmen ', 'Entscheidung ', 'Entscheidungen ', 'Werkzeug ', 'Werkzeuge ', 'Niveau ', 'Ebenen ', 'Objekt ', 'Objekte ', 'Taucto ', 'Rohre ', 'Nutzer', 'Nutzerin', 'Benutzer ', 'erstellen ', 'schafft ', 'Ziel ', 'Ziele ', 'Projekt ', 'Projekte ', 'Gruppe ', 'Gruppen ', 'Bürger', 'Bürgerin', 'Bürger ', 'Gemeinschaft ', 'lokal ', 'Plattform ', 'Plattformen ', 'Personen ', 'Menschen ', 'Person ', 'zum ', 'kann ', 'könnte ', 'jedoch ', 'verwenden ', 'Verwendet ', 'machen ', 'macht ', 'gut ', 'Nutzer', 'Nutzerin', 'ebenfalls ', 'Direkte ', 'Idee ', 'von ', 'Gegenstand ', 'verwenden ', 'ein ', 'Über ', 'über ', 'nach ', 'nochmal ', 'gegen ', 'Auge ', 'alle ', 'bin ', 'ein ', 'und ', 'irgendein ', 'sind ', 'aren ', 'sind nicht ', 'wie ', 'beim ', 'Sein ', 'weil ', 'gewesen ', 'Vor ', 'Sein ', 'unten ', 'zwischen ', 'beide ', 'aber ', 'durch ', 'können ', 'konnte nicht ', 'konnte nicht ', 'd ', 'tat ', 'nicht ', 'nicht ', 'tun ', 'tut ', 'tut es nicht ', 'nicht ', 'tun ', 'Don ', 'nicht ', 'Nieder ', 'während ', 'jeder ', 'wenige ', 'zum ', 'von ', 'des Weiteren ', 'hätten ', 'hatte nicht ', 'hatte nicht ', 'hat ', 'Huh ', 'hat nicht ', 'haben ', 'Oase ', 'habe nicht ', 'haben ', 'mit ', 'ihm', 'ihr', 'Hier ', 'ihres ', 'Sie selber ', 'ihm ', 'selbst ', 'seine ', 'Wie ', 'ich ', 'wenn ', 'im ', 'in ', 'ist ', 'isn ', 'ist nicht ', 'es ', 'es ist ', 'es ist ', 'selbst ', 'gerade ', 'll ', 'm ', 'Pferd ', 'mich ', 'könnte nicht ', 'könnte nicht ', 'Mehr ', 'die meisten ', 'darf nicht ', 'darf nicht ', 'meine ', 'mich selber ', 'brauche nicht ', 'brauche nicht ', 'Nein ', 'Noch ', 'nicht ', 'jetzt ', 'Ö ', 'von ', 'aus ', 'auf ', 'Einmal ', 'nur ', 'oder ', 'andere ', 'unsere ', 'unsere ', 'uns selbst ', 'aus ', 'Über ', 'besitzen ', 'Hitze ', 's ', 'gleich ', 'Berg ', 'Shantou ', 'Schlange ', 'sie ist ', 'sollte ', 'sollte haben ', 'sollte nicht ', 'sollte nicht ', 'damit ', 'etwas ', 'eine solche ', 't ', 'als ', 'Das ', 'das wird ', 'das ', 'ihr ', 'ihre ', 'Sie ', 'sich ', 'dann ', 'Dort ', 'diese ', 'Sie ', 'diese ', 'jene ', 'durch ', 'zu ', 'auch ', 'unter ', 'bis um ', 'oben ', 'und ', 'sehr ', 'war ', 'warn ', 'war nicht ', 'wir ', 'wurden ', 'kein Zutritt ', 'waren nicht ', 'Was ', 'wann ', 'wo ', 'welche ', 'während ', 'Wer ', 'wem ', 'Warum ', 'werden ', 'mit ', 'gewonnen ', 'Gewohnheit ', 'würde nicht ', 'würde nicht ', 'und ', 'Haben ', 'du würdest ', 'du wirst ', 'du bist ', 'Sie ', 'Ihre ', 'deine ', 'du selber ', 'euch ', 'könnten ', 'er würde ', 'Hölle ', 'er ist ', 'hier ist ', 'wie ist ', 'Ich würde ', 'krank ', 'Ich bin ', 'Ich habe ', 'Lasst uns ', 'sollen ', 'Schuppen ', 'Schale ', 'das ist ', 'da ist ', 'Sie würden ', 'sie werden ', 'Sie sind ', 'Sie haben ', 'heiraten ', 'Gut ', 'wurden ', 'wir haben ', 'was ist ', 'wann ist ', 'wo ist ', 'wer ist ', 'warum ist ', 'würde ', 'imstande ', 'abst ', 'Übereinstimmung ', 'gemäß ', 'entsprechend ', 'über ', 'Handlung ', 'tatsächlich ', 'hinzugefügt ', 'adj ', 'betroffen ', 'beeinflussen ', 'betrifft ', 'danach ', 'Ah ', 'fast ', 'allein ', 'entlang ', 'bereits ', 'ebenfalls ', 'obwohl ', 'immer ', 'unter ', 'unter ', 'bekannt geben ', 'Ein weiterer ', 'irgendjemand ', 'jedenfalls ', 'nicht mehr ', 'jemand ', 'etwas ', 'wie auch immer ', 'Sowieso ', 'irgendwo ', 'offenbar ', 'etwa ', 'nicht ', 'entstehen ', 'um ', 'beiseite ', 'Fragen ', 'fragen ', 'auth ', 'verfügbar ', 'Weg ', 'schrecklich ', 'b ', 'zurück ', 'wurden ', 'werden ', 'wird ', 'Werden ', 'vorweg ', 'Start ', 'Anfang ', 'Anfänge ', 'beginnt ', 'hinter ', 'glauben ', 'neben ', 'Außerdem ', 'darüber hinaus ', 'Biol ', 'kurz ', 'kurz ', 'c ', 'Das ', 'kam ', 'kann nicht ', 'kippen ', 'Ursache ', 'Ursachen ', 'sicher ', 'bestimmt ', 'Was ', 'mit ', 'Kommen Sie ', 'kommt ', 'enthalten ', 'enthält ', 'enthält ', 'konnte nicht ', 'Datum ', 'anders ', 'getan ', 'nach unten ', 'fällig ', 'ist ', 'ed ', 'Quote ', 'bewirken ', 'z.B ', 'acht ', 'achtzig ', 'entweder ', 'sonst ', 'anderswo ', 'Ende ', 'Ende ', 'genug ', 'insbesondere ', 'und ', 'usw ', 'sogar ', 'je ', 'jeder ', 'jeder ', 'jeder ', 'alles ', 'überall ', 'Ex ', 'außer ', 'f ', 'weit ', 'ff ', 'fünfte ', 'zuerst ', 'fünf ', 'Fix ', 'gefolgt ', 'folgenden ', 'folgt ', 'ehemalige ', 'früher ', 'her ', 'gefunden ', 'vier ', 'Außerdem ', 'G ', 'gegeben ', 'bekommen ', 'bekommt ', 'bekommen ', 'geben ', 'gegeben ', 'gibt ', 'geben ', 'gehen ', 'geht ', 'Weg ', 'habe ', 'bekommen ', 'h ', 'das passiert ', 'kaum ', 'heiß ', 'daher ', 'Jenseits ', 'hiermit ', 'hierin ', 'hier ist ', 'hierauf ', 'er ist ', 'Hallo ', 'versteckt ', 'hierher ', 'Zuhause ', 'aber ', 'jedoch ', 'hundert ', 'Ich würde ', 'dh ', 'im ', 'sofortig ', 'sofort ', 'Bedeutung ', 'wichtig ', 'inc ', 'tatsächlich ', 'Index ', 'Information ', 'stattdessen ', 'Erfindung ', 'innere ', 'usw. ', 'es wird ', 'j ', 'zu ', 'behalten ', 'hält ', 'gehalten ', 'kg ', 'km ', 'kennt ', 'bekannt ', 'weiß ', 'l ', 'weitgehend ', 'zuletzt ', 'in letzter Zeit ', 'später ', 'letztere ', 'zuletzt ', 'am wenigsten ', 'weniger ', 'damit nicht ', 'Lassen ', 'Lasst uns ', 'mögen ', 'gefallen ', 'wahrscheinlich ', 'Linie ', 'wenig ', 'werde ', 'aussehen ', 'suchen ', 'sieht aus ', 'GmbH ', 'gemacht ', 'hauptsächlich ', 'machen ', 'macht ', 'viele ', 'kann ', 'könnte sein ', 'bedeuten ', 'meint ', 'inzwischen ', 'inzwischen ', 'nur ', 'mg ', 'könnte ', 'Million ', 'Fräulein ', 'ml ', 'Außerdem ', 'meist ', 'Herr', 'Herrin', 'Frau ', 'viel ', 'Becher ', 'Muss ', 'n ', 'auf ', 'Dann ', 'nämlich ', 'jetzt weiter ', 'nd ', 'in der Nähe von ', 'fast ', 'Notwendig ', 'notwendig ', 'brauchen ', 'Bedürfnisse ', 'weder ', 'noch nie ', 'Dennoch ', 'Neu ', 'Nächster ', 'neun ', 'neunzig ', 'niemand ', 'nicht ', 'keiner ', 'dennoch ', 'Niemand ', 'normalerweise ', 'wir ', 'notiert ', 'nichts ', 'nirgends ', 'erhalten ', 'erhalten ', 'offensichtlich ', 'häufig ', 'Oh ', 'in Ordnung ', 'in Ordnung ', 'alt ', 'weggelassen ', 'einer ', 'Einsen ', 'auf zu ', 'Wörter ', 'Andere ', 'Andernfalls ', 'draußen ', 'insgesamt ', 'geschuldet ', 'p ', 'Seite ', 'Seiten ', 'Teil ', 'besonders ', 'insbesondere ', 'Vergangenheit ', 'zum ', 'vielleicht ', 'platziert ', 'Bitte ', 'Mehr ', 'schlecht ', 'möglich ', 'möglicherweise ', 'möglicherweise ', 'pp ', 'überwiegend ', 'Geschenk ', 'vorher ', 'in erster Linie ', 'wahrscheinlich ', 'sofort ', 'stolz ', 'bietet ', 'stellen ', 'q ', 'Was ', 'schnell ', 'ziemlich ', 's ', 'r ', 'Na sicher ', 'lieber ', 'rd ', 'leicht ', 'Ja wirklich ', 'kürzlich ', 'vor kurzem ', 'ref ', 'refs ', 'hinsichtlich ', 'ungeachtet ', 'Grüße ', 'verbunden ', 'verhältnismäßig ', 'Forschung ', 'beziehungsweise ', 'resultierte ', 'resultierend ', 'Ergebnisse ', 'Recht ', 'Lauf ', 'sagte ', 'sah ', 'sagen ', 'Sprichwort ', 'sagt ', 'sek ', 'Sektion ', 'sehen ', 'Sehen ', 'scheinen ', 'schien ', 'scheinbar ', 'scheint ', 'gesehen ', 'selbst ', 'Selbst ', 'geschickt ', 'Sieben ', 'mehrere ', 'soll ', 'Schuppen ', 'shes ', 'Show ', 'gezeigt ', 'gezeigt ', 'gezeigt ', 'zeigt an ', 'von Bedeutung ', 'bedeutend ', 'ähnlich ', 'ähnlich ', 'schon seit ', 'sechs ', 'leicht ', 'jemanden ', 'irgendwie ', 'jemand ', 'etwas ', 'etwas ', 'irgendwann ', 'manchmal ', 'etwas ', 'irgendwo ', 'demnächst ', 'Es tut uns leid ', 'speziell ', 'spezifizierten ', 'angeben ', 'spezifizieren ', 'immer noch ', 'halt ', 'stark ', 'sub ', 'im Wesentlichen ', 'erfolgreich ', 'ausreichend ', 'vorschlagen ', 'sup ', 'sicher ', 'nehmen ', 'genommen ', 'nehmen ', 'sagen ', 'neigt dazu ', 'th ', 'danken ', 'Vielen Dank ', 'Danke ', 'das ist ', 'das haben ', 'von dort ', 'danach ', 'damit ', 'das Rote ', 'deshalb ', 'darin ', 'da wird ', 'davon ', 'da ', 'theres ', 'dazu ', 'daraufhin ', 'da haben ', 'Sie würden ', 'Sie sind ', 'Überlegen ', 'du ', 'obwohl ', 'obwohl ', 'tausend ', 'durch ', 'während ', 'durch ', 'so ', 'zu ', 'Trinkgeld ', 'zusammen ', 'dauerte ', 'zu ', 'gegenüber ', 'versucht ', 'versucht es ', 'wirklich ', 'Versuchen ', 'versuchen ', 'ts ', 'zweimal ', 'zwei ', 'u ', 'ein ', 'Unglücklicherweise ', 'es sei denn ', 'nicht wie ', 'unwahrscheinlich ', 'zu ', 'auf ', 'UPS ', 'uns ', 'verwenden ', 'gebraucht ', 'nützlich ', 'nützlich ', 'Nützlichkeit ', 'Verwendet ', 'mit ', 'meistens ', 'im ', 'Wert ', 'verschiedene ', "'und ", 'über ', 'nämlich ', 'vol ', 'Flüge ', 'vs. ', 'im ', 'wollen ', 'will ', 'war nicht ', 'Weg ', 'heiraten ', 'herzlich willkommen ', 'ging ', 'werent ', 'wie auch immer ', 'was wird ', 'was ist ', 'woher ', 'wann immer ', 'danach ', 'wohingegen ', 'wodurch ', 'worin ', 'wo ist ', 'worauf ', 'wo auch immer ', 'ob ', 'Laune ', 'wohin ', 'Wer würde ', 'wer auch immer ', 'ganze ', 'Wer wird ', 'wen auch immer ', 'wer ', 'deren ', 'weit ', 'bereit ', 'Wunsch ', 'innerhalb ', 'ohne ', 'Gewohnheit ', 'Wörter ', 'Welt ', 'würde nicht ', 'www ', 'x ', 'Ja ', 'noch ', 'du ', 'du bist ', 'mit ', 'Null ', 'wie ', 'ist nicht ', 'ermöglichen ', 'erlaubt ', 'ein Teil ', 'erscheinen ', 'schätzen ', 'angemessen ', 'damit verbundenen ', 'Beste ', 'besser ', 'Komm schon ', "c's ", 'kippen ', 'Änderungen ', 'deutlich ', 'über ', 'Folglich ', 'Erwägen ', 'in Anbetracht ', 'dazugehörigen ', 'Kurs ', 'zur Zeit ', 'bestimmt ', 'beschrieben ', 'Trotz ', 'vollständig ', 'genau ', 'Beispiel ', 'gehen ', 'Schöne Grüße ', 'Hallo ', 'Hilfe ', 'hoffnungsvoll ', 'ignoriert ', 'insofern ', 'zeigen ', 'angegeben ', 'zeigt an ', 'innere ', 'soweit ', 'es würde ', 'behalten ', 'hält ', 'Roman ', 'vermutlich ', 'vernünftig ', 'zweite ', 'zweitens ', 'sinnvoll ', 'ernst ', 'Ernsthaft ', 'sicher ', "t's ", 'dritte ', 'gründlich ', 'gründlich ', 'drei ', 'Gut ', 'Wunder ', 'ein ', 'Über ', 'über ', 'über ', 'über ', 'nach ', 'danach ', 'nochmal ', 'gegen ', 'alle ', 'fast ', 'allein ', 'entlang ', 'bereits ', 'ebenfalls ', 'obwohl ', 'immer ', 'bin ', 'unter ', 'unter ', 'unter ', 'Menge ', 'ein ', 'und ', 'Ein weiterer ', 'irgendein ', 'jedenfalls ', 'jemand ', 'etwas ', 'wie auch immer ', 'irgendwo ', 'sind ', 'um ', 'wie ', 'beim ', 'zurück ', 'Sein ', 'wurden ', 'weil ', 'werden ', 'wird ', 'Werden ', 'gewesen ', 'Vor ', 'vorweg ', 'hinter ', 'Sein ', 'unten ', 'neben ', 'Außerdem ', 'zwischen ', 'darüber hinaus ', 'Rechnung ', 'beide ', 'Unterseite ', 'aber ', 'durch ', 'Anruf ', 'können ', 'kann nicht ', 'kippen ', 'Was ', 'mit ', 'könnten ', 'konnte nicht ', 'Schrei ', 'von ', 'beschreiben ', 'Detail ', 'tun ', 'getan ', 'Nieder ', 'fällig ', 'während ', 'jeder ', 'z.B ', 'acht ', 'entweder ', 'elf ', 'sonst ', 'anderswo ', 'leer ', 'genug ', 'usw ', 'sogar ', 'je ', 'jeder ', 'jeder ', 'alles ', 'überall ', 'außer ', 'wenige ', 'fünfzehn ', 'fify ', 'füllen ', 'finden ', 'Feuer ', 'zuerst ', 'fünf ', 'zum ', 'ehemalige ', 'früher ', 'vierzig ', 'gefunden ', 'vier ', 'von ', 'Vorderseite ', 'voll ', 'des Weiteren ', 'bekommen ', 'geben ', 'gehen ', 'hätten ', 'hat ', 'hat nicht ', 'haben ', 'mit ', 'daher ', 'ihm', 'ihr', 'Hier ', 'Jenseits ', 'hiermit ', 'hierin ', 'hierauf ', 'ihres ', 'Sie selber ', 'ihm ', 'selbst ', 'seine ', 'Wie ', 'jedoch ', 'hundert ', 'dh ', 'wenn ', 'im ', 'inc ', 'tatsächlich ', 'Interesse ', 'in ', 'ist ', 'es ', 'es ist ', 'selbst ', 'behalten ', 'zuletzt ', 'letztere ', 'zuletzt ', 'am wenigsten ', 'weniger ', 'GmbH ', 'gemacht ', 'viele ', 'kann ', 'mich ', 'inzwischen ', 'könnte ', 'von ', 'Bergwerk ', 'Mehr ', 'Außerdem ', 'die meisten ', 'meist ', 'Bewegung ', 'viel ', 'Muss ', 'meine ', 'mich selber ', 'Dann ', 'nämlich ', 'weder ', 'noch nie ', 'Dennoch ', 'Nächster ', 'neun ', 'Nein ', 'niemand ', 'keiner ', 'Niemand ', 'Noch ', 'nicht ', 'nichts ', 'jetzt ', 'nirgends ', 'von ', 'aus ', 'häufig ', 'auf ', 'Einmal ', 'einer ', 'nur ', 'auf zu ', 'oder ', 'andere ', 'Andere ', 'Andernfalls ', 'unsere ', 'unsere ', 'uns selbst ', 'aus ', 'Über ', 'besitzen ', 'Teil ', 'zum ', 'vielleicht ', 'Bitte ', 'stellen ', 'lieber ', 'Hitze ', 'gleich ', 'sehen ', 'scheinen ', 'schien ', 'scheinbar ', 'scheint ', 'ernst ', 'mehrere ', 'Schlange ', 'sollte ', 'Show ', 'Seite ', 'schon seit ', 'aufrichtig ', 'sechs ', 'sechzig ', 'damit ', 'etwas ', 'irgendwie ', 'jemand ', 'etwas ', 'irgendwann ', 'manchmal ', 'irgendwo ', 'immer noch ', 'eine solche ', 'System ', 'nehmen ', 'diese ', 'als ', 'Das ', 'das ', 'ihr ', 'Sie ', 'sich ', 'dann ', 'von dort ', 'Dort ', 'danach ', 'damit ', 'deshalb ', 'darin ', 'daraufhin ', 'diese ', 'Sie ', 'dick ', 'dünn ', 'dritte ', 'diese ', 'jene ', 'obwohl ', 'drei ', 'durch ', 'während ', 'durch ', 'so ', 'zu ', 'zusammen ', 'auch ', 'oben ', 'zu ', 'gegenüber ', 'zwölf ', 'zwanzig ', 'zwei ', 'ein ', 'unter ', 'bis um ', 'oben ', 'auf ', 'uns ', 'sehr ', 'über ', 'war ', 'wir ', 'Gut ', 'wurden ', 'Was ', 'wie auch immer ', 'wann ', 'woher ', 'wann immer ', 'wo ', 'danach ', 'wohingegen ', 'wodurch ', 'worin ', 'worauf ', 'wo auch immer ', 'ob ', 'welche ', 'während ', 'wohin ', 'Wer ', 'wer auch immer ', 'ganze ', 'wem ', 'deren ', 'Warum ', 'werden ', 'mit ', 'innerhalb ', 'ohne ', 'würde ', 'noch ', 'Haben ', 'Ihre ', 'deine ', 'du selber ', 'euch ', 'das ', 'Mangel ', 'machen ', 'wollen ', 'scheinen ', 'Lauf ', 'brauchen ', 'sogar ', 'Recht ', 'verwenden ', 'nicht ', 'würde ', 'sagen ', 'könnten ', '_ ', 'Sein ', 'kennt ', 'gut ', 'gehen ', 'bekommen ', 'tun ', 'getan ', 'Versuchen ', 'viele ', 'von ', 'Gegenstand ', 'Hitze ', 'Quote ', 'etwas ', 'nett ', 'danken ', 'Überlegen ', 'sehen ', 'lieber ', 'einfach ', 'leicht ', 'Menge ', 'Linie ', 'sogar ', 'ebenfalls ', 'kann ', 'nehmen ', 'Kommen Sie '])
a_file = open("stopwords.txt", "r")
for line in a_file:
    stripped_line = line.strip()
    stop_words_de.append(stripped_line)

#Initialize URL and EMAIL PATTERNS
url_pattern = re.compile(re.compile(r'https?://\S+|www\.S+'))
email_pattern = re.compile(re.compile(r'\S*@\S*\s?'))


def extract_features_de(df, feature,allowed_postags=['NOUN', 'ADJ']):
    """
    funtion to extract the nouns and adjectives from the dataframe GERMAN LANGUAGE 

    IN: df : pandas dataframe
        feature: name of column that contains text
    OUT: new_text_list: List of list of words extracted
        deleted_index: A list with the indexes where the text was deleted 

    """    

    #Intialize the lists
    texts_list = []
    deleted_index = []    
    new_texts_list = []    
    AI_stopwords = ['KI','künstlich','Intelligenz','AI','ki','kI','Ai','aI','Artifizielle','artifizielle','intelligenz']

    #Replace "-" with empty space
    entries = [entry.replace("-", " ") for entry in df[feature]]

    #Extract only nouns and adjectives
    for text in entries:
        tokenized_sent = nltk.tokenize.word_tokenize(text,language='german')
        tags = tagger.tag_sent(tokenized_sent)
        texts_list.append([lemma for (word,lemma,pos) in tags if pos == "NN" or pos == "NA" or pos == "ADJA"])       

    #delete URL, EMAIL PATTERNS, STOPWORDS and WORDS with LENGTH LESS THAN 2   
    texts_list = [[word for word in doc if word not in stop_words_de] for doc in texts_list]
    texts_list = [[url_pattern.sub('', word) for word in doc] for doc in texts_list]
    texts_list = [[email_pattern.sub('', word) for word in doc] for doc in texts_list]
    texts_list = [[word for word in doc if len(word)>1] for doc in texts_list]
    texts_list = [[word for word in doc if word not in stop_words_de] for doc in texts_list]
    texts_list = [[word for word in doc if word not in AI_stopwords] for doc in texts_list]

    #STORE the words lists that contains at least 3 words and store the deleted index of lists that contain less than 3 words      
    for i,x in enumerate(texts_list):
        if x != [] or len(x)>2:            
            new_texts_list.append(x)
        else:
            deleted_index.append(i)   

    return new_texts_list, deleted_index



def extract_features_de_sub(document_list,allowed_postags=['NOUN', 'ADJ']):
    """
    funtion to extract the nouns and adjectives from the dataframe LEVEL 2 or 3 of TOPIC MODELLING GERMAN LANGUAGE 

    IN: document_list : list of documents belonging to each topic in LEVEL 1 
        
    OUT: texts_list: List of list of words extracted
        df_level: dataframe containing the text column filled with document_list 

    """        

    #Initialize the dataframe, the list of words and Stopwords related to AI
    df_level = pd.DataFrame()
    texts_list = []
    AI_stopwords = ['KI','künstlich','Intelligenz','AI','ki','kI','Ai','aI','Artifizielle','artifizielle','intelligenz']

    #Fill the dataframe with document_list from each topic in level 1 
    df_level['Text'] = document_list

    entries = [entry.replace("-", " ") for entry in document_list]
    
    for text in entries:
        tokenized_sent = nltk.tokenize.word_tokenize(text,language='german')
        tags = tagger.tag_sent(tokenized_sent)
        texts_list.append([lemma for (word,lemma,pos) in tags if pos == "NN" or pos == "NA" or pos == "ADJA"])       

       
    texts_list = [[word for word in doc if word not in stop_words_de] for doc in texts_list]
    texts_list = [[url_pattern.sub('', word) for word in doc] for doc in texts_list]
    texts_list = [[email_pattern.sub('', word) for word in doc] for doc in texts_list]
    texts_list = [[word for word in doc if len(word)>1] for doc in texts_list]
    texts_list = [[word for word in doc if word not in stop_words_de] for doc in texts_list]
    texts_list = [[word for word in doc if word not in AI_stopwords] for doc in texts_list]
        

    return texts_list, df_level






