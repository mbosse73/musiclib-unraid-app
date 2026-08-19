# -*- coding: utf-8 -*-
"""79 Lesezeichen — der Text ist die Zeitachse.

Zweite von drei **Abweichungen**. Kein Vorbild im Register, und diesmal auch
kein Gegenstand: das Blatt ist eine **Buchseite**.

Die ganze Titelliste steht als **ein einziger Absatz im Blocksatz**, Titel an
Titel, durch ein Quadrat getrennt, die Dauern als hochgestellte Ziffern wie
Fussnotenzeichen. Und dann kommt der eine Einfall, an dem alles hängt:

**Was gespielt ist, steht in voller Schwärze; was kommt, steht blass.** Die
Grenze zwischen beidem ist die Gegenwart — mitten im Wort, wenn es sein muss,
denn die Zeit hält sich nicht an Silben. Genau dort steht ein
zinnoberroter Keil, und das ist die gesamte Anzeige des Entwurfs.

Was daran ungewöhnlich ist, ist nicht die Optik, sondern die Folge: **es gibt
keine Fortschrittsanzeige, weil der Inhalt die Anzeige ist.** Man liest ab,
wie weit das Album ist, indem man liest, wie weit die Schwärze reicht — und
weil ein langes Stück viele Zeichen hat und ein kurzes wenige, ist der
Absatz zugleich das Bild des Albums. Kein Balken, kein Ring, keine Prozente,
keine zweite Fläche für dieselbe Auskunft.

Gespult wird **im Text**: man zieht den Keil durch den Absatz. Titelgrenzen
sind Trennzeichen, keine Sprungmarken — man geht darüber hinweg wie beim
Lesen.

Zwei Dinge, die nicht verhandelbar sind:

- **Der Blocksatz.** Flattersatz macht daraus eine Liste, und eine Liste hat
  das Register in dreissig Fassungen. Der geschlossene Satzblock ist das,
  was die Seite zur Seite macht.
- **Nur eine Farbe.** Zinnober steht am Keil und sonst nirgends. Das Bild ist
  in denselben zwei Druckfarben gehalten wie der Text — Schwarz und Zinnober,
  wie ein zweifarbiger Druck es hergibt.

Abgegrenzt: K10 Weissraum und K89 Bogen sind auch ruhig und typografisch,
aber dort ist die Schrift der *Inhalt* und eine Linie die Anzeige. Hier gibt
es keine Linie.
"""
from kanon import LAEUFT, TITEL, gesamtzeit, marken
from werkzeug import A, biblio, laut, lupe, nexti, pausei, prev, schreibe
from werkzeug import MONO, SANS, SERIF

PAPIER = '#F7F3E9'
PAPIER2 = '#EFE9DA'
SCHWARZ = '#1A1714'
BLASS = 'rgba(26,23,20,.26)'
HALB = 'rgba(26,23,20,.55)'
ZINNOBER = '#C1361F'


def _css(tel):
    k = 1.5 if tel else 1
    return f'''
.stage{{background:linear-gradient(178deg,{PAPIER} 0%,{PAPIER2} 100%);
  font-family:{SERIF};color:{SCHWARZ};-webkit-font-smoothing:antialiased}}
.kap{{font-family:{SANS};font-size:{int(12 * k)}px;letter-spacing:.30em;
  text-transform:uppercase;color:{HALB}}}
.titel{{font-size:{int(74 * k)}px;line-height:.98;letter-spacing:-.022em;
  font-weight:400;text-wrap:balance}}
.wer{{font-style:italic;font-size:{int(26 * k)}px;color:{HALB};margin-top:{int(12 * k)}px}}
/* Der Satzblock. Alles, was diesen Entwurf ausmacht, steckt hier — Blocksatz,
   Trennung, zwei Schwaerzen. Und er ist **gross**: fuenf Titel fuellen keine
   Seite in Lesegroesse, also wird die Titelliste selbst zur Ueberschrift.
   Das dreht die uebliche Rangfolge um, und zwar mit Absicht: gehoert wird ein
   Titel, nicht ein Album. */
.satz{{text-align:justify;hyphens:auto;-webkit-hyphens:auto;
  line-height:1.02;letter-spacing:-.018em;text-indent:0;margin:0;
  /* Der Absatz ist ein Flex-Kind: ohne min-width:0 waechst er auf seine
     max-content-Breite und laeuft aus dem Blatt heraus. */
  width:100%;min-width:0}}
.gelesen{{color:{SCHWARZ}}}
.kommt{{color:{BLASS}}}
.trenn{{color:{BLASS};padding:0 {int(7 * k)}px;font-size:.26em;vertical-align:.42em}}
.gelesen .trenn{{color:rgba(26,23,20,.42)}}
.dauer{{font-family:{MONO};font-size:.20em;vertical-align:.90em;letter-spacing:.02em;
  padding-left:{int(6 * k)}px;font-weight:400}}
/* Der Keil sitzt im Textfluss, nicht darueber: so steht er immer genau auf
   der Stelle, egal wie der Satz umbricht. */
.marke{{display:inline-block;width:0;height:0;vertical-align:.06em;
  border-left:.20em solid {ZINNOBER};
  border-top:.17em solid transparent;border-bottom:.17em solid transparent;
  margin:0 .04em}}
.fuss{{font-family:{SANS};font-size:{int(13 * k)}px;color:{HALB};
  display:flex;align-items:center;gap:{int(26 * k)}px}}
.uhr{{font-family:{MONO};font-size:{int(16 * k)}px;color:{SCHWARZ};
  font-variant-numeric:tabular-nums}}
.zeichen{{display:flex;align-items:center;gap:{int(24 * k)}px}}
.folio{{font-family:{MONO};font-size:{int(13 * k)}px;color:{BLASS}}}
'''


def _atome():
    """Die Titelliste als Folge von Stücken, jedes mit seiner Zeichenzahl —
    daraus wird der Absatz und daraus die Stelle, an der er umschlägt."""
    st = []
    for i, (nr, na, da) in enumerate(TITEL):
        if i:
            st.append(('trenn', '▪'))
        st.append(('titel', na))
        st.append(('dauer', da))
    return st


def _satz(tel):
    """Ein Absatz, zwei Schwärzen, ein Keil dazwischen.

    Die Stelle wird über die **Zeichenzahl** gefunden, nicht über eine
    Pixelbreite: der Absatz bricht auf jedem Gerät anders um, die Zeichen
    bleiben dieselben.
    """
    _, stand = marken()
    st = _atome()
    gesamt = sum(len(x[1]) for x in st)
    ziel = stand * gesamt

    def stueck(art, text, gelesen):
        if art == 'trenn':
            # Echte Leerzeichen um das Quadrat: CSS-Polster gibt keine
            # Umbruchstelle her, und ohne Umbruchstelle haengt die Dauer am
            # naechsten Titel fest und reisst die Zeile auf.
            return f' <span class="trenn">{text}</span> '
        if art == 'dauer':
            # Ohne Leerzeichen davor: die Dauer gehoert an ihren Titel wie
            # ein Fussnotenzeichen und darf nie eine Zeile anfangen.
            return f'<span class="dauer">{text}</span>'
        return text

    vor, nach, lauf, keil = [], [], 0, False
    for art, text in st:
        if keil:
            nach.append(stueck(art, text, False))
            continue
        if lauf + len(text) <= ziel:
            vor.append(stueck(art, text, True))
            lauf += len(text)
            continue
        # Hier schlägt es um — mitten im Wort, wenn es sein muss.
        schnitt = max(0, int(ziel - lauf))
        if art == 'titel' and 0 < schnitt < len(text):
            vor.append(text[:schnitt])
            nach.append(text[schnitt:])
        elif schnitt >= len(text):
            vor.append(stueck(art, text, True))
        else:
            nach.append(stueck(art, text, False))
        keil = True
    return (f'<p class="satz" lang="en"><span class="gelesen">{"".join(vor)}</span>'
            f'<span class="marke"></span>'
            f'<span class="kommt">{"".join(nach)}</span></p>')


def _zeichen(k, gross, klein):
    z = [prev(gross, SCHWARZ), pausei(int(gross * 1.2), SCHWARZ), nexti(gross, SCHWARZ)]
    l = [lupe(klein, HALB, 2), biblio(klein, HALB), laut(klein, HALB)]
    return (f'<span class="zeichen">{"".join(z)}</span>'
            f'<span style="width:1px;height:{int(24 * k)}px;background:{BLASS}"></span>'
            f'<span class="zeichen">{"".join(l)}</span>')


def rechner():
    """Eine Spalte, so gross wie es geht. Der Satz ist die Seite; darüber
    steht klein, wovon er handelt, darunter, wo man gerade steht."""
    tel, k = False, 1
    body = f'''<div style="position:absolute;inset:0;padding:74px 88px 66px;
  display:flex;flex-direction:column">
  <div style="display:flex;align-items:baseline;justify-content:space-between">
    <span class="kap">{A['album']} · {A['interpret']} · {A['jahr']}</span>
    <span class="kap">Musiklib · {len(TITEL)} Titel · {gesamtzeit()}</span>
  </div>
  <div style="flex:1;display:flex;align-items:center;font-size:114px">
    {_satz(tel)}
  </div>
  <div style="padding-top:26px;border-top:1px solid rgba(26,23,20,.16);
    display:flex;align-items:center;justify-content:space-between">
    <div class="fuss">
      <span class="uhr" style="font-size:22px">{A['pos']}</span>
      <span>von {TITEL[LAEUFT][2]}</span>
      <span class="kap">{TITEL[LAEUFT][1]}</span>
    </div>
    <div class="fuss">{_zeichen(k, 26, 21)}</div>
    <span class="folio">{A['jahr']}</span>
  </div>
</div>'''
    return _css(tel), body


def telefon():
    """Hochkant dasselbe, nur schmaler und damit höher — der Satz füllt die
    Fläche von selbst, weil weniger Zeichen in eine Zeile passen."""
    tel, k = True, 1.5
    body = f'''<div style="position:absolute;inset:0;padding:92px 78px 88px;
  display:flex;flex-direction:column">
  <div>
    <div class="kap">{A['album']} · {A['interpret']}</div>
    <div class="kap" style="margin-top:10px">{len(TITEL)} Titel · {gesamtzeit()} · {A['jahr']}</div>
  </div>
  <div style="flex:1;display:flex;align-items:center;font-size:138px">
    {_satz(tel)}
  </div>
  <div style="padding-top:34px;border-top:1px solid rgba(26,23,20,.16)">
    <div class="fuss" style="justify-content:space-between">
      <span class="uhr" style="font-size:34px">{A['pos']}</span>
      <span class="kap">{TITEL[LAEUFT][1]}</span>
    </div>
    <div class="fuss" style="margin-top:40px;justify-content:space-between">
      {_zeichen(k, 44, 34)}
    </div>
  </div>
</div>'''
    return _css(tel), body


def bau():
    for art, fn in (('iphone', telefon), ('pc', rechner)):
        css, body = fn()
        yield schreibe('79', 'Lesezeichen', art, css, body)
