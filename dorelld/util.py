from clld.web.util.htmllib import HTML, literal
from clld.web.util import helpers

from datetime import datetime

    ## A download form for all pages
    # 'full'    : displays the full form or (False) just the button
    #             default values then are 'wav=True&format=all'
def get_form(lang_n="",ext=False, full=True):
    """Provides a download form.
    ARGUMENTS:
    - 'lang_n'      :   the glottocode
    - 'ext'         :   if for the extended corpus
    - 'full'        :   if all fields (or just the button)"""
    
    style = ("<style>"
     "form {float: left; margin: 0px; padding: 0px;} "
     "input {float: left; margin-right: 10px;} "
     "select {float: left; margin-right: 10px;} "
     "label {float: left; margin-right: 10px;} "
     "p.form {float: left; margin-right: 10px; padding: 3px;} "
     "p.citeb {float: right;}"
     "</style>")
    lang = ("<input type=\"hidden\" id=\"f_id\" "
            "name=\"id\" value=\""+lang_n+"\">")
    wav = ""; form = ""; text = ""
    if full:
        if lang_n.lower() == 'languages':
            wav = ("<input type=\"hidden\" id=\"f_wav\" "
                   "name=\"wav\" value=\"False\">")
        else:
            wav = ("<input type=\"checkbox\" id=\"f_wav\" name=\"wav\" "
                   "value=\"WAV\"><label for=\"f_wav\">WAV</label>")
        form = ("<select id=\f_format\" name=\"format\">"
          "<option value=\"all\">All types</option>"
          "<option value=\"praat\">Praat (.TextGrid)</option>"
          "<option value=\"elan\">Elan (.eaf)</option>"
          "<option value=\"tabular\">Tabular (.csv)</option>"
          "<option value=\"tei\">TEI (.xml)</option>"
          "<option value=\"cross1\">Crosstable_1</option>"
          "<option value=\"cross2\">Crosstable_2</option>"
          "<option value=\"cross3\">Crosstable_3</option></select>")
    else:
        wav = ("<input type=\"hidden\" id=\"f_wav\" "
               "name=\"wav\" value=\"True\">")
        form = ("<input type=\"hidden\" id=\"f_format\" "
               "name=\"format\" value=\"all\">")
    if ext and not ext == "False":
        ext = ("<input type=\"hidden\" id=\"f_ext\" "
               "name=\"extended\" value=\"True\">")
        text = ("<p class=\"form\"><b>Download all files:</b></p>")
    else:
        ext = ("<input type=\"hidden\" id=\"f_ext\" "
               "name=\"extended\" value=\"False\">")
        text = ("<p class=\"form\"><b>Download all core files:</b></p>")
    submit = "<input type=\"submit\" value=\"Download\">"
    if full:
        return literal(style+text+"<form method=\"post\" action=\"/doreLoad\">"
            +ext+lang+wav+form+submit+"</form>")
    else:
        return literal(style+"<form method=\"post\" action=\"/doreLoad\">"
            +ext+lang+wav+form+submit+"</form>")

    ## A citation string 
    # provides a citation in formats 'txt/bibtex/ris' (following WALS)
def get_author(author,type):
    """Support function ('get_cite') to get a nice author format."""
    
    l_auth = []
        # Turning a string into a list
    if ";" in author: # normalized
        l_auth = author.split(";")
    else:                  # guessing
        for el1 in author.split("&"):
            for el2 in el1.split(","):
                for el3 in el1.split(" and "):
                    l_auth.append(el3)
        # Turning that list back into a formatted string
    auth = ""; la = len(l_auth)
    if type == "txt" or type == "bibtex":
        auth = l_auth[0].rsplit(" ",1)
        if len(auth) > 1:
            auth = auth[1]+", "+auth[0]
        else:
            auth = auth[0]
        for a in range(1,la-1):
            auth = auth + "," + l_auth[a]
        if la > 1:
            auth = auth + " &" + l_auth[-1]
    elif type == "ris":
        auth = []
        for author in l_auth:
            author = author.rsplit(" ",1)
            if len(author) > 1:
                author = author[1]+", "+author[0]
            auth.append(author)
    return auth
def get_cite(name,sour,type="txt",dflt=True,us=False):
    """Generates a DoReCo citation.
    ARGUMENTS:
    - 'name'        :   name of the language / thingy.
    - 'sour'        :   a 'Source' object.
    - 'type'        :   txt,bibtex,ris
    - 'dflt'        :   using the DoReCo default template
    RETURNS:
    - cite          :   (str) the citation in 'txt/bibtext/ris' format."""
    
        # DoReCo main reference
    doauth = "Frank Seifart; Ludger Paschen; Matthew Stave"
    doauth = get_author(doauth,type)
    dotitle = "Language Documentation Reference Corpus (DoReCo) 1.0"
    doloc = "Berlin & Lyon"
    doedit = ("Leibniz-Zentrum Allgemeine Sprachwissenschaft & "
               "Université de Lyon/CNRS-DDL")
        # 'sour' reference
        ## authors
    auth = get_author(sour.author,type)
        ## year, title, link, access date
    year = sour.year; title = ""
    title = sour.title
    link = sour.url
    if us:
        access = datetime.now().strftime("%m/%d/%Y")
    else:
        access = datetime.now().strftime("%m/%d/%Y")
        ## We return
    if dflt:
        if type == "txt":
            return ("{}. {}. {}. In {} (eds.). {}. {}: {}. "
                    "&lt;{}&gt;. (Accessed on {})."
                    .format(auth,year,title,doauth,dotitle,doloc,doedit,
                            link,access))
        elif type == "bibtex":
            return ("@incollection{doreco-"+sour.id+",\n  address   = "
                    +doloc+",\n  author    = "+auth+",\n  booktitle = "
                    +dotitle+",\n  editor    = "+doauth+",\n  publisher = "
                    +doedit+",\n  title     = "+title+",\n  url       = "
                    +link+",\n  urldate   = "+access+",\n  year      = "
                    +year+",\n}")
        elif type == "ris":
            txt = "TY  - CHAP\n"
            for author in auth:
                txt = txt + "AU  - "+author+"\n"
            for editor in doauth:
                txt = txt + "ED  - "+editor+"\n"
            compl = ("PY  - {0}\nDA  - {0}//\nTI - {1}\nBT  - {2}\n"
                     "PB  - {3}\nCY  - {4}\nUR  - {5}\nID  - doreco-{6}\n"
                     "ER  - "
                     .format(year,title,dotitle,doedit,doloc,link,sour.id))
            return txt+compl

    ## A language 'description'
    # 
def get_desc(ctx,sour,dflt=True,us=False):
    """Provides a language description."""
    
    style = ("<style>p.cite {padding-left: 25px; text-indent: -15px; "
             "font-size: 90%;}</style></style>")
    text = ("<p>The {} DoReCo data set was compiled by {} in 2015-2015 "
            "and further processed by the DoReCo team in 2020-2022."
            .format(ctx.name,ctx.creator))
    arch = ""
    if not ctx.arclink == "na":
        arch = ("A larger collection of Pavel Ozerov's {} data is archived "
                "at {}.".format(ctx.name,literal(ctx.arc_link())))
    return literal(text + arch + (" A set of files with further information "
            "on the {0} DoReCo data set, including metadata and PIDs is "
            "automatically included in each download of Anal DoReCo files.</p>"
            "<p>The {0} DoReCo data set should be cited as follows "
            "(a BibTex version of this citation is provided below):</p>"
            "<p class=\"cite\">{1}</p><p class>Please note that when citing "
            "this data set, or any number of DoReCo data sets, it is NOT "
            "sufficient to refer to DoReCo (and its editors) as a whole, "
            "but the full citation for each individual data set must be "
            "provided, including the names of the creators of each data "
            "set.</p>".format(ctx.name,"[insert citation]")))
   



