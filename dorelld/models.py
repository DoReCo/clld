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
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import Language, Contribution
from clld.web.util.helpers import external_link


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
@implementer(interfaces.ILanguage)
class doreLanguage(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)

    family = Column(String)
    fam_glottocode = Column(String)
    area = Column(String)
    creator = Column(String)
    archive = Column(String)
    arclink = Column(String)
    transl = Column(String)
    words = Column(Integer); c_words = Column(Integer)
    spks = Column(Integer); c_spks = Column(Integer)
    texts = Column(Integer); c_texts = Column(Integer)
    gloss = Column(String)
    extended = Column(Boolean)
        # For download
    lic = Column(String); audio_lic = Column(String)
    NAK = Column(String)
    
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

@implementer(interfaces.IContribution)
class doreContrib(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    
    glottocode = Column(String)
    tname = Column(String)
    spks = Column(String)
    spks_age = Column(String)
    spks_agec = Column(String)
    spks_sex = Column(String)
    recdate = Column(String)
    recdatec = Column(String)
    genre = Column(String)
    subgenre = Column(String)
    gloss = Column(String)
    transl = Column(String)
    sound = Column(String)
    process = Column(String)
    words = Column(Integer)
    extended = Column(Boolean)
        # For download
    NAKwav = Column(String); NAKpraat = Column(String)
    NAKelan = Column(String); NAKtab = Column(String); NAKtei = Column(String)
    NAKcross1 = Column(String); NAKcross2 = Column(String)
    NAKcross3 = Column(String)
    
