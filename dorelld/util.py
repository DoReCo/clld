from clld.web.util.htmllib import HTML, literal

    ## A download form for all pages
    # 'full'    : displays the full form or (False) just the button
    #             default values then are 'wav=True&format=all'
def get_form(lang_n="",ext=False, full=True):
    style = ("<style>"
     "form {float: left; margin: 0px; padding: 0px;} "
     "input {float: left; margin-right: 10px;} "
     "select {float: left; margin-right: 10px;} "
     "label {float: left; margin-right: 10px;} "
     "p.form {float: left; margin-right: 10px; padding: 3px;}"
     "</style>")
    lang = ("<input type=\"hidden\" id=\"f_id\" "
            "name=\"id\" value=\""+lang_n+"\">")
    if full:
        wav =  ("<input type=\"checkbox\" id=\"f_wav\" name=\"wav\" "
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
