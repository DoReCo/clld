from __future__ import unicode_literals
import sys

from clld.scripts.util import initializedb, Data, add_language_codes
from clld.db.meta import DBSession
from clld.db.models import common

from datetime import date
import dorelld
from dorelld.models import doreLanguage, doreContrib
from dorelld.scripts.filltables import cleardb, filltables

    # 'main' : initializes the database
    # Don't call directly: requires a DBSession
def _addLang(lp):
    """For a lighter 'main' function and because of checks."""
    
    for a in range(len(lp)):
        if a == 18:
            if lp[a] == "no":
                lp[a] = False
            else:
                lp[a] = True
        elif a > 15 and (not lp[a] or lp[a] == 'na'): #coordinates
            lp[a] = 0.0
        elif a > 9 and not lp[a]: # words/speakers/texts
            lp[a] = 0
        elif not lp[a]:
            lp[a] = 'na'
    lang = doreLanguage(lp[0],id=lp[0],name=lp[1],family=lp[2],
             fam_glottocode=lp[3],area=lp[4],creator=lp[5],
             archive=lp[6],arclink=lp[7],transl=lp[8],gloss=lp[9],
             words=lp[10],spks=lp[11],texts=lp[12],
             c_words=lp[13],c_spks=lp[14],c_texts=lp[15],
             latitude=lp[16],longitude=lp[17],extended=lp[18])
    DBSession.add(lang)
    DBSession.flush()
    return lang
def _addText(lp):
    """For a lighter 'main' function and because of checks."""

    for a in range(1,len(lp)):
        if a == 16:
            if lp[a] == "no":
                lp[a] = False
            else:
                lp[a] = True
        elif a == 15 and not lp[a]:
            lp[a] = 0
        elif not lp[a]:
            lp[a] = 'na'
    DBSession.add(doreContrib(id=lp[1],tname=lp[2],spks=lp[3],spks_age=lp[4],
             spks_agec=lp[5],spks_sex=lp[6],recdate=lp[7],recdatec=lp[8],
             genre=lp[9],subgenre=lp[10],gloss=lp[11],transl=lp[12],
             sound=lp[13],process=lp[14],words=lp[15],glottocode=lp[0],
             extended=lp[16]))
    DBSession.flush()
def _addDataset(data):
    """For a lighter 'main' function."""
    
    dataset = common.Dataset(
        id=dorelld.__name__,
        name="DoReCo",
        domain='doreco.info',
        description=('DoReCo: Language Documentation Reference Corpora'),
        published=date(2020,9,1), # date
        contact='thisisamail@nowhere.lo', # mail
        publisher_name='DDL, ZAS',
        publisher_place='Lyon, Berlin',
        publisher_url='https://anr.fr/Projet-ANR-18-FRAL-0010',
        license='http://creativecommons.org/licenses/by/4.0/',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': ('Creative Commons ' +
            'Attribution 4.0 International License')
            }
        )
        # Contributors/editors
    eds = [('seifartfrank','Frank Seifart'),
           ('pellegrinofrancois','François Pellegrino')]
    for i, (id_,name) in enumerate(eds):
        ed = data.add(common.Contributor,id_,id=id_,name=name)
        common.Editor(dataset=dataset,contributor=ed,ord=i+1)
    del eds
    DBSession.add(dataset); DBSession.flush()
def main(args):
    data = Data()
        # dataset
    _addDataset(data)

        # load languages
    for typ,name,tupl in filltables("/home/doreco/dorelld/tables"):
        if typ == "languages":
            lang = _addLang([name,tupl.get('Language',"na"),
                     tupl.get('Family',"na"),
                     tupl.get('fam_glottocode',""),
                     tupl.get('Area',"na"),
                     tupl.get('Creator',"na"),
                     tupl.get('Archive',"na"),
                     tupl.get('Archive_link',"na"),
                     tupl.get('Translation',"na"),
                     tupl.get('Gloss',"na"),
                     tupl.get('Words',0),
                     tupl.get('Speakers',0),
                     tupl.get('Texts',0),
                     tupl.get('coreWords',0),
                     tupl.get('coreSpeakers',0),
                     tupl.get('coreTexts',0),
                     tupl.get('Latitude',0.0),
                     tupl.get('Longitude',0.0),
                     tupl.get('extended',"no")])
            add_language_codes(data, lang,tupl.get('iso-639-3'),
                               glottocode=name)
        else:
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
                     tupl.get('processed',"na"),
                     tupl.get('words',0),
                     tupl.get('extended',"no")])
                     
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
