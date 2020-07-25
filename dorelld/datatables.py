
"""
Contains 'datatables' for actual data display on the website.

Classes:
'doreCol'		: basically a 'LinkCol' to open a language page.
'Languages'		: the table of all languages
'Contributions'	: the table of all texts
                  > texts are filtered by glottocode
                  
Defs:
'__init__'		: needed to pass **kwargs for 'base_query'
'base_query'	: filters the content to display
'col_defs'		: the columns displayed
"""

from clld.web import datatables
from clld.web.datatables.base import DataTable, Col, IdCol, LinkCol, ExternalLinkCol
from clld.web.util.helpers import (
	link, button, icon, JS_CLLD, external_link, linked_references, JSDataTable,
)
#from clld.web.util.helpers import link
#from clld.web.util.htmllib import HTML

from clld.db.models.common import Language, Contribution
from dorelld.models import doreLanguage, doreContrib

class doreCol(Col):
    def format(self, item):
        obj = self.get_obj(item)
        return link(self.dt.req, obj, **self.get_attrs(item)) if obj else ''
    
    def get_attrs(self, item):
        return {'label': getattr(self.get_obj(item),self.name)}

class Languages(datatables.Languages):
    def col_defs(self):
        return [
            doreCol(self,'name', sTitle="Language",
                     model_col=doreLanguage.name),
            Col(self,'id', sTitle="Glottocode",
                     format=lambda i: i.glo_link()),
            Col(self,'family', sTitle="Family",
                     format=lambda i: i.fam_link()),
            Col(self,'area', sTitle="Area",
                     model_col=doreLanguage.area),
            Col(self,'creator', sTitle="Creator(s)",
                     model_col=doreLanguage.creator),
            Col(self,'words', sTitle="Words",
                     model_col=doreLanguage.words),
            Col(self,'spks', sTitle="Spk\'s",
                     model_col=doreLanguage.spks),
            Col(self,'texts', sTitle="Texts",
                     model_col=doreLanguage.texts),
            Col(self,'gloss', sTitle="Gloss",
                     model_col=doreLanguage.gloss),
        ]
class Contributions(datatables.Contributions):
        # All of this just to parse the data
    __constraints__ = [doreContrib]
    def __init__(self, req, model, **kw):
        super().__init__(req,model,**kw)
        self.glottocode = kw.pop('glottocode',req.params.get('__eid__',None))
        if self.glottocode:
            self.eid = self.glottocode
    def base_query(self,query):
        if self.glottocode:
            query = query.filter(doreContrib.glottocode == self.glottocode)
        return query
    
        # Actual display
    def col_defs(self):
        return [
            Col(self,'tname', sTitle="File name",
                     model_col=doreContrib.tname),
            Col(self,'spks_age', sTitle="Speaker age",
                     input_size='mini',
                     model_col=doreContrib.spks_age),
            Col(self,'spks_sex', sTitle="Speaker gender",
                     input_size='mini',
                     model_col=doreContrib.spks_sex),
            #Col(self,'recdate', sTitle="Recording date",
            #         model_col=doreContrib.recdate),
            Col(self,'genre', sTitle="Genre",
                     model_col=doreContrib.genre),
            Col(self,'gloss', sTitle="Gloss",
                     model_col=doreContrib.gloss),
            #Col(self,'sound', sTitle="Sound quality",
            #         model_col=doreContrib.sound),
            Col(self,'words', sTitle="Words",
                     model_col=doreContrib.words),
        ]

def includeme(config):
    config.register_datatable('languages', Languages)
    config.register_datatable('contributions', Contributions)
