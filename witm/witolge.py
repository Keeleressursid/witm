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
import wirutiinid as wi
import syntaks as s
import rutiinid as r
import traceback

def main(tekst,lähtekeel,sihtkeel,dikt,viis):
	lib_path = os.path.abspath(os.path.join('..', 'htdocs'))
	sys.path.append(lib_path)
	import html as h
	# XXX dikt
	"""WI liidese tõlkemasina peaprogramm"""
	import time
	try:
		algusaeg = time.time()
		tõlkenumber = r.uustõlkenumber()
		lõppaeg = time.time() - algusaeg
		r.www2db(tõlkenumber,lähtekeel,sihtkeel,tekst,viis)
		if viis=="wwwdebug":
			h.k("<td><table><tr><td>peale www2db-d: </td><td>")
			h.k(lõppaeg)
			h.k("</td></tr>")

		blokiaeg = time.time()
		r.sõnetatekst(tõlkenumber)
		lõppaeg = time.time() - blokiaeg
		if viis=="wwwdebug":
			h.k("<tr><td>sõneta+lausesta:</td><td>")
			h.k(lõppaeg)
			h.k("</td></tr>")

		tõlke1aeg = time.time()
		wi.tõlgisõna(tõlkenumber,lähtekeel,sihtkeel,viis)	# enne genereerisõna
		lõppaeg = time.time() - tõlke1aeg
		if viis=="wwwdebug":
			h.k("<tr><td>tõlgi1:</td><td>")
			h.k(lõppaeg)
			h.k("</td></tr>")
		
		süntaksiaeg = time.time()
		wi.lopylausõstaminy(tõlkenumber)
		#s.süntaks(tõlkenumber,lähtekeel,sihtkeel,viis)
		lõppaeg = time.time() - süntaksiaeg
		if viis=="wwwdebug":
			h.k("<tr><td>süntaksiaeg:</td><td>")
			h.k(lõppaeg)
			h.k("</td></tr></table></td>")

		tõlke2aeg = time.time()
		#wi.sihtkeelde(tõlkenumber,lähtekeel,sihtkeel,viis)	# genereerisõna
		wi.valitõlge(tõlkenumber,viis)
		lõppaeg = time.time() - tõlke2aeg
		if viis=="wwwdebug":
			h.kr("<tr><td></td><td>")
			h.k("  <table><tr><td>tõlgi2:</td><td>")
			h.k(lõppaeg)
			h.kr("</td></tr>")

		koguaeg = time.time() - algusaeg
		if viis=="wwwdebug":
			h.k("  <tr><td>tõlke koguaeg:</td><td>")
			h.k(koguaeg)
			h.kr("</td></tr>\n  </table>")
		if viis=="www" or viis == "wwwdebug":
			h.kr("</tr></table>")

	except:
		h.k("<pre>")
		traceback.print_exc()
		h.kr("</pre>")

if __name__ == '__main__':
	import sys
	tekst = ""
	tekst = sys.stdin.readlines()
	tekst = [rida.replace('\n', '') for rida in tekst]
	main(tekst,"et","vro","dikt4_vro_et","käsurida")
