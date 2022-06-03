from sqlalchemy.orm import joinedload
from clld.web import datatables
from clld.web.datatables.base import Col, IdCol, LinkCol, ExternalLinkCol
from clld.web.util.helpers import (
    link, button, icon, JS_CLLD, external_link, linked_references, JSDataTable,
)
#from clld.web.util.helpers import link
#from clld.web.util.htmllib import HTML
from clldutils.misc import dict_merged

from clld.db.models.common import Language, Contribution
from dorelld.models import doreLanguage, doreContrib, dorEditor

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
            Col(self,'id', sTitle="Glottocode",
                     format=lambda i: i.glo_link()),
            Col(self,'family', sTitle="Family",
                     format=lambda j: j.fam_link()),
            Col(self,'area', sTitle="Area",
                     model_col=doreLanguage.area),
            Col(self,'creator', sTitle="Creator(s)",
                     model_col=doreLanguage.creator),
            Col(self,'lic', sTitle="License(s)",
                     format=lambda k: k.lic_link(),
                     bSearchable=False, bSortable=False),
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
            #Col(self,'wave', sTitle="Text annotation",
            #         model_col=doreContrib.NAK, format=ExternalLinkCol),
        ]

def ExternalLinkCol(value):
    handle = getattr(value, 'NAK')
    #TODO make parser ready to live
    result = ''
    if handle !='na':
        result = '<a href="https://test.nakala.fr/' + handle + '" title="data repository" target="_BLANK"><img style="height:2vh;" src="https://nakala.fr/build/images/nakala.png" alt="' + handle + '"/></a>'
    return result

    parse_handle = handle.split('test.nakala.fr/')
    if len(parse_handle) > 1 :
        handle = parse_handle[1]
        #TODO change the url to nakala, not test server
        result = '<a href="https://test.nakala.fr/' + handle + '" title="data repository" target="_BLANK"><img style="height:2vh;" src="https://nakala.fr/build/images/nakala.png" alt="' + handle + '"/></a>'
    else:
        result = handle
    return result
class Contributors(datatables.Contributors):
    def __init__(self, req, model, **kw):
        super().__init__(req,model,**kw)
        self.team = kw.pop('team',req.params.get('team',""))
        self.status = kw.pop('status',req.params.get('status',""))
        if self.team:
            self.eid = self.eid+self.team
    def base_query(self,query):
        if self.team:
            query = query.filter(dorEditor.team == self.team)
        if self.status:
            query = query.filter(dorEditor.status == self.status)
        return query
    def xhr_query(self):
        return dict_merged(super(Contributors, self).xhr_query(),
                           team=self.team,
                           status=self.status)
        # Actual display
    def col_defs(self):
        cols = [Col(self,'name', sTitle="Members",
                     format=lambda i: i.name_link())]
        if not self.team:
            cols.append(Col(self,'team', sTitle="Team",
                     model_col=dorEditor.team))
        if not self.status:
            cols.append(Col(self,'function', sTitle="Status",
                     model_col=dorEditor.function))
        return cols

def includeme(config):
    config.register_datatable('languages', Languages)
    config.register_datatable('contributions', Contributions)
    config.register_datatable('contributors', Contributors)
