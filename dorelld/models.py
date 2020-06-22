from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Float,
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
from clld.db.models.common import Language


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
@implementer(interfaces.ILanguage)
class doreLanguage(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)

    family = Column(String)
    area = Column(String)
    creator = Column(String)
    words = Column(Integer)
    spks = Column(Integer)
    texts = Column(Integer)
    gloss = Column(Boolean)

