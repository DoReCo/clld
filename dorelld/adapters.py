from clld import interfaces
from clld.web.adapters.md import BibTex, TxtCitation
from clld.web.adapters.base import Representation

from dorelld.util import get_cite

    # Allows for citations from 'source' objects.
    # APiCS (Atlas of Pidgin and Creole Language Structures) illustrates
    #       how to implement it.
    # We however resort to 'get_cite' ('util.py') for the rendering.
class SourceMetadata(Representation):
    """Metadata?"""
    template = 'md_html.mako'
    mimetype = 'application/vnd.clld.md+xml'
    extension = 'md.html'
class SourceBibTex(BibTex):
    """Bibtex format?"""
    def rec(self, ctx, req):
        return get_cite(ctx.id,ctx,'bibtex')
class SourceReferenceManager(SourceBibTex):
    """RIS format."""
    name = 'RIS'
    __label__ = 'RIS'
    unapi = 'ris'
    extension = 'md.ris'
    mimetype = "application/x-research-info-systems"
    def render(self,ctx,req):
        return get_cite(ctx.id,ctx,'ris')
class SourceTxtCitation(TxtCitation):
    """TXT format?"""
    def render(self,ctx,req):
        return get_cite(ctx.id,ctx,'txt')

def includeme(config):
    pass
    config.register_adapter(SourceMetadata, interfaces.ISource)
    for cls in [SourceBibTex, SourceTxtCitation, SourceReferenceManager]:
        for if_ in [interfaces.IRepresentation, interfaces.IMetadata]:
            config.register_adapter(cls, interfaces.ISource, if_)
