import os

from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Float,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import DBSession, Base, CustomModelMixin
from clld.db.models.common import Language, Contribution, Contributor
from clld.web.util.helpers import external_link, cc_link
from clld.web.util.htmllib import HTML

    # Support functions
def _get_cc(cc,arc="",arc_l=""):
    """Support function ('doreLanguage.lic_link()') to get a nice CC."""
    url = "https://creativecommons.org/licenses/"
    ch = cc.lower()
    if not ch.startswith("cc"):
        if ch == "na":
            return cc
        elif arc == "na":
            return "No audio archive"
        return external_link(arc_l,label="Audio at "+arc)
    ch = ch[3:]
    known = {
        'zero': 'Public Domain',
        'by': 'Creative Commons Attribution License',
        'by-nc': 'Creative Commons Attribution-NonCommercial License',
        'by-nc-nd': 'Creative Commons Attribution-NonCommercial-NoDerivatives'
                    ' License',
        'by-nc-sa': 'Creative Commons Attribution-NonCommercial-ShareAlike'
                    ' License',
        'by-nd': 'Creative Commons Attribution-NoDerivatives License',
        'by-sa': 'Creative Commons Attribution-ShareAlike License'}
    
    img_attrs = dict(
        alt=known[ch],
        src="https://doreco.huma-num.fr/static/cc/" + ch + '.png')
    img_attrs.update(height=15, width=80)
    if not ch == 'zero':
        license_url = url+ch+"/4.0/"
    else:
        license_url = url+ch+"/"
    return HTML.a(HTML.img(**img_attrs), href=license_url,
                  rel='license',target="_blank")

#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
@implementer(interfaces.ILanguage)
class doreLanguage(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)

    family = Column(String); fam_glottocode = Column(String)
    area = Column(String)
    creator = Column(String); date = Column(String)
    archive = Column(String); arclink = Column(String)
    transl = Column(String)
    words = Column(Integer); c_words = Column(Integer)
    spks = Column(Integer); c_spks = Column(Integer)
    texts = Column(Integer); c_texts = Column(Integer)
    gloss = Column(String)
    extended = Column(Boolean)
        # For download
    lic = Column(String); audio_lic = Column(String)
    NAK = Column(String)
    
    def glo_link(self):
        gl = "https://glottolog.org/resource/languoid/id/"
        return external_link(os.path.join(gl,self.id),
                             label=self.id)
    def fam_link(self):
        if not self.fam_glottocode == "na":
            gl = "https://glottolog.org/resource/languoid/id/"
            return external_link(os.path.join(gl,self.fam_glottocode),
                                 label=self.family)
        return self.family
    def arc_link(self):
        if not self.arclink == "na":
            return external_link(self.arclink,label=self.archive)
        return self.archive
    def get_lic(self):
        return _get_cc(self.lic)
    def get_alic(self):
        return _get_cc(self.audio_lic,self.archive,self.arclink)
    def lic_link(self):
        cc1 = self.lic.lower(); cc2 = self.audio_lic.lower()
        res1 = _get_cc(self.lic)
        res2 = _get_cc(self.audio_lic,self.archive,self.arclink)
        if cc1 == cc2:
            return res1
        return (res1, res2)

@implementer(interfaces.IContribution)
class doreContrib(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    
    glottocode = Column(String)
    tname = Column(String)
    spks = Column(String)
    spks_age = Column(String); spks_agec = Column(String)
    spks_sex = Column(String)
    recdate = Column(String); recdatec = Column(String)
    genre = Column(String); subgenre = Column(String)
    gloss = Column(String)
    transl = Column(String)
    sound = Column(String); overlap = Column(String)
    process = Column(String)
    words = Column(Integer)
    extended = Column(Boolean)
        # For download
    NAK = Column(String)
    
@implementer(interfaces.IContributor)
class dorEditor(CustomModelMixin, Contributor):
    pk = Column(Integer, ForeignKey('contributor.pk'), primary_key=True)
    
        # Note: the base class already contains 'url', 'email', 'address'
    team = Column(String)
    function = Column(String)
    
    def name_link(self):
        if self.url == "na":
            return self.name
        else:
            return external_link(self.url,label=self.name)
