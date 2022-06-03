from clld.web.adapters.base import adapter_factory
from pyramid.view import view_config
from dorelld.scripts.download import download

    # Download function
    ## This is an actual link, 'doreco.info/doreLoad'
    ## Returns a url to a '.zip' file
@view_config(route_name='doreLoad')
def doreLoad(req):
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
    return download(req)

@view_config(route_name='audio', renderer = 'audio/detail_html.mako')
def DLaudio(req):
    pass
    req.name = 'audio download page'
    req.description = 'test direct'
    return {'ctx' : req}