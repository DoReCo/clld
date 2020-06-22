from clld.web import datatables
from clld.web.datatables.base import Col, IdCol, LinkCol, ExternalLinkCol
#from clld.web.util.helpers import link
#from clld.web.util.htmllib import HTML

class Languages(datatables.Languages):
    def col_defs(self):
        return [
            Col(self,'name', sTitle='Language'),
            IdCol(self,'id', sTitle='Glottocode'),
            Col(self,'family', sTitle='Family'),
            Col(self,'area', sTitle='Area'),
            Col(self,'creator', sTitle='Creator(s)'),
            Col(self,'words', sTitle='Words'),
            Col(self,'spks', sTitle='Spk\'s'),
            Col(self,'texts', sTitle='Texts'),
            Col(self,'gloss', sTitle='Gloss'),
        ]

def includeme(config):
    config.register_datatable('languages', Languages)
