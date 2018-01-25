#!/usr/local/bin/python3
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

import cgi, cgitb, sys, codecs
import html as h
import funk_sn as fsn
import body as b

cgitb.enable()
writer = codecs.getwriter('utf8')(sys.stdout.buffer)
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

h.kr("\r\n")

h.pais('Võru keele paralleelkorpus')
h.kr("<div id=\"keha\">")
h.kr("<div id=\"kast\">")
h.kr("<div id=\"yl\">")
h.kr("<h3>Võru keele paralleelkorpus</h3>")
b.menüürida()
h.kr("</div>")
h.kr("<br>")
h.kr("<br><br>")
form = cgi.FieldStorage()
if form.getvalue('z'):
	z = form.getvalue('z')
	z = cgi.escape(z)
	if (z == "tee"):
		b.menüürida()
	elif (z == "vaa"):
		b.vaataallikaid()
	elif (z == "vat"):
		b.vaatatekste()
	elif (z == "vati"):
		if form.getvalue('nr'):
			nr = form.getvalue('nr')
		else:
			nr = '0'                          
		b.vaatateksti(nr)
	elif (z == "val"):
		if form.getvalue('tnr'):
			tnr = form.getvalue('tnr')
		else:
			tnr = '0'                          
		if form.getvalue('lnr'):
			lnr = form.getvalue('lnr')
		else:
			lnr = '0'                          
		b.vaatalauset(tnr,lnr)
	elif (z == "o"):
		b.otsiabi()
		b.otsi()
	elif (z == "o2"):
		if form.getvalue('x'):
			x = form.getvalue('x')
		else:
			x = '0'                          
		if form.getvalue('s'):
			s = form.getvalue('s')
		else:
			s = '0'                          
		b.otsi2(s,x)
	elif (z == "o3"):
		if form.getvalue('x'):
			x = form.getvalue('x')
		else:
			x = '0'                          
		if form.getvalue('s'):
			s = form.getvalue('s')
		else:
			s = '0'                          
		b.otsi3(s,x)
	elif (z == "ontl"):
		b.otsiabi()
		b.otsinäitelausist()
	elif (z == "ontl2"):
		if form.getvalue('x'):
			x = form.getvalue('x')
		else:
			x = '0'                          
		if form.getvalue('s'):
			s = form.getvalue('s')
		else:
			s = '0'                          
		b.otsintl2(s,x)
	else:
		z = 'vaikimisi'
else:
	b.witekstideinfo()

h.kr("</div>")
h.kr("</div>")
h.jalus()

