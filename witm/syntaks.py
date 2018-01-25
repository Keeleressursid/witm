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

import wisql as s
import dbparingud as db
import dbconf as d

def süntaks(tõlkenumber,lähtekeel,sihtkeel,viis):
	import rutiinid as r
	import time
	nimisõna = tõlgitulemus = ""
	sõnad = []
	indeks = []
	krammar = []
	klass = []
	for r in s.sqle(d.n,db.valikõiksõnad(tõlkenumber)):
		algus = time.time()
		# loetakse grammar sisse
		# tegelikult loetakse kogu staaf sisse, et hakata modelleerima
		sõna = r['lsõ']; pid = r['id'];
		grammar = r['lkl']; klaß = r['lgr'];
		sõnad.append(sõna); indeks.append(pid); krammar.append(grammar)
		klass.append(klaß)
		# grammaris peab olema kirjas VB.
		# kui VB, siis kas 1) olema; 2) omama; 3) muu
		# kui olema, siis vaadatakse aega ja arvu.
		# sihtsõna tõlkimisse peab "olema" korral arvu arvestatama

		# tuleb teha kolmemõõtlemine massiiv...

	if viis=='wwwdebug' or viis=='käsurida':
		print(sõnad); print(indeks); print(krammar); print(klass)
	# Nimekiri, millised toetused esmalt:
	#	arvu leidmine
	#	eitus-jaatus
	#	tegumoe leidmine, hiljem
	#	aja leidmine, mitte nii vajalik

	# arv: üks on nimisõna mitmus, teine on ainsus + arvsõna,
	#		mille tuge hetkel pole
