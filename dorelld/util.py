import os
from urllib import parse,request
from zipfile import ZipFile 

import clld.web.util.helpers as helpers

def cite_button(req, ctx):
    return helpers.button(
        'cite',
        id="cite-button-%s" % ctx.id,
        onclick=helpers.JSModal.show(ctx.name, req.resource_url(ctx, ext='md.html')))

def _getfiles(lang):
	"""For 'dorload()'. Gets the files."""
def _getcite(lang):
	"""For 'dorload()'. Gets the citations."""
	return None
def _zip(files,cite,meta=None):
	"""For 'dorload()'. Zips everything together."""
	return None
def dorload(lang,i=-1,wav=False):
	"""Downloading files, regrouping them, zipping them.
	ARGUMENTS:
	- 'lang'	:	the collection to download
	- 'i'		:	the type of format to download
	- 'wav'		:	whether to fetch sounds too
	RETURNS:
	- When all is said and done, a '.zip' file.
	Note: the '.zip' should contain:
	      a) the transcriptions in a given format (.x)
	      b) a metadata document (?)
	      c) the citations to include (.txt)"""
	
	url = "hdl.handle.net/11280/6e9d57e9"
	fi = request.Request(url)
	response = request.urlopen(glottolog).read()
	return response
		# to do
	files = _getfiles(lang)
	cite = _getcite(lang)
	pack = _zip(files,cite)
def download_button(req,ctx,i=0):
	"""Actual download button."""
	alng=""; name=""; wav=False
	if i == 0:
		name = "WAV"; wav = True
	elif i == 1:
		name = "Praat"
	elif i == 2:
		name = "Elan"
	elif i == 3:
		name = "Tabular"
	elif i == 4:
		name = "TEI"
	
	return helpers.button(
	       name,
	       id="b-download-%s" % ctx.id
	       )
