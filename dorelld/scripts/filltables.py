#### Support script for 'initializedb.py'
# Reads our files to fill the CLLD database. Supports '.csv', '.tsv',
# '.xls', '.xlsx' and '.ods' files. 
# Note: '.csv' and '.tsv' depend on a user-defined separator symbol 'sep'.
# Note: if multiples files share the same name, only the first will be read.
# Note: only one 'ods/xls' file will be read (first found).
#
# REQUIREMENT:
# Requires the 'pyexcel' package with at least 'pyexcel-xlsx' and
# 'pyexcel-ods3'.
# Those can be imported (in the right Python environment) using
# 'pip3 install' and the package's name as written above.
#
# PATH:
# The path is for a directory containing our tables. It can be modified
# in 'filltables()', directly in its arguments.
# Note that this is also where the separator can be edited, if need be.
#
# RETURNS:
# An iterator of tuples (name,key,metadata).
# - the 'name' is either 'languages' or the language's glottocode.
# - the 'key' is either the glottocode or the transcription's name.
# - 'metadata' is a dictionary.
# Parsing that dictionary to fill our database is up to 'initializedb.py'.
#
# Lyon, 04/08/2020
# François Delafontaine
####

    ## Imports
    # If 'pyexcel' fails:
    # - make sure to be in the right Python environment
    # - use 'pip3 install' to load the missing packages
import os, pyexcel

    # Support function (reader)
def _readarray(mode,sheet):
    """Support function to read a sheet from 'pyexcel'.
    ARGUMENT:
    - sheet     :   an array iterator from 'pyexcel'
    - mode      :   '0' for a global languages sheet
                    '1' for an individual language sheet
    RETURNS:
    - a dictionary of languages (dict[glottocode][metadata])
    - or of a transcription     (dict[name][metadata])"""
    
    d_array = {}; d_pos = {}; i_col = 0; l_temp = []
    ch_header = False; lang = ""
    for row in sheet:
        if not row:
            continue
        if ch_header == False:
            i_col = -1
            for col in row:
                i_col += 1
                if not col:
                    continue
                d_pos[i_col] = col
            ch_header = True; continue
        i_col = -1; l_temp.clear(); lang = ""
        for col in row:
            i_col += 1
            n_temp = d_pos.get(i_col,None)
            if not n_temp:
                continue
            if ((mode == 0 and n_temp == "Glottocode") or 
                (mode == 1 and n_temp == "name")):
                d_array[col] = {n_temp:col}
                for tupl in l_temp:
                    d_array[col][tupl[0]] = tupl[1]
                lang = col; l_temp.clear()
            elif lang:
                d_array[lang][n_temp] = col
            else:
                l_temp.append((n_temp,col))
    del d_pos; del l_temp
    return d_array
    # Support functions (iterators)
def _opencsv(d_csv,sep=","):
    """Support function for 'filltables', iterator over a CSV file.
    ARGUMENTS:
    - d_csv     :   a dictionary of csv/tsv files
    RETURNS:
    - an iterator of tuples (fi,key,metadata)"""
    
        # Variables
    lang = d_csv.get('languages')
    eds = d_csv.get('editors')
    sour = d_csv.get('sources')
    
        # We get the 'languages' sheet first
    d_langs = {}
    sheet = pyexcel.get_sheet(file_name=lang,delimiter=sep)
    if sheet:
        sheet = _readarray(0,sheet)
        for code,metadata in sheet.items():
            d_langs[code] = True
            yield ('languages',code,metadata)
        # We get 'editors' next
    if eds:
        sheet = pyexcel.get_sheet(file_name=eds,delimiter=sep)
        if sheet:
            sheet = _readarray(0,sheet)
            for code,metadata in sheet.items():
                d_langs[code] = True
                yield ('editors',code,metadata)
        # Followed by 'sources'
    if sour:
        sheet = pyexcel.get_sheet(file_name=sour,delimiter=sep)
        if sheet:
            sheet = _readarray(0,sheet)
            for code,metadata in sheet.items():
                d_langs[code] = True
                yield ('sources',code,metadata)
    
        # We create each default language file
    d = os.path.join(os.path.dirname(__file__),
                         "..","templates","descriptions")
    if not os.path.isdir(d):
        os.mkdir(d)
    for code in d_langs:
        f = os.path.join(d,code+".html")
        if not os.path.exists(f):
            with open(f,'w',encoding="utf-8") as fi:
                fi.write("<br/><br/><br/><br/><br/><br/>\n"
                           "<br/><br/><br/><br/><br/><br/>")
        # We finally get each language sheet
    for code in d_langs:
        if not code in d_csv:
            continue
        sheet = pyexcel.get_sheet(file_name=sour,delimiter=sep)
        if not sheet:
            continue
        sheet = _readarray(1,sheet)
        for name,metadata in sheet.items():
            yield (code,name,metadata)
    pyexcel.free_resources()
def _openbook(path):
    """Support function for 'filltables', iterator over an 'Excel' file.
    ARGUMENTS:
    - path      :   the file path
    RETURNS:
    - an iterator of tuples (sheet,key,metadata)"""
        # We open the file
    fil = pyexcel.iget_book(file_name=path)
        # We get a dict of sheets
    d_sheets = {}
    for n_sheet in fil.sheets:
        low = n_sheet.lower()
        d_sheets[low] = n_sheet
        
        # We get the 'languages' sheet first
    d_langs = {}
    sheet = d_sheets.get('languages')
    if sheet:
        sheet = fil.sheets[sheet].get_internal_array()
        sheet = _readarray(0,sheet)
        for code,metadata in sheet.items():
            d_langs[code] = True
            yield ('languages',code,metadata)
        # We get 'editors' next
    sheet = d_sheets.get('editors')
    if sheet:
        sheet = fil.sheets[sheet].get_internal_array()
        sheet = _readarray(1,sheet)
        for code,metadata in sheet.items():
            yield ('editors',code,metadata)
        # Followed by 'sources'
    sheet = d_sheets.get('sources')
    if sheet:
        sheet = fil.sheets[sheet].get_internal_array()
        sheet = _readarray(1,sheet)
        for code,metadata in sheet.items():
            yield ('sources',code,metadata)

        # We create each default language file
    d = os.path.join(os.path.dirname(__file__),
                         "..","templates","descriptions")
    if not os.path.isdir(d):
        os.mkdir(d)
    for code in d_langs:
        f = os.path.join(d,code+".html")
        if not os.path.exists(f):
            with open(f,'w',encoding="utf-8") as fi:
                fi.write("<br/><br/><br/><br/><br/><br/>\n"
                           "<br/><br/><br/><br/><br/><br/>")
        # We finally get each language sheet
    for code in d_langs:
        sheet = fil.sheets.get(code,None)
        if not sheet:
            continue
        sheet = sheet.get_internal_array()
        sheet = _readarray(1,sheet)
        for name,metadata in sheet.items():
            yield (code,name,metadata)
    pyexcel.free_resources()
    # Main function
def filltables(path="/home/doreco/dorelld/tables",sep=","):
    """Fetches tables and yields on their information.
    ARGUMENTS:
    - path      :   the file path
    - sep       :   for '.csv'/'.tsv', the separator symbol (default ',')
    RETURNS:
    - an iterator for 'initializedb'.
    Note: relies on 'pyexcel' and its plugins. if 'ImportError' happens,
          use 'pip3 install' in the right environment to install the
          missing libraries.
    Note: while we use 'iget_book()' to try and manage memory consumption,
          we mostly assume imported files will be small anyway.
    Note: Each sheet (or '.csv' file) should only contain one table."""
    
        # We look at the available files
    d_csv = {}; book = ""; ch_url = False
    if not os.path.isdir(path):
        if os.path.isfile(path):
            book = path
        elif path.startswith("http://") or path.startswith("https://"):
            book = downtable(path); ch_url = True
    else:
        for fil in os.listdir(path):
            fi,ext = os.path.splitext(fil)
            f = os.path.join(path,fil)
            if ((ext == '.csv' or ext == '.tsv') and not
                (fi in d_csv)):
                d_csv[fi.lower()] = f
            elif (ext == '.ods' or '.xls' in ext) and not book:
                book = f
        # We prioritize 'ods/xls'
    if book:
        ite = _openbook(book); del d_csv
        # Otherwise we go for 'csv/tsv'
    elif "languages" in d_csv:
        ite = _opencsv(d_csv,sep)
        # We give up if nothing got returned
    if not ite:
        return
        # We iterate over the tables
    for tupl in ite:
            yield tupl # /!\ It is up to 'initializedb' to parse and rename.
        # If we downloaded the table, we delete it
    if ch_url:
        os.remove(path)
    
    # Other functions
def cleardb():
    """Clearing the database."""
    os.system("sudo -u postgres psql -c \"alter database dboreco owner"
              " to postgres;\"")
    os.system("sudo -u postgres psql -c \"drop database dboreco;\"")
    os.system("sudo -u postgres psql -c \"create database dboreco;\"")
    os.system("sudo -u postgres psql -c \"alter database dboreco owner"
              " to dboreco\"")
def downtable(url,path="",f=""):
    """Downloads the table for use."""
    from urllib import request
    
        # check
    if not url or (not url.startswith("https://") or
       not url.startswith("http://")):
        return path
        # get format
        ## it's a parameter in the url
    if not f:
        start = url.find("format="); end = url.find("&id",start)
        if start < 0 or end < 0:
            return path
        f = url[s+7:end]
    if not f == "ods" and not f == "xlsx":
        return path
        # get the file
    response = request.urlopen(url)
        # get path
    if os.path.isdir(path):
        path = os.path.join(path,'table.'+f)
    else:
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'table.'+f)
        # write
    with open(path,'wb') as file:
        file.write(response.read())
    return path
def _get_count(mode,d_x,book=None,f=""):
    """Support function ('count') to increment the language table columns.
    ARGUMENT:
    - 'mode'        :   '0' for 'csv/tsv', '1' for 'ods/xls'
    RETURNS:
    - directly edits the table"""
    
    lang_sh = None
    if mode == 0:
        lang_sh = pyexcel.get_sheet(d_csv['languages'],name_columns_by_row=0)
    elif mode == 1:
        lang_sh = d_x.get('languages'); lang_sh.name_columns_by_row(0)
    else:
        return -1
    lsr = lang_sh.number_of_rows()
            # for each language
    for a in range(lsr):
        gcode = lang_sh[a,'Glottocode']
        print(gcode)
            # we get the language csv
        l_sheet = None
        if mode == 0:
            l_sheet = d_x.get(gcode)
            if not l_sheet:
                continue
            l_sheet = pyexcel.get_sheet(l_sheet,name_columns_by_row=0)
        elif mode == 1:
            l_sheet = d_x.get(gcode)
            if not l_sheet:
                continue
            l_sheet.name_columns_by_row(0)
        ulsr = l_sheet.number_of_rows()
        egt = 0; egw = 0; egs = 0
        gt = 0; gw = 0; gs = 0
            # and we increment words/speakers/texts
        for b in range(ulsr):
            if not l_sheet[b,'name']:
                continue
                continue
            print(b,l_sheet.row[b])
            w = l_sheet[b,'words']; s = l_sheet[b,'spk_code']
            if w and not str(w).startswith("check"):
                w = int(w)
            else:
                w = 0
            if s:
                s = str(s).count(";")+1
            else:
                s = 0
            egw = egw + w; egs = egs + s; egt += 1
            if l_sheet[b,'extended'] == "no":
                gw = gw + w; gs = gs + s; gt += 1
            # which we write back in the language's row
        lang_sh[a,'Words'] = egw; lang_sh[a,'Core words'] = gw
        lang_sh[a,'Speakers'] = egs; lang_sh[a,'Core speakers'] = gs
        lang_sh[a,'Texts'] = egt; lang_sh[a,'Core texts'] = gt
    if mode == 0:
        lang_sh.save_as(d_x['languages'])
    else:
        book.save_as(f)
    return 0
def count(path="/home/vuld/CLLD/myapp/tables"):
    """Fill 'spks/words/texts' columns.
    ARGUMENTS:
    - 'path'        :   the directory to look after
    Note: 
    """
        # Variables
    d_csv = {}; book = ""
        # We look for csv/tsv and ods/xls files
    for fil in os.listdir(path):
        fi,ext = os.path.splitext(fil)
        f = os.path.join(path,fil)
        if ((ext == '.csv' or ext == '.tsv') and not
            (fi in d_csv)):
            d_csv[fi.lower()] = f
        elif (ext == '.ods' or '.xls' in ext) and not book:
            book = f
        # We get the tables
    ch = 1
        ## csv/tsv
    if d_csv and "languages" in d_csv:
        ch = _get_count(0,d_csv)
        ## ods/xls
    if ch < 1:
        if ch == 0:
            print("\tcsv/tsv : done")
        else:
            print("\tcsv/tsv : I don't know what went wrong.")
    if book:
            # we get the language table
        lang_b = pyexcel.get_book(file_name=book); d_lang = {}
        for sheet in lang_b:
            d_lang[sheet.name.lower()] = sheet
        if not 'languages' in d_lang:
            return -1
        ch = _get_count(1,d_lang,lang_b,book)
    if ch >= 1:
        print("\tNo file found?")
    elif ch == 0:
        print("\t"+os.path.split(book)[1]+" : done")
    else:
        print("\t"+os.path.split(book)[1]+" : I don't know what went wrong.")
    return ch

    # For debug purposes. 
if __name__ == "__main__":
    import sys
    
    la = len(sys.argv); path = "../../tables"
    if la > 1:
        path = sys.argv[1]
        if la > 2:
            if sys.argv[2] == "count":
                count(path); exit()
            else:
                filltables(path,sep)
        else:
            filltables(path,sep)
