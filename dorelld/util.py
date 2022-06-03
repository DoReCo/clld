import clld.db.models
from clld.web.util.htmllib import HTML, literal
from clld.web.util import helpers
from clld.web.datatables.base import DataTable
from datetime import datetime

from clld.db.meta import DBSession

from clld.db.models import Language, Source
from dorelld.models import doreLanguage


## A download form for all pages
# 'full'    : displays the full form or (False) just the button
#             default values then are 'wav=True&format=all'
# import dorelld.dorelld.models

def get_button(lang_n="", isExtended=False, full=True):
    """Provides a download form.
    ARGUMENTS:
    - 'lang_n'      :   the glottocode
    - 'ext'         :   if for the extended corpus
    - 'full'        :   if all fields (or just the button)"""
    xml = "<span class='span2' style='margin-left:0px'>no xml</span>"
    wav_size = 0
    eaf_size = 0
    tg_size = 0
    xml_size = 0
    tsv_size = 0
    txt = "<span class='span2' style='margin-left:0px'>Dataset files :</span>"
    wav = "<span class='span2' style='margin-left:0px'>" \
              "<button class='btn btn-warning' value='wav' name='format' type='input'>WAV</button> " + str(wav_size) + " MB</span>"
    eaf = "<span class='span2' style='margin-left:0px'>" \
          "<button class='btn btn-primary' value='eaf' name='format' type='input'>eaf</button> " + str(eaf_size) + " MB</span>"
    textgrid = "<span class='span2' style='margin-left:0px'>" \
               "<button class='btn btn-danger' value='textgrid' name='format' type='input'>TextGrid</button> " + str(tg_size) + " MB</span>"
    if xml_size>0:
        xml = "<span class='span2' style='margin-left:0px'>" \
          "<button class='btn btn-info' value='xml' name='format' type='input'>eaf</button> " + str(xml_size) + " MB</span>"
    tsv = "<span class='span2' style='margin-left:0px'>" \
          "<button class='btn btn-info' value='tsv' name='format' type='input'>eaf</button> " + str(tsv_size) + " MB</span>"

    form = "<form method=\"post\" action=\"/doreLoad\" style='margin:0px;line-height:3em;'>" + \
           "<input type=\"hidden\" id=\"f_id\" " "name=\"id\" value=\"" + lang_n + "\">" + \
           "<input type=\"hidden\" id=\"f_ext\" name=\"extended\" value=\"" + str(isExtended) + "\">"
    if isExtended:
        return literal(form + txt + eaf + "</form>")
    else:
        return literal(form + txt + wav + eaf + textgrid + xml + tsv + "</form>")

def get_form(lang_n="", isExtended=False, full=True):
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
            "name=\"id\" value=\"" + lang_n + "\">")
    wav = ""
    form = ""
    text = ""
    ext = ""
    if full:
        if lang_n.lower() == 'languages':
            wav = ("<input type=\"hidden\" id=\"f_wav\" "
                   "name=\"wav\" value=\"False\">")
        else:
            wav = ("<input type=\"checkbox\" id=\"f_wav\" name=\"wav\" "
                   "value=\"True\"><label for=\"f_wav\">WAV</label>")
    else:
        wav = ("<input type=\"hidden\" id=\"f_wav\" "
               "name=\"wav\" value=\"True\">")
        form = ("<input type=\"hidden\" id=\"f_format\" "
                "name=\"format\" value=\"all\">")
    if isExtended and not isExtended == "False":
        ext = ("<input type=\"hidden\" id=\"f_ext\" "
               "name=\"extended\" value=\"True\">")
        text = ("<p class=\"form\"><b>Download all files:</b></p>")
        form = ("<select id=\f_format\" name=\"format\">"
                "<option value=\"elan\">Elan (.eaf)</option></select>")
    else:
        ext = ("<input type=\"hidden\" id=\"f_ext\" "
               "name=\"extended\" value=\"False\">")
        text = ("<p class=\"form\"><b>Download all core files:</b></p>")
        form = ("<select id=\f_format\" name=\"format\">"
                "<option value=\"all\">All types</option>"
                "<option value=\"praat\">Praat (.TextGrid)</option>"
                "<option value=\"elan\">Elan (.eaf)</option></select>")
        # "
        # "<option value=\"tabular\">Tabular (.csv)</option>"
        # "<option value=\"tei\">TEI (.xml)</option>"
        # "<option value=\"MAUS\">MAUS parameters</option>
    submit = "<input type=\"submit\" value=\"Download\">"
    wav = ""
    audio = (
        "<p><a href='mailto:dorecoproject@gmail.com?subject=[doreco]Audio files for'>contact us</a> if you are interested in downloading all the audio files as a zip archive.</p>")
    # TODO audio license, do we exclude the audio for TLA archive too ?
    if lang_n == 'languages':
        audio = ('<p>Not all audio are available. Please check languages individually</p>')
    else:
        statement = DBSession.query(doreLanguage) \
            .filter(Language.id == lang_n).first()
        # print('toto', lang_n, statement)
        if statement:
            audioLicense = statement.audio_lic
            if audioLicense == 'audio linked':
                audio = ("<p>See archive for the audio files.</p>")
            if statement.AUDIO is not None and statement.AUDIO != 'na':
                audio = '<a style="display:block" href="https://test.nakala.fr/' + \
                        statement.AUDIO + '" target="_BLANK">direct link to audios</a>'
    if isExtended==True:
        audio = ''

    if full:
        return literal(style + audio + text + "<form method=\"post\" action=\"/doreLoad\">"
                       + ext + lang + wav + form + submit + "</form>")
    else:
        return literal(style + "<form method=\"post\" action=\"/doreLoad\">"
                       + ext + lang + wav + form + submit + "</form>")

    ## A citation string
    # provides a citation in formats 'txt/bibtex/ris' (following WALS)


def get_author(author, type):
    """Support function ('get_cite') to get a nice author format."""

    l_auth = []
    # Turning a string into a list
    if ";" in author:  # normalized
        l_auth = author.split(";")
    else:  # guessing
        for el1 in author.split("&"):
            for el3 in el1.split(" and "):
                l_auth.append(el3)
        # Turning that list back into a formatted string
    l_auth = list(set(l_auth))
    auth = "";
    la = len(l_auth)
    if type == "txt":
        for a in range(0, la):
            auth = l_auth[a].rsplit(",", 1)
            if len(auth) == 1:
                auth = l_auth[a].rsplit(" ", 1)
                l_auth[a] = (auth[-1].strip() + ", " + auth[0].strip())
            else:
                l_auth[a] = auth[-1].strip() + " " + auth[0].strip()
            l_auth[a] = l_auth[a].strip()
        last = l_auth.pop()
        auth = ', '.join(l_auth)
        if auth:
            auth += ' and ' + last
        else:
            auth = last
    if type == "bibtex":
        for a in range(0, la):
            auth = l_auth[a].rsplit(",", 1)
            if len(auth) == 1:
                auth = l_auth[a].rsplit(" ", 1)
                l_auth[a] = (auth[1].strip() + ", " + auth[0].strip())
            l_auth[a] = l_auth[a].strip()
        auth = ' and '.join(l_auth)
        # for a in range(1,la-1):
        #    auth = auth + " and" + l_auth[a]
        # if la > 1:
        #    auth = auth + " and" + l_auth[-1]
    elif type == "ris":
        auth = []
        for author in l_auth:
            author_part = author.rsplit(",", 1)
            if len(author_part) == 1:
                author_part = author.rsplit(" ", 1)
                author = (author_part[1].strip() + ", " + author_part[0].strip())
            author = author.strip()
            auth.append(author)
    return auth


def sanitize(input_string):
    output_string = ''
    for i in input_string:
        if i == '&':
            outchar = '\&'
        else:
            outchar = i
        output_string += outchar
    return output_string


def get_cite(name, sour, type="txt", dflt=True, us=False):
    """Generates a DoReCo citation.
    ARGUMENTS:
    - 'name'        :   name of the language / thingy.
    - 'sour'        :   a 'Source' object.
    - 'type'        :   txt,bibtex,ris
    - 'dflt'        :   using the DoReCo default template
    RETURNS:
    - cite          :   (str) the citation in 'txt/bibtext/ris' format."""

    # DoReCo main reference
    doauth = "Frank Seifart; Paschen, Ludger ; Matthew Stave"
    doauth = get_author(doauth, type)
    dotitle = ("Language Documentation Reference Corpus (DoReCo) 1.0")
    doloc = ("Berlin & Lyon")
    doedit = ("Leibniz-Zentrum Allgemeine Sprachwissenschaft & "
              # "Université de Lyon/CNRS-DDL")
              "laboratoire Dynamique Du Langage (UMR5596, CNRS & Université Lyon 2)")
    # 'sour' reference
    ## authors
    auth = get_author(sour.author, type)
    ## year, title, link, access date
    year = sour.year;
    title = ""
    title = sour.title
    link = sour.url
    if us:
        access = datetime.now().strftime("%m/%d/%Y")
        month, day, year = access.split("/")
        raccess = year + "/" + month + "/" + day
    else:
        access = datetime.now().strftime("%d/%m/%Y")
        day, month, year = access.split("/")
        raccess = year + "/" + month + "/" + day
        ## We return
    if dflt:
        if type == "txt":
            return ("{}. {}. {}. In {} (eds.). {}. {}: {}. "
                    "&lt;{}&gt; (Accessed on {})."
                    .format(auth, year, title, doauth, dotitle, doloc, doedit,
                            link, access))
        elif type == "bibtex":
            return sanitize("@incollection{doreco-" + sour.id + ",\n  address   = {"
                            + doloc + "},\n  author    = {" + auth + "},\n  booktitle = {"
                            + dotitle + "},\n  editor    = {" + doauth + "},\n  publisher = {"
                            + doedit + "},\n  title     = {" + title + "},\n  url       = {"
                            + link + "},\n  urldate   = {" + access + "},\n  year      = {"
                            + year + "}\n}")
        elif type == "ris":
            txt = "TY  - CHAP\n"
            for author in auth:
                txt = txt + "AU  - " + author + "\n"
            for editor in doauth:
                txt = txt + "ED  - " + editor + "\n"
            compl = ("PY  - {0}\nDA  - {0}//\nTI - {1}\nBT  - {2}\n"
                     "PB  - {3}\nCY  - {4}\nUR  - {5}\nY2  - {6}"
                     "\nID  - doreco-{7}\nER  - "
                     .format(year, title, dotitle, doedit, doloc, link,
                             raccess, sour.id))
            return txt + compl

    ## A language 'descriptions'
    #
    #   ctx.name        language
    #   ctx.creator     author
    #   ctx.arclink     na or link to archive
    #   missing         compiled in ( see field date from metadata ???) or na ?
    #   missing         doreco years ( static ? 2020 - 2022 ?
    #   missing         citation form ( create by a function from clld framework ?


def get_desc(ctx, sour, dflt=True, us=False, type='html'):
    """Provides a language descriptions."""
    data_year = '2022'
    isSource = "[click cite button]"
    human_creator = get_author(ctx.creator, 'txt')
    print(human_creator)
    arc_link = literal(ctx.arc_link())
    if hasattr(sour, 'year'):
        data_year = sour.year
        isSource = get_cite(ctx.id, sour, 'bibtex')
    style = ("<style>p.cite {padding-left: 25px; text-indent: -15px; "
             "font-size: 90%;}</style></style>")
    list_marker = ['<p>', '</p>', '<pre class=\"cite\">', '</pre>']
    if type == 'markdown':
        style = ''
        list_marker = ['', '\n\r', '', '\n\r']
        arc_link = '[' + ctx.arclink + '](' + ctx.arclink + ' "click to open")'

    text = ((list_marker[0] + "The {0} DoReCo data set was compiled by {1} in {2} "
                              "and further processed by the DoReCo team in {3}.")
            .format(ctx.name, human_creator, data_year, "2020-2022"))
    arch = ""
    if not ctx.arclink == "na":
        arch = (" A larger collection of {}'s {} data is archived "
                "at {}.".format(human_creator, ctx.name, arc_link))
    return literal(text + arch + ((list_marker[1] + list_marker[0] + "A set of files with further information "
                                                                     "on the {0} DoReCo data set, including metadata and PIDs is "
                                                                     "automatically included in each download of {0} DoReCo files." +
                                   list_marker[1] +
                                   list_marker[0] + "The {0} DoReCo data set should be cited as follows "
                                                    "(a BibTex version of this citation is provided below):" +
                                   list_marker[1] +
                                   list_marker[2] + "{1}" + list_marker[3] + list_marker[
                                       0] + "Please note that when citing "
                                            "this data set, or any number of DoReCo data sets, it is NOT "
                                            "sufficient to refer to DoReCo (and its editors) as a whole, "
                                            "but the full citation for each individual data set must be "
                                            "provided, including the names of the creators of each data "
                                            "set." + list_marker[1]).format(ctx.name, isSource)))  # " )))#


def get_source(ctx):
    sources = DBSession.query(Source).filter(Source.id == ctx.id).all()
    print(sources)


def get_audio(ctx):
    html_result = "list of audio in nakala"
    languages = DBSession.query(doreLanguage).join(Language, Language.pk == doreLanguage.pk).all()
    for lang in languages:
        if lang.AUDIO is not None and lang.AUDIO != 'na':
            html_result += '<li> ' + lang.name + ' <a href="https://test.nakala.fr/' + lang.AUDIO + '" target=_BLANK>view audio</a><br>' + '<a href="./static/' + lang.id + '.zip">add a direct link to a zip archive of the audio ?</a>' + '</li>'
    return literal(html_result)


def get_nak(ctx, sour):
    html_result = ""
    lang = DBSession.query(doreLanguage). \
        filter(doreLanguage.id == ctx.id).first()
    if lang.NAK is not None and lang.NAK != 'na':
        html_result += '<a href="https://test.nakala.fr/' + lang.NAK + '" target=_BLANK>view language information on nakala</a></li>'
    return literal(html_result)


def Handle2Nakala(instance):
    return instance
