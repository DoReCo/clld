from pyramid.response import Response, FileResponse    # pyramid imports

import io,html
import os,shutil,tempfile,zipfile                      # generic imports
from urllib import parse,request
from dorelld.models import doreLanguage,doreContrib    # models

    # Get the arguments
def _downargs(req,s_path):
    """Support function ('download') to get the arguments."""
    
        # Extensions table
    d_exts = {'all':['textgrid','eaf','xml','tei','json','csv'],
              'praat':['textgrid'],
              'elan':['eaf'],
              'tei':['tei','xml'],
              'tabular':['json','csv'],
              'cross1':['crosstable1','crosstable_1'],
              'cross2':['crosstable2','crosstable_2'],
              'cross3':['crosstable3','crosstable_3'],
              'cross':['crosstable']}
    
        # retrieve variables from 'request'
    lang_n = req.POST.get('id')                # the language
    wav_n = req.POST.get('wav',"False")        # if audio files
    format_n = req.POST.get('format').lower()  # the format
    ext_n = req.POST.get('extended',"False")   # if extended
    if not lang_n or not format_n:
        return False,"",[],False,"",False,""
        # rework the variables a bit
    wav = False; ext = False                   # booleans
    if wav_n == "True":
        wav = True
    if ext_n == "True":
        ext = True
    lang = []                                  # lang_n into list
    if ";" in lang_n:
        temp = lang_n.split(";"); lang = []
        for l in lang_n:
            if lang:
                lang.append(l.lower())
        if len(lang) > 5:
            wav = False
    else:
        lang = [lang_n]
        if lang_n.lower() == "languages":
            wav = False
    l_format = d_exts.get(format_n)            # format
    if not l_format:
        l_format = [format_n]
    z_name = lang_n                            # zip file name
    if wav == True:
        name = z_name + "_w"
    z_name = z_name+"_"+format_n+".zip"
    return True,lang_n,lang,wav,format_n,l_format,ext,z_name
    # Query and fetch links
def _loop(typ,fi):
    """Support function ('_getf()') to read NAKALA metadata pages."""
    
        # Variables
    ch_title = False; ch_files = False;
    title = ""; l_files = []; doc = ""
    
        # Collection
    if typ == "col":
        for line in fi:
            line = line.decode('utf-8')
            if not ch_title:
                if "<h1 id=\"title\">" in line:
                    start = line.find(">")+1; end = line.find("<",start)
                    title = html.unescape(line[start:end]); ch_title = True
            elif ch_files:
                if "<small>of</small>" in line:
                    ch_files = False
                elif "href=" in line:
                    start = line.find("href=\"")+6; end = line.find("\"",start)
                    text = line[start:end]
                    if not "output" in text:
                        l_files.append(text)
                elif "class=\"property-name\">" in line:
                    break
            else:
                if "aggregates</a>" in line:
                    ch_files = True
    elif typ == "res":
        ch_title2 = False
        for line in fi:
            line = line.decode('utf-8')
            if not ch_title:
                if not ch_title2:
                    if "altLabel</a>" in line:
                        ch_title2 = True
                elif "class=\"literal\">" in line:
                    start = line.find("literal\">")+9
                    end = line.find("<",start)
                    if end >= start:
                        title = line[start:end]
                    else:
                        title = line[start:-1]
                    ch_title = True
                elif "class=\"property-name\">" in line:
                    ch_title2 = False
            elif ch_files == False:
                if "primaryTopic</a>" in line:
                    ch_files = True
            else:
                if "<small>of</small>" in line:
                    ch_files = False
                elif "href=" in line:
                    start = line.find("href=\"")+6; end = line.find("\"",start)
                    doc = line[start:end]
                    doc = doc.replace("page/","")
                    break
                elif "class=\"property-name\">" in line:
                    break
    elif typ == "list":
        for line in fi:
            line = line.decode('utf-8')
            if not ch_files:
                if "<ul" in line:
                    ch_files = True
            else:
                if "<small>of</small>" in line:
                    ch_files = False
                elif "href=" in line:
                    start = line.find("href=\"")+6; end = line.find("\"",start)
                    text = line[start:end]
                    l_files.append(text)
                elif "</ul>" in line:
                    ch_files = False
    
    return (title,l_files,doc)
def _getf(typ,path):
    """Support function ('_gelink()') to process links or files."""
    if path.startswith("http"):
        path = request.urlopen(path)
        return _loop(typ,io.BytesIO(path.read()))
    else:
        with open(path,'rb') as fi:
            result = _loop(typ,fi)
        return result
def _linkf(path,name,elim={}):
    """Takes a NAKALA link and returns a list of tuples (folder,name,file)."""
        # Collections to return
    l_files = []
    if not path:
        return l_files
        # Increment lists
    l_titles = [name]; l_chtitle = [True]
    l_paths = [[path]]; l_incr = [0]; l_len = [1]
        # We loop
    while l_paths:
            # End of a list of links
        if l_incr[-1] >= l_len[-1]:
            if l_chtitle[-1] == True:
                l_titles.pop()
            l_chtitle.pop(); l_paths.pop(); l_incr.pop(); l_len.pop()
            continue
            # We check if that's a path we want to follow
        path = l_paths[-1][l_incr[-1]]; l_incr[-1] += 1
        check = path.rsplit("/",2)
        if not len(check) >= 3:
            continue
        check = check[1]+"/"+check[2]
        if check in elim:
            continue
            # We define the type
        typ = ""
        if "values.data" in path:
            typ = 'list'
        elif "collection" in path:
            typ = 'col'
        elif "resource" in path:
            typ = 'res'
        else:
            typ = 'col'
        title,l_urls,doc = _getf(typ,path)
            # We get the resource
        if doc:
            parent = l_titles[-1]
            l_files.append((parent,title,doc))
            continue
            # We add the new links
        if l_urls:
            if title:
                l_titles.append(title); l_chtitle.append(True)
            else:
                l_chtitle.append(False)
            l_paths.append(l_urls.copy())
            l_incr.append(0); l_len.append(len(l_urls))
            continue
    return l_files
def _gelink(typ,obj,wav=False,format_n="",l_format=[],elim={}):
    """Support function ('_downquery') to get a tuple (file,link)."""
    
        # Languages
    if not typ:
        return _linkf(obj.NAK,obj.name,elim=elim)
        # Texts
    else:
        l_temp = _linkf(obj.NAK,obj.tname); ch_file = False
        l_files = []
        for parent,title,doc in l_temp:
            core,ext = os.path.splitext(title)
            ext = ext[1:].lower(); ch_file = False
                # WAV
            if ext == "wav" and wav:
                l_files.append((parent,title,doc))
                # formats
            elif ext in l_format:
                l_files.append((parent,title,doc))
                # crosstables
            elif "cross" in format_n:
                core = core.lower()
                if format_n == "cross" and l_format[0] in core:
                    l_files.append((parent,title,doc))
                elif core in l_format:
                    l_files.append((parent,title,doc))
    return l_files
def _downquery(req,lang,wav,format_n,l_format,ext):
    """Support function ('download') to retrieve the links.
    
    We want:
    - 'l_links' :   a list [(args,l_texts)]
    - 'args'    :   a tuple (glottocode,name,license,audio_license,nak_link)
    - 'l_texts' :   a list [(file_name,nak_link)]
    'nak_link' means the handle to NAKALA."""
    
    l_links = [] # the list to return
    l_langs = [] # the list of languages
    l_largs = [] # language attributes (glottocode,name,license,
                 #                      audio_license,NAKALA)
    
        # get the language(s)
        ## Query
    if lang[0] == "languages":
        query = req.db.query(doreLanguage).all()
    else:
        query = req.db.query(doreLanguage) \
                .filter(doreLanguage.id.in_(lang)).all()
        ## List
    for obj in query:
        if not obj.NAK:
            continue
        l_largs.append((obj.id,obj.name,obj.lic,obj.audio_lic,obj.NAK))
        l_langs.append([[],[]])
            # get the text(s)
            ## Query
        gcode = l_largs[-1][0]                   # Glottocode
        texts = req.db.query(doreContrib) \
                    .filter(doreContrib.glottocode == gcode)
        up_texts = None                         # Texts to retrieve
        if ext:
            up_texts = texts.all()
        else:
            up_texts = texts.filter(doreContrib.extended == False).all()
        temp = texts.all(); texts = {}
        for t_obj in temp:
            if t_obj.NAK == "na":
                continue
            texts[t_obj.NAK.split(".net/",1)[1]] = True
        del temp
            ## List
            # language
        l_langs[-1][0] = _gelink(False,obj,elim=texts)
            # texts
        for t_obj in up_texts:
            if not t_obj.NAK == "na":
                l_langs[-1][1].append(_gelink(True,t_obj,wav,
                                              format_n,l_format))
            # We clean with 'l_links'
        l_links.append((l_largs[-1],l_langs[-1].copy()))
    return l_links
    # Download the collection
def _write(link,d_path,name):
    """Support function to download and write."""
    
        # We ensure extensions are lowered, except TextGrid
    n,e = os.path.splitext(name); e = e.lower()
    if "textgrid" in e:
        e = ".TextGrid"
    d_path = os.path.join(d_path,n+e)
        # Check
    if os.path.exists(d_path):
        return
        # Fetch and write
    r_file = request.urlopen(link)
    with open(d_path,'wb') as fi:
        fi.write(r_file.read())
def _setdirs(lang_path,lname,l_lang):
    """Support function ('_downwrite()') to generate directories.
    ARGUMENTS:
    - 'lang_path'       :   the path to the language directory
    - 'l_lang'          :   the list of resources at the language level
    RETURNS:
    - 'd_dirs'          :   the list of directories for the language
    - 'tabular'         :   the list of resources for 'tabular'
    Note: does write files at the 'language' level."""
    
        # Variables
    tabular = []                            # tabular files
    d_dirs = {'texts':'Annotation files',   # language directories
              'wav':'Audio files',
              'maus':'MAUS time alignment support files',
              'doc':'Documentation files'}
    maus_dir = d_dirs['maus']
    doc_dir = d_dirs['doc']
        # Set directories
    for key,value in d_dirs.items():
        path = os.path.join(lang_path,value)
        if not os.path.isdir(path):
            os.mkdir(path)
        # Add all
    for parent,name,link in l_lang:
        path = ""
            # MAUS
        if "MAUS" in parent:
            if parent == maus_dir:
                path = os.path.join(lang_path,maus_dir)
            else:
                path = os.path.join(lang_path,maus_dir,parent)
                if not os.path.isdir(path):
                    os.mkdir(path)
        elif parent.lower() == "tabular":
            tabular.append((parent,name,link)); continue
        elif parent == lname:
            path = lang_path
        else:
            if parent == doc_dir:
                path = os.path.join(lang_path,doc_dir)
            else:
                path = os.path.join(lang_path,doc_dir,parent)
                if not os.path.isdir(path):
                    os.mkdir(path)
        _write(link,path,name)
    return d_dirs,tabular
def _gettabular(lang_path,d_dirs,tabular,format_n,l_format):
    """Support function ('_downwrite()') to write tabular formats."""

        # Tabular directory
    tab_path = ""; text_path = d_dirs('texts')
    if not text_path:
        tab_path = os.path.join(lang_path,'tabular')
    else:
        tab_path = os.path.join(lang_path,text_path)
        if not os.path.isdir(tab_path):
            os.mkdir(tab_path)
        tab_path = os.path.join(tab_path,'tabular')
    if not os.path.isdir(tab_path):
        os.mkdir(tab_path)
    if not os.path.isdir(tab_path):
        os.mkdir(tab_path)
        # All crosstables
    if format_n == 'cross':
        check = l_format[0]
        for parent,name,link in tabular:
            if check not in name:
                continue
            _write(link,tab_path,name)
        # No crosstable
    elif format_n == 'tabular' or format_n == 'all':
        for parent,name,link in tabular:
            n,ext = os.path.splitext(name)
            ext = ext[1:].lower()
            if ext in l_format:
                _write(link,tab_path,name)
        # A specific crosstable
    elif 'cross' in format_n:
        for parent,name,link in tabular:
            core,e = os.path.splitext(name)
            core = core.lower()
            if core in l_format:
                _write(link,tab_path,name)
def _gettexts(lang_path,d_dirs,l_texts,wav,format_n,l_format):
    """Support function ('_downwrite()') to write other formats.
    ARGUMENTS:
    - 'lang_path'       :   (string) path to the language directory
    - 'd_dirs'          :   (dict) names for the language sub-directories
    - 'l_texts'         :   (list) resources at the text level
    - 'wav'             :   (bool) whether to include wav files
    - 'format_n'        :   (string) what formats to include
    RETURNS:
    - downloads and writes
    Note: includes WAV files.
    Note: will default the folder to the file's name (without extension)
          if no 'd_dirs' correspondant is found."""
    
        # We set the two 'audio' and 'annotation' directories
    wav_dir = d_dirs.get('wav')
    if wav_dir:
        wav_dir = os.path.join(lang_path,wav_dir)
        if not os.path.isdir(wav_dir):
            os.mkdir(wav_dir)
    text_dir = d_dirs.get('texts')
    if text_dir:
        text_dir = os.path.join(lang_path,text_dir)
        if not os.path.isdir(text_dir):
            os.mkdir(text_dir)
        # Loop through the texts
    for text in l_texts:
        for parent,name,link in text:
            core,ext = os.path.splitext(name)
            ext = ext[1:].lower()
                # WAV
            if ext == 'wav' and wav:
                if wav_dir:
                    path = wav_dir
                elif text_dir:
                    path = text_dir
                else:
                    path = os.path.join(lang_path,core)
                    if not os.path.isdir(path):
                        os.mkdir(path)
                _write(link,path,name)
            elif format_n == "none":
                continue
            elif ((format_n == 'all') or (ext in l_format)):
                if text_dir:
                    path = text_dir
                else:
                    path = os.path.join(lang_path,core)
                    if not os.path.isdir(path):
                        os.mkdir(path)
                _write(link,path,name)
def _downwrite(z_name,l_links,lang,s_path,wav,format_n,l_format):
    """Support function ('download') to actually download from NAKALA.
    
    Note: for user update, should be turned into a 'yield' iterator."""

        # collection
    ch_all = False
    if lang[0] == "languages":
        ch_all = True
        coll_path = os.path.join(s_path,os.path.splitext(z_name)[0])
        if not os.path.isdir(coll_path):
            os.mkdir(coll_path)
        # languages
    for args, l_langs in l_links:
        gcode = args[0]; lname = args[1]; lang_path = ""
        if ch_all:
            lang_path = os.path.join(coll_path,lname+" DoReCo data set")
        else:
            coll_path = os.path.join(s_path,lname+" DoReCo data set")
            lang_path = coll_path
        if not os.path.isdir(lang_path):
            os.mkdir(lang_path)
            # language docs
        d_dirs,tabular = _setdirs(lang_path,lname,l_langs[0])
            # texts
            ## tabular
        if ((format_n == 'all') or (format_n == 'tabular') or
            ('cross' in format_n)):
            _gettabular(lang_path,d_dirs,tabular,format_n,l_format)
                # WAV for tabular
                # (and/or other formats)
            if wav or format_n == "all":
                if format_n == "all":
                    _gettexts(lang_path,d_dirs,l_langs[1],wav,format_n,l_format)
                else:
                    _gettexts(lang_path,d_dirs,l_langs[1],wav,'none',[])
            ## Other formats
        else:
            _gettexts(lang_path,d_dirs,l_langs[1],wav,format_n,l_format)
    return coll_path
    # Main
def download(req):
    """Downloads files from NAKALA then returns a '.zip'.
    ARGUMENTS:
    - 'req'     :   a request generated by POST
    - 'id'      :   (in 'req') the language name
    - 'wav'     :   (in 'req') if WAV files are included
    - 'format'  :   (in 'req') the file format
    RETURNS:
    - a url to a '.zip' file for download
    Note: all arguments are strings
    Note: 'lang_n=languages' means all languages
    Note: The process can be lengthy, to recover each and every file,
          then zip them, then delete all but the zip file.
          If the zip file already exists, though, it is directly returned."""

        # get variables
    s_path = "/data/downloads"                  # download dir_path
    nakala = "https://www.nakala.fr/data"       # nakala data url
    ch,lang_n,lang,wav,format_n,l_format,ext,z_name = _downargs(req,s_path)
        # Missing variables, return default page
    if not ch:
        return Response("<!DOCTYPE html>"
                "<html><head><title>DoReCo download service</title></head>"
                "<body><h1>DoReCo download service</h1><p>This link calls "
                "a function to download DoReCo resources. But it requires "
                "more parameters.</p>"
                "<p>Please POST {id=\"glottocode\", format=\"format\"}.</p>"
                "<p>The actual parameters are:</p><table>"
                "<tr><td>id</td><td>The language's glottocode</td></tr>"
                "<tr><td>wav</td><td>Whether to include audio files</td></tr>"
                "<tr><td>format</td><td>The transcription format.</td></tr>"
                "<tr><td>ext</td><td>Whether to include extended files.</td>"
                "</tr></table></body></html>")
        # Check if zip already exists
        ## Note: obsolete, left because it does no harm.
    if os.path.isfile(z_name):
        return FileResponse(z_name,content_type="application/zip")
        # Query the contributions
    l_links = _downquery(req,lang,wav,format_n,l_format,ext)
    print("Links retrieved.")
        # Get the citations/licenses/etc
    #to-do
        # Download
    coll_path = _downwrite(z_name,l_links,lang,s_path,wav,format_n,l_format)
    print("Collection downloaded.")
        # Zip
    with tempfile.NamedTemporaryFile(delete=True) as output:
        zf = zipfile.ZipFile(output,'w', zipfile.ZIP_DEFLATED)
        for root,dirs,files in os.walk(coll_path):
            dir = root.split(s_path,1)[1]
            for file in files:
                zf.write(os.path.join(root,file),
                         arcname=os.path.join(dir,file))
        zf.close(); del zf
        shutil.rmtree(coll_path) # using 'shutil' to remove NAKALA files
        response = FileResponse(os.path.abspath(output.name))
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = 'filename="'+z_name+'"'
        return response
