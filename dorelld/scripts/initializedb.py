from __future__ import unicode_literals
import sys

from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common

import dorelld
from dorelld.models import doreLanguage
from dorelld.scripts.filltables import cleardb, filltables


def main(args):
    data = Data()

    dataset = common.Dataset(id=dorelld.__name__, domain='dorelld.clld.org')
    DBSession.add(dataset)
        # customize dataset

        # load languages
    for typ,name,tupl in filltables():
        if typ == "languages":
            lat = tupl.get('Latitude',0.0); lon = tupl.get('Longitude',0.0)
            if lat == "na":
                lat = 0.0
            if lon == "na":
                lon = 0.0
            lang = tupl.get('Language',"na"); fam = tupl.get('Family',"na")
            area = tupl.get('Area',"na")
            DBSession.add(doreLanguage(id=name,name=lang,family=fam,
                          area=area,latitude=lat,longitude=lon,
                          creator="na",words=0,spks=0,texts=0,gloss=False))

def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """


if __name__ == '__main__':  # pragma: no cover
    cleardb() # clearing DB first
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
