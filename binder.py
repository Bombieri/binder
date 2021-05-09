#!/usr/local/bin/python3.6
#binder.py -- unisce in ordine alfabetico tutti i pdf inseriti nella cartella ./pool
#versione 1.1

import os
import sys
import time
import re
import PyPDF2 as pypdf

#functions
def pdflist(pdfFiles):
	for Filename in os.listdir("."):
		if (Filename.lower().endswith(".pdf")):
			pdfFiles.append(Filename)
	convert = lambda text: float(text) if text.isdigit() else text
 	alphanum = lambda key: convert(c) for c in re.split('([-+]?[0-9]*\.?[0-9]*)', key)
	pdfFiles.sort(key=alphanum)
	return pdfFiles

def read(file):
	pdfFileObj = open(file, 'rb')
	pdfReader = pypdf.PdfFileReader(pdfFileObj)
	return pdfReader

def append(pdfWriter, pdfReader):
	for pageNum in range(0, pdfReader.numPages):
		pageObj = pdfReader.getPage(pageNum)
		pdfWriter.addPage(pageObj)
	return pdfWriter

def save(title, pdfWriter):
	title = title + ".pdf"
	pdfOutput = open(os.path.join(os.path.join(__location__, "binded"), title), 'wb')
	pdfWriter.write(pdfOutput)
	# pdfWriter.addMetadata({
	# 	"/Title": title
	# 	"/Author": author
	# })
	pdfOutput.close()

def log():
	#apertura/creazione file log.txt
	log = open(os.path.join(__location__, "log.txt"), 'a')
	#scrittura data e orario in log.txt
	log.write(time.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S") + '\n' )
	return log

def name(filename):
	s = filename.split("/")		
	l = len(s)								
	filename = s[l-1]			
	return filename

#main
__location__ = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(__location__)

if not os.path.exists('pool'):  #creo directory pool se non esiste
	os.makedirs('pool')

if not os.path.exists('binded'):  #creo directory watermarked
	os.makedirs('binded')

os.chdir(os.path.join(__location__, "pool"))

title = input("Inserire titolo del pdf finale\n")
#author = input("Inserire autore del pdf\n")

log = log()

pdfFiles = []
pdflist(pdfFiles)
length = len(pdfFiles)

pdfWriter = pypdf.PdfFileWriter()
for file in pdfFiles:
	filename = name(file)
	print("Processo %s..." % filename)
	log.write("Processo %s...\n" % filename)
	pdfReader = read(file)
	append(pdfWriter, pdfReader)
	os.remove(file)

if length >=1:
	save(title, pdfWriter)
log.write("\n")
