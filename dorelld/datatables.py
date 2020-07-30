from clld.web import datatables
from clld.web.datatables.base import Col, IdCol, LinkCol, ExternalLinkCol
from clld.web.util.helpers import (
    link, button, icon, JS_CLLD, external_link, linked_references, JSDataTable,
)
#from clld.web.util.helpers import link
#from clld.web.util.htmllib import HTML
from clldutils.misc import dict_merged

from clld.db.models.common import Language, Contribution
from dorelld.models import doreLanguage, doreContrib

class doreCol(Col):
    def format(self, item):
        obj = self.get_obj(item)
        return link(self.dt.req, obj, **self.get_attrs(item)) if obj else ''

    def get_attrs(self, item):
        return {'label': getattr(self.get_obj(item),self.name)}

class Languages(datatables.Languages):
    def __init__(self, req, model, **kw):
        super().__init__(req,model,**kw)
        self.extended = kw.pop('extended',req.params.get('extended',"False"))
        if self.extended == "True":
            self.eid = self.eid+"ext"
    def xhr_query(self):
        return dict_merged(super(Languages, self).xhr_query(),
                           extended=self.extended)
        # Actual display
    def col_defs(self):
        words = doreLanguage.words; spks = doreLanguage.spks
        texts = doreLanguage.texts
        if self.extended == "False":
            words = doreLanguage.c_words; spks = doreLanguage.c_spks
            texts = doreLanguage.c_texts
        return [
            doreCol(self,'name', sTitle="Language",
                     model_col=doreLanguage.name),
            doreCol(self,'id', sTitle="Glottocode",
                     model_col=doreLanguage.id),
            Col(self,'family', sTitle="Family",
                     format=lambda i: i.fam_link()),
            Col(self,'area', sTitle="Area",
                     model_col=doreLanguage.area),
            Col(self,'creator', sTitle="Creator(s)",
                     model_col=doreLanguage.creator),
            Col(self,'words', sTitle="Words",
                     model_col=words),
            Col(self,'spks', sTitle="Spk\'s",
                     model_col=spks),
            Col(self,'texts', sTitle="Texts",
                     model_col=texts),
            Col(self,'gloss', sTitle="Gloss",
                     model_col=doreLanguage.gloss),
        ]

class Contributions(datatables.Contributions):
        # All of this just to parse the data
    __constraints__ = [doreContrib]
    def __init__(self, req, model, **kw):
        super().__init__(req,model,**kw)
        self.glottocode = kw.pop('glottocode',req.params.get('glottocode',""))
        self.extended = kw.pop('extended',req.params.get('extended',"False"))
        if self.extended == "True":
            self.eid = self.eid+"ext"
    def xhr_query(self):
        return dict_merged(super(Contributions, self).xhr_query(),
                           glottocode=self.glottocode,
                           extended=self.extended)
    def base_query(self,query):
        if self.glottocode:
            query = query.filter(doreContrib.glottocode == self.glottocode)
        if self.extended == "False":
            query = query.filter(doreContrib.extended == False)
        return query
        # Actual display
    def col_defs(self):
        return [
            Col(self,'tname', sTitle="Name",
                     model_col=doreContrib.tname),
            Col(self,'spks_age', sTitle="Speaker Age",
                     model_col=doreContrib.spks_age),
            Col(self,'spks_sex', sTitle="Speaker Gender",
                     model_col=doreContrib.spks_sex),
            #Col(self,'recdate', sTitle="Recording date",
            #         model_col=doreContrib.recdate),
            Col(self,'genre', sTitle="Genre",
                     model_col=doreContrib.genre),
            Col(self,'gloss', sTitle="Gloss",
                     model_col=doreContrib.gloss),
            #Col(self,'transl', sTitle="Translation",
            #         model_col=doreContrib.transl),
            #Col(self,'sound', sTitle="Sound quality",
            #         model_col=doreContrib.sound),
            Col(self,'words', sTitle="Words",
                     model_col=doreContrib.words),
        ]

def includeme(config):
    config.register_datatable('languages', Languages)
    config.register_datatable('contributions', Contributions)
