# -*- coding: utf-8 -*-
"""Der Kanon der drei Synthesen — 75 Bogen, 76 Nachtglas, 77 Rundlauf.

Die drei Blätter sind nicht drei Einfälle nebeneinander, sondern **ein Aufbau
in drei Materialien**: Papier, Glas, Metall. Was sie teilen, steht hier; was
sie unterscheidet, steht in ihren eigenen Dateien. Geteilt wird dreierlei.

**Ein Maßband.** Jeder Abstand auf allen sechs Bühnen ist ein Glied derselben
Reihe (8 · 13 · 21 · 34 · 55 · 89 · 144), am Telefon mit 1.5 genommen. Ein
Blatt wirkt nicht ruhig, weil wenig darauf steht, sondern weil alle Abstände
aus einer Reihe stammen — zwei Werte, die fast gleich sind, sind der
häufigste Grund für Unruhe. Der Blattrand ist immer 89.

**Eine Schriftleiter.** Fünf enge Stufen um 1.3 und ein bewusster Sprung zur
Überschrift. Die enge Leiter hält Auszeichnung, Lauftext und Zahl beieinander
— dort will man Ordnung, keinen Kontrast; der Sprung ist der einzige Ort, an
dem gerufen wird. Am Telefon steht dieselbe Leiter etwa doppelt so gross im
Verhältnis zur Fläche: eine Hand ist näher am Auge als ein Schirm, aber eine
Fläche von 1080 px trägt weniger Zeichen als eine von 1600.

**Ein Satzspiegel.** Der Goldene Schnitt teilt die Rechnerbühne: das Bild
nimmt 0.382 der Satzbreite, der Text den Rest. Beim Telefon entfällt die
Teilung — hochkant gibt es nur eine Spalte, und eine Spalte teilt man nicht.

**Eine Bedienreihe.** Zurück · Wiedergabe · Vor, danach mit Abstand die drei
leisen Zeichen Suche · Sammlung · Lautstärke. Dieselbe Reihenfolge, dieselben
Größenverhältnisse (die Wiedergabe 1.25×, die leisen 0.8×) auf allen sechs
Bühnen — das ist der Teil, den man nicht zweimal lernen soll.

Was der Kanon **nicht** vorschreibt, ist die Standanzeige. Die trägt jedes
Material selbst: eine Haarlinie auf Papier, eine Lichtkante im Glas, ein
Zeiger auf Metall. Das ist die Hausregel „bewegt wird, was den Stand zeigt“
von der anderen Seite gelesen — was den Stand zeigt, ist der Entwurf.
"""
from werkzeug import biblio, laut, lupe, nexti, pausei, prev

# ---- Maßband ---------------------------------------------------------------
REIHE = (8, 13, 21, 34, 55, 89, 144)
RAND = 89
GOLD = .382


def m(i, tel=False):
    """Ein Glied der Reihe; am Telefon anderthalbfach."""
    return int(REIHE[i] * (1.5 if tel else 1))


# ---- Schriftleiter ---------------------------------------------------------
# mark  Kapitälchen, Marken, Ziffern unter der Skala
# klein Nebentext, Dauer, Zeitanzeige
# lauf  Titelliste — der Text, den man wirklich liest
# gross Interpret, Zwischenüberschrift
# titel Albumtitel
# ruf   der eine Sprung; nur wo ein Blatt rufen soll
GRADE_PC = dict(mark=13, klein=17, lauf=22, gross=30, titel=46, ruf=104)
GRADE_TEL = dict(mark=19, klein=24, lauf=30, gross=42, titel=64, ruf=140)


def grade(tel):
    return GRADE_TEL if tel else GRADE_PC


# ---- Bedienreihe -----------------------------------------------------------
def zeichenreihe(farbe, d=34):
    """Die drei Transportzeichen einzeln, in der Reihenfolge des Kanons — für
    Materialien, die jedes Zeichen in eine eigene Taste setzen (77 Rundlauf)."""
    return [prev(d, farbe), pausei(int(d * 1.25), farbe), nexti(d, farbe)]


def transport(farbe, d=34, weite=None):
    """Zurück · Wiedergabe · Vor. Die Wiedergabe steht 1.25× — sie ist die
    einzige Taste, die man im Vorbeigehen trifft."""
    w = int(d * 1.15) if weite is None else weite
    return (f'<span class="reihe" style="display:inline-flex;align-items:center;gap:{w}px">'
            + ''.join(zeichenreihe(farbe, d)) + '</span>')


def leise(farbe, d=34, weite=None):
    """Suche · Sammlung · Lautstärke — 0.8× und stiller gefärbt. Die Sammlung
    steht in der Mitte der drei, weil sie von den dreien am häufigsten
    gebraucht wird und die Mitte einer Dreiergruppe der ruhigste Platz ist."""
    d = int(d * .8)
    w = int(d * 1.15) if weite is None else weite
    return (f'<span class="reihe" style="display:inline-flex;align-items:center;gap:{w}px">'
            f'{lupe(d, farbe, 2)}{biblio(d, farbe)}{laut(d, farbe)}</span>')


# ---- Titel und Zeit --------------------------------------------------------
# Ein Album für alle drei Blätter, mit den echten Spielzeiten — nur so ist die
# Skala unter dem Blatt eine Aussage und keine gleichmäßige Teilung.
TITEL = [('01', 'So What', '9:22'), ('02', 'Freddie Freeloader', '9:46'),
         ('03', 'Blue in Green', '5:37'), ('04', 'All Blues', '11:33'),
         ('05', 'Flamenco Sketches', '9:26')]
LAEUFT = 2
IM_TITEL = 134            # 02:14 im laufenden Stück


def sekunden(t):
    mm, ss = t.split(':')
    return int(mm) * 60 + int(ss)


def gesamtzeit():
    s = sum(sekunden(t[2]) for t in TITEL)
    return f'{s // 60}:{s % 60:02d}'


def marken():
    """Die Titelgrenzen als Anteile 0…1 und der Stand im ganzen Album.

    Rückgabe: (grenzen, stand). `grenzen` hat einen Eintrag je Titelanfang
    plus den Schluss, `stand` ist die Gegenwart im ganzen Album.
    """
    dauern = [sekunden(t[2]) for t in TITEL]
    gesamt = sum(dauern)
    lauf, grenzen = 0, [0.0]
    for d in dauern:
        lauf += d
        grenzen.append(lauf / gesamt)
    stand = (sum(dauern[:LAEUFT]) + IM_TITEL) / gesamt
    return grenzen, stand
