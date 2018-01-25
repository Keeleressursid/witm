#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Copyright © Võru Instituut 
#Copyright © Ants Aader
#Edasiturustamine või -levitamine ning tarkvara lähtekoodi ja binaarsete vormide kasutamine modifitseeritud või modifitseerimata kujul on lubatud, kui on täidetud järgmised tingimused:
#Tarkvara lähtekoodi edasiturustamisel või -levitamisel tuleb säilitada ülaltoodud autoriõigusemärge, käesolev tingimuste loetelu ja alljärgnev loobumisteade.
#
#Tarkvara binaarse vormi edasiturustamisel või -levitamisel tuleb dokumentatsioonis ja/või teistes turustamisel või levitamisel üleantavates materjalides reprodutseerida ülaltoodud autoriõigusemärge, käesolev tingimuste loetelu ja alljärgnev loobumisteade:
#
#SELLE TARKVARA ON VALMISTANUD VÕRU INSTITUUT KOOS KAASVALMISTAJATEGA KASUTAMISEKS SELLISENA „NAGU SEE ON“ NING SEE EI ANNA MINGIT SÕNASTATUD VÕI EELDATAVAT GARANTIID, SEALHULGAS TURUSTATAVUSE, TEATUD OTSTARBEKS SOBIVUSE EGA MUUD GARANTIID. MITTE MINGIL JUHUL EI OLE VÕRU INSTITUUT EGA TARKVARA KAASVALMISTAJAD KOHUSTATUD VASTUTAMA ÜKSKÕIK MILLISE OTSESE, KAUDSE, JUHUSLIKU, ERILISE, ÜHEKORDSE EGA TULENEVA KAHJU (SEALHULGAS ASENDUSTOODETE VÕI -TEENUSTE HANKIMISE KUJUL, KASUTAMISE, ANDMETE VÕI TULUDE KAOTUSE KUJUL; VÕI ÄRITEGEVUSE KATKEMISE KUJUL) EEST PÕHJUSTATUNA ÜKSKÕIK KUIDAS JA ÜKSKÕIK MISSUGUSE KOHUSTUSTE PÕHJENDUSEGA, ÜKSKÕIK KAS SEE TEKIB LEPINGULISE KOHUSTUSE, RANGE VASTUTUSE VÕI ÕIGUSERIKKUMISE (SEALHULGAS HOOLETUSE VÕI MUU KUJUL) TÕTTU, KUI SEE TEKIB ÜKSKÕIK MISSUGUSEL TEEL SELLE TARKVARA KASUTAMISE TAGAJÄRJEL, ISEGI KUI ON TEATAVAKS TEHTUD SELLISE KAHJU VÕIMALUS.
#
#Copyright © Võru Institute 
#Copyright © Ants Aader
#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution:
#
#THIS SOFTWARE IS PROVIDED BY THE VÕRU INSTITUTE AND CONTRIBUTORS "AS IS" AND  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys, string, os
import dbconf as d
import wirutiinid as wi
lib_path = os.path.abspath(os.path.join('..', 'sql'))
lib_path = os.path.abspath(os.path.join('..', 'htdocs'))
sys.path.append(lib_path)
import wisql as s
import dbparingud as db
import html as h


def www2db(tõlkenumber,lähtekeel,sihtkeel,veebitekst,viis):
	"""Saab veebiliideselt teksti ja sisestab DB'sse."""
	if viis == "www" or viis == "wwwdebug":
		h.k("<table><tr>\n  <td>")
		h.k(veebitekst)
		h.kr("</td>")
	v = str(veebitekst)
	if viis == "www" or viis == "wwwdebug":
		rida = v.replace("'", r"\''")
	elif viis == "käsurida":
		# lõikame pythoni listi stdin-variandi otsad maha
		rida = v[2:-2]
		#rida = rida.replace("'", r"\''")
	s.sqli(d.n,db.tekstandmetesse(tõlkenumber,lähtekeel,sihtkeel,rida))

def sõnetatekst(tõlkenumber):
	"""Võtab DB'st (tõlkelause) lause ja tokeniseerib/sõnetab."""
	import string,re
	for index,r in enumerate(s.sqle(d.n,db.tükeldatekst(tõlkenumber))):
		lause = r['lähtejutt']
		for index,sõna in enumerate(toki(lause)):
			sõnanr = str(index+1)
			lipp = sõna[0]
			sõna = sõna[1]
			sõna = sõna.replace("'", r"\''")
			s.sqli(d.n,db.toge(tõlkenumber,sõnanr,sõna,lipp))

def uustõlkenumber():
	"""Võtab DB'st suurima tõlkenumberi number ja uus number on +1."""
	maxprnr = s.sqlr(d.n,db.uustõlkenumber())
	nr = int(maxprnr[0])+1
	return nr

def toki(kood):
	import collections
	import re
	# siin üle vaadata, lipsab vigu sisse... nagu ülekirjutus
	Toki = collections.namedtuple('Toki', ['tüüp','väärtus'])
	tokenitüübid = [
	('ingdate'	,r'\d{2}([^:]+)(:\d{2}){2}'),	# inglise kuupäev
	('täiskell'	,r'\d{2}:\d{2}:\d{2}?'),	# kell
	('kell'		,r'\d{2}:\d{2}'),	# kell
	('IPv4'		,r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'),	# IPv4 aadress
	('kuupäev'	,r'\d+(.\d+(.\d*))'),	# kuupäev
        ('täisarv',  r'\d+'),  # Integer or decimal number
	('ingnumber'	,r'\d+(.\d*)?'),	# inglise täis- või reaalarv
	('estnumber'	,r'\d+(,\d*)?'),	# eesti täis- või reaalarv
	('punkt'	,r'\.'),			# punkt
	('koma'		,r',|\\b,,'),			# koma
	('küsimus'	,r'\?+'),			# küsilause
	('hüüe'		,r'!+|\\b!+'),			# hüüdlause
	('aritmkood'	,r'[+\-*/]'),		# aritmeetilised operaatorid
	('semikoolon'	,r';'),			# väljendusüksus
	('koolon'	,r':'),			# loeteludefinitsioon
	('võrdne'	,r'='),			# võrdne, kas mates või kirjanduses ülekantud tähenduses
	('jutumärgid'	,r'"'),			# jutumärgid
	('sulgalgab'	,r'\('),		# sulud algavad
	('sulglõpeb'	,r'\)'),		# sulud lõpevad
	('mail2'	,r'\w+@\w+.\w+.\w+'),		# sõnad
	('mail'		,r'\w+@\w+.\w+'),		# sõnad
	('sõna'		,r'\w+'),		# sõnad
	]

	tokiregavaldused = '|'.join('(?P<%s>%s)' % paar for paar in tokenitüübid)
	for sõne in re.finditer(tokiregavaldused,kood):
		kinder = sõne.lastgroup
		väärtus = sõne.group(kinder)
		yield Toki(kinder,väärtus)

