from pyramid.response import Response, FileResponse    # pyramid imports

import os,shutil,tempfile,zipfile                      # generic imports
from urllib import parse,request
from dorelld.models import doreLanguage,doreContrib


def _downargs(req,s_path):
    """Support function ('download') to get the arguments."""
        # retrieve variables from 'request'
    lang_n = req.POST.get('id')                # the language
    wav_n = req.POST.get('wav',"False")        # if audio files
    format_n = req.POST.get('format')          # the format
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
    else:
        lang = [lang_n]
    format_n = format_n.lower()
    z_name = lang_n                            # zip file name
    if wav == True:
        name = z_name + "_w"
    z_name = z_name+"_"+format_n+".zip"
    return True,lang_n,lang,wav,format_n,ext,z_name
def _gelink(obj,wav,format_n):
    """Support function ('_downquery') to get a tuple (file,link)."""
        # text name
    l_files = [obj.tname]
        # audio file
    if wav and not obj.NAKwav == 'na':
        l_files.append((obj.tname+".wav",obj.NAKwav))
    if format_n == "all":
        if not obj.NAKpraat == 'na':
            l_files.append((obj.tname+".TextGrid",obj.NAKpraat))
        if not obj.NAKelan == 'na':
            l_files.append((obj.tname+".eaf",obj.NAKelan))
        if not obj.NAKtab == 'na':
            l_files.append(("tabular",obj.NAKtab))
        if not obj.NAKtei == 'na':
            l_files.append((obj.tname+".xml",obj.NAKtei))
    elif format_n == "praat" and not obj.NAKpraat == 'na':
        l_langs[a][-1].append((obj.tname+".TextGrid",obj.NAKpraat))
    elif format_n == "elan" and not obj.NAKelan == 'na':
        l_langs[a][-1].append((obj.tname+".eaf",obj.NAKelan))
    elif format_n == "tabular" and not obj.NAKtab == 'na':
        l_langs[a][-1].append(("tabular",obj.NAKtab))
    elif format_n == "tei" and not obj.NAKtei == 'na':
        l_langs[a][-1].append((obj.tname+".xml",obj.NAKtei))
    elif format_n == "cross1" and not obj.NAKcross1 == 'na':
        l_langs[a][-1].append(("crosstable1.csv",obj.NAKcross1))
    elif format_n == "cross2" and not obj.NAKcross3 == 'na':
        ll_langs[a][-1].append(("crosstable2.csv",obj.NAKcross2))
    elif format_n == "cross3" and not obj.NAKcross3 == 'na':
        l_langs[a][-1].append(("crosstable3.csv",obj.NAKcross3))
    return l_files
def _downquery(req,lang,wav,format_n,ext):
    pass
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
                .filter(doreLanguage.id in lang).all()
        ## List
    for obj in query:
        l_largs.append((obj.id,obj.name,obj.lic,obj.audio_lic,obj.NAK))
        l_langs.append([])
    
        # get the text(s)
        ## Query
    for a in range(len(l_langs)):
        gcode = l_largs[a][0]
        if ext:
            query = req.db.query(doreContrib) \
                    .filter(doreContrib.glottocode == gcode).all()
        else:
            query = req.db.query(doreContrib) \
                    .filter(doreContrib.glottocode == gcode) \
                    .filter(doreContrib.extended == False).all()
        ## List
        for obj in query:
            l_langs[a].append(_gelink(obj,wav,format_n))
            # We clean with 'l_links'
        l_links.append((l_largs[a],l_langs[a].copy()))
    return l_links
def _downwrite(z_name,l_links,s_path):
    """Support function ('download') to actually download from NAKALA.
    
    Note: for user update, should be turned into a 'yield' iterator."""
    
        # collection
    coll_path = os.path.join(s_path,os.path.splitext(z_name)[0])
    if not os.path.isdir(coll_path):
        os.mkdir(coll_path)
        # languages
    for args, l_langs in l_links:
        lang_path = os.path.join(coll_path,args[0]) # language by glottocode
        if not os.path.isdir(lang_path):
            os.mkdir(lang_path)
            # texts
        for l_texts in l_langs:
            text = l_texts[0]
            text_path = os.path.join(lang_path,text)
            if not os.path.isdir(text_path):
                os.mkdir(text_path)
                # files
            for a in range(1,len(l_texts)):
                name,link = l_texts[a]
                file_path = os.path.join(text_path,name)
                if os.path.isfile(file_path):
                    continue
                url = nakala+"/"+url.split("/",1)[1]
                response = request.urlopen(url)
                with open(res_path,'wb') as fi:
                    fi.write(response.read())
    return coll_path
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
    Note: 'lang_n=language' means all languages
    Note: The process can be lengthy, to recover each and every file,
          then zip them, then delete all but the zip file.
          If the zip file already exists, though, it is directly returned."""

        # get variables
    s_path = "/data/downloads"                  # download dir_path
    nakala = "https://www.nakala.fr/data"       # nakala data url
    ch, lang_n,lang,wav,format_n,ext,z_name = _downargs(req,s_path)
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
                "<tr><td>ext</td></td>Whether to include extended files.</td>"
                "</tr></table></body></html>")
        # Check if zip already exists
        ## Note: obsolete, left because it does no harm.
    if os.path.isfile(z_name):
        return FileResponse(z_name,content_type="application/zip")
        # Query the contributions
    l_links = _downquery(req,lang,wav,format_n,ext)
        # Get the citations/licenses/etc
    #to-do
        # Download
    coll_path = _downwrite(z_name,l_links,s_path)
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
