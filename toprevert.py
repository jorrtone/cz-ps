#!/usr/bin/python3

"""

Parses .html file to .prevert format


"""

"""
EXAMPLE

<p align="justify"><a href="/sqw/detail.sqw?id=5462">Pøedseda PSP Jan Hamáèek</a>: Dìkuji. Vážený pane místopøedsedo, 
dámy a pánové, vážená vládo, já bych nevystupoval, kdyby moje jméno nepadlo z&nbsp;úst jednoho z&nbsp;øeèníkù. 
A když už tedy to slovo mám, tak to vezmu trošku zeširoka. </p>

<speech ID="401" FirstName="Miroslava" SecondaryRole="poslanec" StenographerTitle="Řeč předsedající Miroslavy Němcové" Surname="Němcová" 
TitleAfter="" TitleBefore="" Url="http://www.psp.cz/sqw/detail.sqw?id=401" Function="Předsedající" Continue="False">
"""

import sys
import re
from bs4 import BeautifulSoup


def print_speech_paragraph(fout, p):
	### write ID
	fout.write("<speech ID=\"")
	fout.write(p.a['href'].split("id=")[-1])
	
	### info_name = [ROLE, FIRSTNAME, LASTNAME]
	info_name = p.find('a').text.rsplit(' ', 2)
	fout.write("\" FirstName=\"%s\" Surname=\"%s\" " % (info_name[1], info_name[2]))
	fout.write("Url=\"%s\" Function=\"%s\">" % ("https://www.psp.cz/" + p.a['href'], info_name[0]))
	fout.write("\n")


def print_paragraph(fout, p):
	if p.text in ["", " ", " " "\n"]:
		return
	space = " " * 10
	fout.write(space)
	fout.write("<p>\n")
	fout.write(space + "  " + p.text + "\n")
	fout.write(space)
	fout.write("</p>\n")


def to_prevert(filename, target):
	with open(filename, encoding = "ISO-8859-1") as file:
		content = file.read()

	new_peson = False
	fout = open(target, "w")
	soup = BeautifulSoup(content, "lxml")
	for paragraph in soup.find_all('p'):
		if paragraph.find('a'):							# if paragraph belongs to the another person
			if new_peson:
				fout.write("</speech>\n")
			new_peson = True
			print_speech_paragraph(fout, paragraph)
		elif not new_peson:
			continue
		print_paragraph(fout, paragraph)				# write the paragraph in .prevert format
	fout.write("</speech>\n")
	fout.close()