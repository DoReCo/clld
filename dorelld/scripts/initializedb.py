from __future__ import unicode_literals
import sys

from clld.lib import bibtex
from clld.scripts.util import initializedb, Data, add_language_codes
from clld.db.meta import DBSession
from clld.db.models import common

from datetime import date
import dorelld
from dorelld.models import doreLanguage, doreContrib, dorEditor
from dorelld.scripts.filltables import cleardb, filltables


    # 'main' : initializes the database
    # Don't call directly: requires a DBSession
def _addLang(lp):
    """For a lighter 'main' function and because of checks."""

    for a in range(len(lp)):
        if a == 22:
            if lp[a] == "no":
                lp[a] = False
            else:
                lp[a] = True
        elif a > 19 and (not lp[a] or lp[a] == 'na'): #coordinates
            lp[a] = 0.0
        elif a > 13 and not lp[a]: # words/speakers/texts
            lp[a] = 0
        elif not lp[a]:
            lp[a] = 'na'
    lang = doreLanguage(lp[0],id=lp[0],name=lp[1],family=lp[2],
             fam_glottocode=lp[3],area=lp[4],creator=lp[5],date=lp[6],
             archive=lp[7],arclink=lp[8],transl=lp[9],
             lic=lp[10],audio_lic=lp[11],NAK=lp[12],gloss=lp[13],
             words=lp[14],spks=lp[15],texts=lp[16],
             c_words=lp[17],c_spks=lp[18],c_texts=lp[19],
             latitude=lp[20],longitude=lp[21],extended=lp[22])
    DBSession.add(lang)
    DBSession.flush()
    return lang
def _addText(lp):
    """For a lighter 'main' function and because of checks."""

    for a in range(1,len(lp)):
        if a == 18:
            if lp[a] == "no":
                lp[a] = False
            else:
                lp[a] = True
        elif a == 17:
            if not lp[a] or str(lp[a]).startswith("check"):
                lp[a] = 0
        elif a == 9:
            genre = lp[9].lower()
            if genre == "personal narrative":
                genre = "pers. narr."
            elif genre == "traditional narrative":
                genre = "trad. narr."
            elif genre == "conversation":
                genre = "convers."
            elif genre == "stimulus-based":
                genre = "stimulus"
            lp[9] = genre
        elif not lp[a]:
            lp[a] = 'na'
    DBSession.add(doreContrib(id=lp[1],tname=lp[2],spks=lp[3],spks_age=lp[4],
             spks_agec=lp[5],spks_sex=lp[6],recdate=lp[7],recdatec=lp[8],
             genre=lp[9],subgenre=lp[10],gloss=lp[11],transl=lp[12],
             sound=lp[13],overlap=lp[14],process=lp[15],NAK=lp[16],
             glottocode=lp[0],words=lp[17],extended=lp[18]))
    DBSession.flush()
def _addSource(lp):
    """For a lighter 'main' function."""

    DBSession.add(common.Source(id=lp[0],name=lp[0],
             author=lp[2],year=lp[3],title=lp[4],url=lp[5],note=lp[6]))
    DBSession.flush()
def _addEditor(dataset,count,lp):
    """For a lighter 'main' function."""
    eds = ['Frank Seifart','Ludger Paschen','Matthew Stave']
    ed = dorEditor(id=lp[0],name=lp[0],url=lp[1],email=lp[2],
             address=lp[3],team=lp[4],function=lp[5])
    if lp[0] in eds:
        common.Editor(dataset=dataset,contributor=ed,ord=count+1)
        count += 1
    DBSession.add(ed); DBSession.flush()
    return dataset,count
def _addDataset(data):
    """For a lighter 'main' function."""

    dataset = common.Dataset(
        id=dorelld.__name__,
        name="DoReCo",
        domain='doreco.info',
        description=('DoReCo'), # name for citation?
        published=date(2020,9,1), # date
        contact='dorecoproject@gmail.com', # mail
        publisher_name='',
        publisher_place='',
        #license='http://creativecommons.org/licenses/by/4.0/',
        #jsondata={
        #    'license_icon': 'cc-by.png',
        #    'license_name': ('Creative Commons ' +
        #    'Attribution 4.0 International License')
        #    }
        )
    return dataset
def main(args):
    """Fills the database with data retrieved from tabular files.
    'filltables()' iterates over each row of each table.
    'typ' is the name of the table, 'name' a key column and 'tupl'
    the other columns as a dict {column_name,cell_value}."""

    data = Data(); count = 0
        # dataset
    dataset = _addDataset(data)
        # load languages
    for typ,name,tupl in filltables():
        if not name or name == "na":
            continue
        #TODO we exclude non core language
        if typ == "languages" and tupl.get('Id').startswith('L_'):
            #print(name, tupl)
            lang = _addLang([name,tupl.get('Language',"na"),
                     tupl.get('Family',"na"),
                     tupl.get('fam_glottocode',""),
                     tupl.get('Area',"na"),
                     tupl.get('Creator',"na"),
                     tupl.get('Date',"na"),
                     tupl.get('Archive',"na"),
                     tupl.get('Archive_link',"na"),
                     tupl.get('Translation',"na"),
                     tupl.get('License',"na"),
                     tupl.get('Audio license',"na"),
                     tupl.get('NAKALA',"na"),
                     tupl.get('Gloss',"na"),
                     tupl.get('Words',0),
                     tupl.get('Speakers',0),
                     tupl.get('Texts',0),
                     tupl.get('Core words',0),
                     tupl.get('Core speakers',0),
                     tupl.get('Core texts',0),
                     tupl.get('Latitude',0.0),
                     tupl.get('Longitude',0.0),
                     tupl.get('Extended',"no")])
            add_language_codes(data, lang,tupl.get('iso-639-3'),
                               glottocode=name)
        elif typ == "editors":
            dataset,count = _addEditor(dataset,count,[name,
                     tupl.get('url',"na"),
                     tupl.get('email',"na"),
                     tupl.get('address',"na"),
                     tupl.get('team',"na"),
                     tupl.get('function',"na")])
        elif typ == "sources":
            _addSource([name,tupl.get('bibtex_type',"na"),
                     tupl.get('author',"na"),
                     tupl.get('year',"na"),
                     tupl.get('title',"na"),
                     tupl.get('url',"na"),
                     tupl.get('note',"na")])
        else:
            #TODO for texts, we exclude delete and so on in column extended
            if tupl.get('extended') in ['no', 'yes']:
                #if typ=='dolg1241' : print(tupl):''
                _addText([typ,name,tupl.get('name',"na"),
                     tupl.get('spk_code',"na"),
                     tupl.get('spk_age','0'),
                     tupl.get('spk_age_c',"na"),
                     tupl.get('spk_sex',"na"),
                     tupl.get('rec_date',"na"),
                     tupl.get('rec_date_c',"na"),
                     tupl.get('genre',"na"),
                     tupl.get('genre_stim',"na"),
                     tupl.get('gloss',"na"),
                     tupl.get('transl',"na"),
                     tupl.get('sound',"na"),
                     tupl.get('overlap',"na"),
                     tupl.get('processed',"na"),
                     tupl.get('nakala',"na"),
                     tupl.get('words',0),
                     tupl.get('extended',"no")])
        # dataset
        # Note: needs to run after loading (for editors)

    DBSession.add(dataset); DBSession.flush()

    # unused
def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """

    # clears then initializes the database
if __name__ == '__main__':  # pragma: no cover
    cleardb() # clearing DB first
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
