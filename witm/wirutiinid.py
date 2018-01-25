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
lib_path = os.path.abspath(os.path.join('..', 'htdocs'))
sys.path.append(lib_path)
import html as h
lib_path = os.path.abspath(os.path.join('..', 'konf'))
sys.path.append(lib_path)
import dbconf as d
lib_path = os.path.abspath(os.path.join('..', 'sql'))
sys.path.append(lib_path)
import dbparingud as db
import wisql as s

def tõlgisõna(tõlkenumber,lähtekeel,sihtkeel,viis):
	import rutiinid as r
	import time
	nimisõna = tõlgitulemus = ""
	for r in s.sqle(d.n,db.valitõlkesõnad(tõlkenumber)):
		algus = time.time()
		sõna = r['lsõ']; pid = r['id']
		tõlgitulemus = sõnavõrdlus(tõlkenumber,lähtekeel,sihtkeel,sõna,pid,'snv0')
		if tõlgitulemus != 0:
			lõpp = time.time() - algus
			if viis == "wwwdebug":
				h.k("<tr><td>....")
				h.k(sõna)
				h.k("</td><td>")
				h.k(lõpp)
				h.k("</td></tr>")
			continue
		if len(sõna) < 4:
			# tundmatuid alla neljatähelisi sõnu pole mõtet tüvi+lõpp
			# rutiinidesse saata, peale tüve lõppu ära ei mahu
			continue
		# siia kontroll, kas sõna om üldse õnnõ suure tähega, vai om egäl puul väiko tähega
		sõna = sõna.lower()
		tõlgitulemus = sõnavõrdlus(tõlkenumber,lähtekeel,sihtkeel,sõna,pid,'snv1')
		if tõlgitulemus != 0:
			continue
		# analüüsib grammarit, aga tulemuse väljastab siis, kui saab võrukeelse lõppsõna, seega osa tööd mõtetult kaob
		tõlgitulemus = lihttõlge_erinditest(tõlkenumber,sõna,pid,lähtekeel,sihtkeel)
		if tõlgitulemus != 0:
			lõpp = time.time() - algus
			if viis == "wwwdebug":
				h.k("<tr><td>....")
				h.k(sõna)
				h.k("</td><td>")
				h.k(lõpp)
				h.k("</td></tr>\n\r<tr>")
			continue
		# see osa on aeglane, võiks optimeerida
		leialõpuliited(sõna,lähtekeel,pid,'lll')
		# siia vahele ülejäänud arendus, kus kontrollitakse mitmetüve
		# võimalust, kui lõpud on olemas, aga ühtegi tüve kätte ei saadud
		tüvekontroll(sihtkeel,pid)
		tõlgilõpuliited(lähtekeel,sihtkeel,pid)
		# veelkord :)))
		tüvekontroll(sihtkeel,pid)
		lõpp = time.time() - algus
		if viis == "wwwdebug":
			h.k("<tr><td>....")
			h.k(sõna)
			h.k("</td><td>")
			h.k(lõpp)
			h.k("</td></tr>\n\r<tr>")

def sihtkeelde(tõlkenumber,lähtekeel,sihtkeel,viis):
	import rutiinid as r
	import time
	nimisõna = tõlgitulemus = ""
	for r in s.sqle(d.n,db.valitõlkesõnad(tõlkenumber)):
		algus = time.time()
		sõna = r['lsõ']; pid = r['id']
		genereerisõna(lähtekeel,sihtkeel,pid)	
		#päälttöötlus(lähtekeel,sihtkeel,tõlkenumber)

def lopylausõstaminy(tõlkenumber):
	"""Loeb tõlketõlkenumberist kogu teksti ja jagab osalauseteks"""
	# XXX Paremini saab seda teha siis, kui teha süntaksianalüüsiga koos ->
	# XXX järelikult tuleks seda osa hilisemaks tõsta
	# XXX A edimält tulõ-õks punkti ni koma kotussõ päält är' lausõsta, selle et
	# XXX muido tulõ suurõ möla päält katssata sõnna lauseh.
	# XXX peräh tulõ nummõrtiisi lihtsahe ümbre nõsta
	osalausenr = lausenr = sõnanr = osasõnanr = 1
	for index,r in enumerate(s.sqle(d.n,db.sõnadsõnanumbrikaupa(tõlkenumber))):
		s.sqli(d.n,db.nummerdasõnadlausetes(sõnanr,osasõnanr,lausenr,osalausenr,r['id'],r['tasn']))
		if (r['lsõ'] == ',') or (r['lsõ'] == ':') or (r['lsõ'] == ';'):
			# XXX kui punkt, koma või koolon on sõna sees, nagu arv, MAC-aadress, jne.
			osalausenr += 1
			osasõnanr = 0
		elif (r['lsõ'] == '.') or (r['lsõ'] == '?') or (r['lsõ'] == '!'):
			lausenr += 1
			sõnanr = 0
			osasõnanr = 0
			osalausenr = 1
		sõnanr += 1
		osasõnanr += 1

def valitõlge(tõlkenumber,viis):
	tekst = tõlgitudtekst = ""
	s.sqli(d.n,db.vormikutestsõnadesse(tõlkenumber))
	päring = db.valiparalleeltõlge(tõlkenumber)
	#s.sqli(d.n,db.ennetõlget(tõlkenumber))
	if viis == "www" or viis == "wwwdebug":
		h.k("  <td>")
	for index,r in enumerate(s.sqle(d.n,päring)):
		if (r['tõlge'] == '.') or (r['tõlge'] == ',') or (r['tõlge'] == '!') or (r['tõlge'] == '?'):
			tõlgitudtekst = tõlgitudtekst + r['tõlge']
		else:
			if r['tõlge'] == None:
				tõlge = ''
			elif r['tõlge'] == 'None': 
				tõlge = ''
			else:
				tõlge = r['tõlge']
			tõlgitudtekst = tõlgitudtekst + " " + tõlge
	print(tõlgitudtekst)
	if viis == "www" or viis == "wwwdebug":
		h.kr("</td>")
	s.sqli(d.n,db.tõlkelausessetõlgejuurde(tõlgitudtekst,tõlkenumber))

def leialõpuliited(sõna,lähtekeel,pid,kus):
	if lähtekeel == 'et':
		tul = s.sqli(d.n,db.leialõpuliited_et(pid,sõna))
	elif lähtekeel == 'vro':
		tul = s.sqli(d.n,db.leialõpuliited_vro(pid,sõna))
	else: h.k("Maoli maas, näoli sees")
	return tul

def tõlgilõpuliited(lähtekeel,sihtkeel,pid):
	if lähtekeel == 'et' and sihtkeel == 'vro':
		s.sqli(d.n,db.tõlgilõpuliited_etvro(pid))
	elif lähtekeel == 'vro' and sihtkeel == 'et':
		h.k("Hetkel pole veel toetatud.")
	else: h.k("Pole toetatud. Ei tule ka. V.a., kui keegi finantseerib. V2")

def genereerisõna(lähtekeel,sihtkeel,pid):
	if lähtekeel == 'et' and sihtkeel == 'vro':
		s.sqli(d.n,db.genereerisõna_etvro(pid))
	elif lähtekeel == 'vro' and sihtkeel == 'et':
		h.k("Hetkel toetusest maas - vanad tabelid uuendamata.")
		#s.sqli(d.n,db.genereerisõna_vroet(pid))
	else: h.k("Pole toetatud. Ei tule ka. V.a., kui keegi finantseerib.")

def sõnavõrdlus(tõlkenumber,lähtekeel,sihtkeel,sõna,pid,kus):
	"""Tõlgib sõna, tagastab sõnade ja grammatika massiivi."""
	leitudsõnanr = 0
	sõna = sõna.replace("\\'",r"''")
	if lähtekeel == 'et' and sihtkeel == 'vro':
		sisestus = db.võrdlesõna_etvro(sõna)
	elif lähtekeel == 'vro' and sihtkeel == 'et':
		sisestus = db.võrdlesõna_vroet(sõna)
		#sisestus = db.tõlgisõna_vroet(sõna)
	else: h.k("Häki edasi, siia poldud ette nähtud jõuda... Versioon 0.1")
	for index,r in enumerate(s.sqlf(d.n,sisestus)):
		sihtsõna = r[0].replace("'", r"\''")
		grammar = r[1]
		leitudsõnanr += 1
		if index == 0:
			s.sqli(d.n,db.uuendatõlkesõna(sihtsõna,grammar,pid,kus))
		elif index > 0:
			s.sqli(d.n,db.sisestatõlkesõnadesse(sihtsõna,grammar,pid,kus))
	return leitudsõnanr

def lihttõlge_erinditest(tõlkenumber,sõna,pid,lähtekeel,sihtkeel):
	"""Tõlgib sõna, tagastab sõnade ja grammatika massiivi."""
	leitudsõnanr = 0
	sõna = sõna.replace("\\'",r"''")
	if lähtekeel == 'et' and sihtkeel == 'vro':
		sisestus0 = db.erindid_etvro(sõna)
	elif lähtekeel == 'vro' and sihtkeel == 'et':
		sisestus0 = db.erindid_vroet(sõna)
	else: h.k("Häki edasi, siia poldud ette nähtud jõuda... Versioon 0.2")
	for index,r in enumerate(s.sqlf(d.n,sisestus0)):
		sihtsõna = r[0].replace("'", r"\''")
		grammar = r[1]; sihtgrammar = r[2]
		leitudsõnanr += 1
		if index == 0:
			s.sqli(d.n,db.uuendatõlkesõna(sihtsõna,grammar,pid,'erindivõrdlus0'))
		else:
			s.sqli(d.n,db.sisestatõlkesõnadesse(sihtsõna,grammar,pid,'erindivõrdlus1'))
	return leitudsõnanr

def päälttöötlus(lähtekeel,sihtkeel,tõlkenumber):
	päring = db.päälttõlkmist(tõlkenumber)
	for index,r in enumerate(s.sqle(d.n,päring)):
		if (r['tõlge'] == '.') or (r['tõlge'] == ',') or (r['tõlge'] == '!') or (r['tõlge'] == '?'):
			tõlgitudtekst = tõlgitudtekst + r['tõlge']

def testiliidetearvu(pid):
	arv = s.sqli(d.n,db.küsiliidetearvu(pid))
	return arv

def tüvekontroll(sihtkeel,pid):
	if sihtkeel == 'vro':
		tul = s.sqli(d.n,db.tüvekontra(pid))
