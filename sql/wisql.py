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

import sys, os
import string
import psycopg2
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
lib_path = os.path.abspath(os.path.join('..', 'konf'))
sys.path.append(lib_path)
from dbconf import konfig

def sqlp(db,sisu):
	try:
		yh = konfig(db)
		conn = psycopg2.connect(yh)
		cur = conn.cursor()
		cur.execute(sisu)
		rows = cur.fetchall()
		for r in rows:
			yield r
		conn.close()
	except Exception as e:
		print(e)

def sqle(db,sisu):
	"""Pärib, annab read"""
	import psycopg2
	import psycopg2.extras
	psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
	psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
	try:
		yh = konfig(db)
		conn = psycopg2.connect(yh)
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute(sisu)
		rows = cur.fetchall()
		for r in rows:
			yield r
	except Exception as e:
		print(e)

	conn.close()

def sqlf(db,sisu):
	"""Pärib, annab read, reanumbritega"""
	import psycopg2
	import psycopg2.extras
	psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
	psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
	try:
		yh = konfig(db)
		conn = psycopg2.connect(yh)
		cur = conn.cursor()
	except Exception as e:
		print(e)

	cur.execute(sisu)
	rows = cur.fetchall()
	for r in rows:
		yield r
	conn.close()

def sqli(db,sisu):
	"""Sisestab"""
	import psycopg2
	import psycopg2.extras
	psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
	psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
	try:
		yh = konfig(db)
		conn = psycopg2.connect(yh)
		cur = conn.cursor()
		cur.execute(sisu)
		conn.commit()
	except Exception as e:
		print(e)
		conn.close()
	return cur.rowcount
	conn.close()

def sqlr(db,sisu):
	"""Küsib ühte rida"""
	import psycopg2
	import psycopg2.extras
	psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
	psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
	try:
		yh = konfig(db)
		conn = psycopg2.connect(yh)
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute(sisu)
		conn.commit()
		return(cur.fetchone())
	except Exception as e:
		if conn:
			conn.rollback()
		print(e)
	conn.close()
