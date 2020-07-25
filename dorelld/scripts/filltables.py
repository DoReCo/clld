#### Support script for 'initializedb.py'
# Reads our files to fill the CLLD database. Supports '.csv', '.tsv',
# '.xls', '.xlsx' and '.ods' files. 
# Note: '.csv' and '.tsv' depend on a user-defined separator symbol 'sep'.
# Note: if multiples files share the same name, only the first will be read.
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
# Lyon, 05/14/2020
# François Delafontaine
####

	## Imports
	# If 'pyexcel' fails:
	# - make sure to be in the right Python environment
	# - use 'pip3 install' to load the missing packages
import os, pyexcel

	# Support functions
def readarray(mode,sheet):
	"""Support function to read a sheet from 'pyexcel'.
	ARGUMENT:
	- sheet		:	an array iterator from 'pyexcel'
	- mode		:	'0' for a global languages sheet
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
def opencsv(path,sheet,fi,sep):
	"""Support function for 'filltables', iterator over a CSV file.
	ARGUMENTS:
	- path		:	the file path
	- sheet/fi	:	the file name, respectively with and without extension
	- sep		:	the separator symbol (default ',')
	RETURNS:
	- an iterator of tuples (fi,key,metadata).
	DEPRECATED"""
	
	fil = pyexcel.iget_book(file_name=path,delimiter=sep)
	sheet = fil.sheets[sheet].get_internal_array()
	if fi.lower() == "languages":
		sheet = readarray(0,sheet)
	else:
		sheet = readarray(1,sheet)
	for key,metadata in sheet.items():
		yield (fi,key,metadata)
	pyexcel.free_resources()
def openbook(path):
	"""Support function for 'filltables', iterator over an 'Excel' file.
	ARGUMENTS:
	- path		:	the file path
	RETURNS:
	- an iterator of tuples (sheet,key,metadata)
	Note: Also creates default language description files."""
		# We open the file
	fil = pyexcel.iget_book(file_name=path)
		# We get the 'languages' sheet first
	d_langs = {}
	for n_sheet in fil.sheets:
		low = n_sheet.lower()
		if not (low == "languages"):
			continue
		sheet = fil.sheets[n_sheet].get_internal_array()
		sheet = readarray(0,sheet)
		for code,metadata in sheet.items():
			d_langs[code] = True
			yield (low,code,metadata)
		break
		# We create each default language file
	d = os.path.join(os.path.dirname(__file__),
		                 "..","templates","descriptions")
	for code in d_langs:
		f = os.path.join(d,code+".html")
		if not os.path.exists(f):
			with open(f,'w',encoding="utf-8") as fi:
				fi.write("<br/><br/><br/><br/><br/><br/>\n"
                           "<br/><br/><br/><br/><br/><br/>")
		# We get each language sheet next
	for code in d_langs:
		sheet = fil.sheets.get(code,None)
		if not sheet:
			continue
		sheet = sheet.get_internal_array()
		sheet = readarray(1,sheet)
		for name,metadata in sheet.items():
			yield (code,name,metadata)
	pyexcel.free_resources()

	# Main function
def filltables(path="/home/doreco/dorelld/dorelld/tables",sep=","):
	"""Fetches tables and yields on their information.
	ARGUMENTS:
	- path		:	the file path
	- sep		:	for '.csv'/'.tsv', the separator symbol (default ',')
	RETURNS:
	- an iterator for 'initializedb'.
	Note: relies on 'pyexcel' and its plugins. if 'ImportError' happens,
	      use 'pip3 install' in the right environment to install the
	      missing libraries.
	Note: while we use 'iget_book()' to try and manage memory consumption,
          we mostly assume imported files will be small anyway.
    Note: Each sheet (or '.csv' file) should only contain one table."""
	
		# We iterate over the files
	ite = None; d_files = {}
	for fil in os.listdir(path):
		#print(fil) #DEBUG
			# Variables
		fi,ext = os.path.splitext(fil)
		f = os.path.join(path,fil); ite = None
		if fi in d_files:
		    continue
			# We get an iterator over our file
		if ext == ".csv" or ext == ".tsv":
			ite = opencsv(f,fil,fi,sep)
		elif ext == ".ods" or '.xls' in ext:
			ite = openbook(f)
		if not ite:
			continue
			# We use that iterator
		for tupl in ite:
			yield tupl # /!\ It is up to 'initializedb' to parse and rename.
		ite = None; d_files[fi] = True

    
    # Other functions
def cleardb():
	"""I am losing my nerves."""
	os.system("sudo -u postgres psql -c \"alter database dboreco owner"
	          " to postgres;\"")
	os.system("sudo -u postgres psql -c \"drop database dboreco;\"")
	os.system("sudo -u postgres psql -c \"create database dboreco;\"")
	os.system("sudo -u postgres psql -c \"alter database dboreco owner"
	          " to dboreco\"")

	# For debug purposes. 
if __name__ == "__main__":
	import sys
	
	la = len(sys.argv); path = "../../tables"; sep=","
	if la > 1:
		path = sys.argv[1]
		if la > 2:
			sep = sys.argv[2]
	print("Start:")
	for tupl in filltables(path,sep):
		print("\t",tupl[0], tupl[1])
		for key, value in tupl[2].items():
			print("\t\t\t",key,value)
	print("End.")
