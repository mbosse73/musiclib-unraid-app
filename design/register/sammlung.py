"""Eine Testsammlung mit realistischen Albumlaengen.

Vier Titel je Album lassen jedes listenbasierte Layout halb leer aussehen —
das ist ein Fehler der Sammlung, nicht des Entwurfs. Zehn bis zwoelf Titel
zeigen, was die Layouts wirklich tun.

Als Modul: baue(ordner) legt die Sammlung dort an. Als Skript: nach
design/register/musik, damit man sie sich auch von Hand ansehen kann.
"""
import pathlib, shutil, sys

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO))
from conftest import write_mp3, frames

ALBEN = [
 ('ambient','Music for Airports','Brian Eno','1978',
  ['1/1','2/1','1/2','2/2','Ambient Drift','Signal','Terminal','Slow Arrival',
   'Departure Lounge','Night Flight']),
 ('btr','Born to Run','Bruce Springsteen','1975',
  ['Thunder Road','Tenth Avenue Freeze-Out','Night','Backstreets','Born to Run',
   "She's the One",'Meeting Across the River','Jungleland']),
 ('kob','Kind of Blue','Miles Davis','1959',
  ['So What','Freddie Freeloader','Blue in Green','All Blues','Flamenco Sketches']),
 ('rumours','Rumours','Fleetwood Mac','1977',
  ['Second Hand News','Dreams','Never Going Back Again','Go Your Own Way','Songbird',
   'The Chain','You Make Loving Fun','I Dont Want to Know','Oh Daddy','Gold Dust Woman']),
 ('dsotm','The Dark Side of the Moon','Pink Floyd','1973',
  ['Speak to Me','Breathe','On the Run','Time','The Great Gig in the Sky','Money',
   'Us and Them','Any Colour You Like','Brain Damage','Eclipse']),
 ('blue','Blue','Joni Mitchell','1971',
  ['All I Want','My Old Man','Little Green','Carey','Blue','California','This Flight Tonight',
   'River','A Case of You','The Last Time I Saw Richard']),
 ('okc','OK Computer','Radiohead','1997',
  ['Airbag','Paranoid Android','Subterranean Homesick Alien','Exit Music','Let Down',
   'Karma Police','Fitter Happier','Electioneering','Climbing Up the Walls','No Surprises',
   'Lucky','The Tourist']),
 ('grace','Graceland','Paul Simon','1986',
  ['The Boy in the Bubble','Graceland','I Know What I Know','Gumboots',
   'Diamonds on the Soles of Her Shoes','You Can Call Me Al','Under African Skies',
   'Homeless','Crazy Love, Vol. II','All Around the World']),
 ('unknown','Unknown Pleasures','Joy Division','1979',
  ['Disorder','Day of the Lords','Candidate','Insight','New Dawn Fades',
   'She’s Lost Control','Shadowplay','Wilderness','Interzone','I Remember Nothing']),
 ('tee','Trans Europa Express','Kraftwerk','1977',
  ['Europa Endlos','Spiegelsaal','Schaufensterpuppen','Trans Europa Express',
   'Metall auf Metall','Franz Schubert','Endlos Endlos']),
 ('love','A Love Supreme','John Coltrane','1965',
  ['Acknowledgement','Resolution','Pursuance','Psalm']),
 ('magic','Magic','Bruce Springsteen','2007',
  ['Radio Nowhere','Youll Be Comin Down','Livin in the Future','Your Own Worst Enemy',
   'Gypsy Biker','Girls in Their Summer Clothes','I ll Work for Your Love','Magic',
   'Last to Die','Long Walk Home','Devils Arcade']),
]


def baue(ziel):
    """Legt die Sammlung unter ziel an — vorhandenes wird ersetzt."""
    ziel = pathlib.Path(ziel)
    shutil.rmtree(ziel, ignore_errors=True)
    n = 0
    for ordner, album, interpret, jahr, titel in ALBEN:
        for i, t in enumerate(titel, 1):
            write_mp3(ziel / ordner / f'{i:02d}.mp3', title=t, artist=interpret, album=album,
                      album_artist=interpret, track=str(i), year=jahr, data=frames(30))
            n += 1
    return len(ALBEN), n


if __name__ == '__main__':
    hier = pathlib.Path(__file__).parent
    shutil.rmtree(hier / 'daten', ignore_errors=True)
    print('%d Alben, %d Titel' % baue(hier / 'musik'))
