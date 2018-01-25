#!/usr/bin/python3
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
from array import array
import html as h
lib_path = os.path.abspath(os.path.join('..', 'konf'))
lib_path = os.path.abspath(os.path.join('..', 'sql'))
sys.path.append(lib_path)
import wisql as s
import dbconf as d

def avatekst():
	h.kr("<hr>")
	h.kr("<a href = \"sn.py?z=etvro\">Eesti-Võru</a> ja <a href = \"sn.py?z=vroet\">Võru-Eesti</a> digisõnaraamatus (esitatud häälduspõhiselt) on andmebaasis kõik võimalikud sünonüümi- ja misiganes variandid eraldi real. Veebiversioonis on erinevad sünonüümid toodud ühel real ning eraldatud komadega.")
	h.kr("Tegemist on ühest failist (võru-eesti) sisseloetud tõlkevastetega, mida protsessides on saadud ka nn. pöördtabel ehk eesti-võru sõnaraamat.")
	h.kr("Protsessitud on muutsõnade read ning algusest muutsõnade kirjeldused ning varieeruva pikkusega esimesed tõlked kuni kolme sõna pikkuseni, k.a. erinevas konfiguratsioonis komad, semikoolonid, sulud ning sünonüümide omistused ehk viited.")
	h.kr("Sulgudes olev (täpsustav) info läheb samuti eraldi tabelisse. Esimesed protsessimised on juba tehtud.<br>")

	h.kr("<a href = \"sn.py?z=puhasvro\">Puhastatud (võro)</a> (esitatud kirjapildis) sõnaraamatu võrukeelsete sõnade loend, kust on eraldi real sulgudes olevad alternatiivid ehk nii lisatähtedega variandid nt. -(l)l on nii -l kui ka -ll, aga ka -(h)n variandid, kus on nii -h kui -n.")

	h.kr("<hr>")
	h.kr("Siinkohal on <b>vanad</b> katsetused, mis on proof-of-concept põhimõttel kokkukleebitud:<br>")
	h.viide('sn.py?z=koikkaandsonad','Kõik muutsõnade kolme esimese käände või põhipöörde kirjeldused<br>')
	h.viide('sn.py?z=vroen','Võru inglise sõnaraamat, määneki vana variant')
	h.kr("<hr>")
	h.kr("Käesolev DB põhineb Sulev Iva / Jüvva Sullõvi ühele Võro - Eesti sõnaraamatu aluseks olevale vanale excelifailile.")

def vro_en_koik():
	sql = """SELECT vro,en from vro_en order by vro,en ;"""
	#sql = """SELECT COUNT(nr) AS palju, nr,om,os FROM käändsõnad_vro GROUP BY nr,om,os ORDER BY nr,palju DESC ;;"""
	h.tabel_a()
	h.kr("<tr><td>vro</td><td>en</td></tr>")
	for r in s.sqle(d.n,sql):
		h.tr_a()
		h.td(r['vro'],'d')
		h.td(r['en'],'d')
		h.tr_l()
	h.tabel_l()

def kaanded():
	h.h3('Käänded')
	sql = """SELECT nr,nim,om,os from käändsõnad_vro ORDER BY nim,om,os;"""
	h.tabel_a()
	h.kr("<tr><td>nr</td><td>nim</td><td>om</td><td>os</td></tr>")
	for r in s.sqle(d.n,sql):
		h.tr_a()
		h.td(r['nr'],'d')
		h.td(r['nim'],'d')
		h.td(r['om'],'d')
		h.td(r['os'],'d')
		h.tr_l()
	h.tabel_l()

def yhesugusedkaandelopud():
	h.h3('Ühesugused käändelõpud')
	sql = """SELECT COUNT(nr) AS palju, nr,om,os FROM käändsõnad_vro GROUP BY nr,om,os ORDER BY nr,palju DESC ;;"""
	h.tabel_a()
	h.kr("<tr><td>palju</td><td>nr</td><td>om</td><td>os</td></tr>")
	for r in s.sqle(d.n,sql):
		h.tr_a()
		h.td(r['palju'],'d')
		h.td(r['nr'],'d')
		h.td(r['om'],'d')
		h.td(r['os'],'d')
		h.tr_l()
	h.tabel_l()

def kaandeloppuderuhmad():
	h.h3('Käändelõppude rühmad')
	sql = """with algus as (select count(nr) as mitu, nr as käändk,om as omastav,os as osastav from käändsõnad_vro  group by nr,om,os order by nr,mitu desc) select mitu,käändk,omastav,osastav from algus where mitu > 1 order by omastav,osastav;"""
	h.tabel_a()
	h.kr("<tr><td>sõnadearv</td><td>käändkonna nr</td><td>omastav</td><td>osastav</td></tr>")
	for r in s.sqle(d.n,sql):
		h.tr_a()
		h.td(r['mitu'],'d')
		h.td(r['käändk'],'d')
		h.td(r['omastav'],'d')
		h.td(r['osastav'],'d')
		h.tr_l()
	h.tabel_l()

def etvro():
	sql = """SELECT eesti,võro FROM eesti_võru_sõnaraamat ORDER BY eesti,võro;"""
	h.tabel_a()
	h.kr("<tr><td>Eesti</td><td>Võro</td></tr>")
	for r in s.sqle(d.n,sql):
		h.tr_a()
		h.td(r['eesti'],'d')
		h.td(r['võro'],'d')
		h.tr_l()
	h.tabel_l()

def vroet():
	sql = """SELECT võro,eesti FROM võru_eesti_sõnaraamat ORDER BY võro,eesti;"""
	h.tabel_a()
	h.kr("<tr><td>Võro</td><td>Eesti</td></tr>")
	for r in s.sqle(d.n,sql):
		h.tr_a()
		h.td(r['võro'],'d')
		h.td(r['eesti'],'d')
		h.tr_l()
	h.tabel_l()

def puhasvro():
	sql = """SELECT * FROM puhas_vro ORDER BY sõna,hg;"""
	h.kr("<br>Iva ID on ivasõnaraamatu rea ID, mille abil saab sõnu tagasisiduda")
	h.tabel_a()
	h.kr("<tr><td>ID</td><td>Sõna</td><td>homograaf</td></tr>")
	for r in s.sqle(d.n,sql):
		h.tr_a()
		h.td(r['iid'],'d')
		h.td(r['sõna'],'d')
		h.td(r['hg'],'d')
		h.tr_l()
	h.tabel_l()

def tprojektid():
	sql = """SELECT * FROM tõlkelause where (lke='et' and ske='vro') or (lke='vro' and ske='et') ORDER BY pro DESC;"""
	h.kr("<br>Projektid")
	h.tabel_a()
	h.kr("<tr><td>ID</td><td>Sõna</td><td>homograaf</td></tr>")
	for r in s.sqle(d.n,sql):
		h.tr_a()
		h.td(r['pro'],'d')
		h.td(r['lähtelause'],'d')
		h.td(r['sihtlause'],'d')
		h.tr_l()
	h.tabel_l()
