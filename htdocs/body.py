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

def vaikimisi():
	pass

def menüürida():
	h.viide('wi.py?z=o','Otsi tekstidest |')
	h.viide('wi.py?z=ontl','Otsi sõnaraamatutest |')
	h.viide('wi.py?z=vaa','Allikad |')
	h.viide('wi.py?z=vat','Tekstid')

def witekstideinfo():
	wilauseid=witekstidearv()
	h.k("Eesti - võru paralleelkorpuste andmebaasis on (")
	h.a(wilauseid)
	h.k(") lausehaaval käsitsi joondatud teksti.")
	h.k(" Ühes keeles on mitu lauset koos juhul kui teises keeles on liitlause.")
	h.k(" Tekstide loetelus on toodud iga teksti esimene lause.")
	h.kr("<br>")
	h.k("Eestikeelseid sõnu on ")
	h.a(et_sõnadearv())
	h.k(", võrukeelseid sõnu on ")
	h.a(vro_sõnadearv())
	h.kr(".<br>")

def vaatatekste():
	sql = """SELECT t.nr AS tnr,t.allikas AS tallikas,t.nimi_et AS etnimi,t.kirjeldus_et AS etkirjeldus,
		t.kirjeldus_vro AS vrokirjeldus, t.nimi_vro AS vro_nimi, a.kirjeldus_et AS akirjeldus
		FROM witekst t, wiallikas a WHERE t.allikas=a.id ORDER BY t.nr;"""
	h.tabel_a()
	h.tr_l()
	h.td("allikas",'d')
	h.td("nr",'d')
	h.td("eesti",'d')
	h.td("võru",'d')
	h.tr_l()
	for r in s.sqle(d.n,sql):
		h.tr_l()
		h.td(r['akirjeldus'],'d')
		nr = str(r['tnr'])
		viide = "wi.py?z=vati&nr=" + nr
		h.atd('aeg r',viide,nr)
		h.td(r['etkirjeldus'],'d')
		h.td(r['vrokirjeldus'],'d')
		h.tr_l()
	h.tabel_l()

def vaataallikaid():
	sql = "SELECT * FROM wiallikas;"
	h.tabel_a()
	for r in s.sqle(d.n,sql):
		h.tr_l()
		h.td(r['nimi_et'],'d')
		h.td(r['kirjeldus_et'],'d')
		h.td(r['nimi_vro'],'d')
		h.td(r['kirjeldus_vro'],'d')
		h.tr_l()
	h.tabel_l()

def vaatateksti(nr):
	h.k("<h4>Tekst nr: ")
	h.a(nr)
	h.kr("</h4>")
	sql = "SELECT et.lausenr AS nr, et.lause AS etlause, vro.lause AS vrolause FROM wilaused_et et, wilaused_vro vro WHERE et.nr='%s' AND vro.nr='%s' AND et.lausenr=vro.lausenr ORDER BY et.lausenr;" % (nr,nr)
	h.tabel_a()
	for r in s.sqle(d.n,sql):
		h.tr_l()
		h.td(r['nr'],'d')
		h.td(r['etlause'],'d')
		h.td(r['vrolause'],'d')
		h.tr_l()
	h.tabel_l()

def otsiabi():
	h.k("Otsida saab mitu sõna korraga, hetkel miinusmärki väljajättena ei toetata.")
	h.kr("Vaikimisi otsitakse mitte terveid sõnu vaid sõnesid pikemate sõnede sees.")

def otsi():
	h.kr("<h4>OTSI (tekstidest)</h4>")
	viide = str("wi.py?z=o3&x=3")
	h.vorm(viide)
	h.kr("<br>")
	h.tabel_a()
	h.inputval("s","sõna",100,100)
	h.submit('2','Otsida saab mitu sõna korraga. Vali otsitav sõna(d) eesti keeles')
	h.tabel_l()
	h.kr("</form>")           
	viide = str("wi.py?z=o3&x=4")
	h.vorm(viide)
	h.tabel_a()
	h.inputval("s","sõnna",100,100)
	h.submit('2','Otsi saat kõrraga üts kooni mitu sõnna. Kae otstavat sõnna/u võro keeleh')
	h.tabel_l()
	h.kr("</form>")           
	viide = str("wi.py?z=o3&x=5")
	h.vorm(viide)
	h.kr("<br>")
	h.tabel_a()
	h.inputval("s","sõna",100,100)
	h.submit('2','TEST, sorteerituna sõnade arvu ja lause pikkuse järgi')
	h.tabel_l()
	h.kr("</form>")           
	viide = str("wi.py?z=o3&x=6")
	h.vorm(viide)
	h.kr("<br>")
	h.tabel_a()
	h.inputval("s","sõna",100,100)
	h.submit('2','TEST, sõnnu ja lause pikkuse perrä sortitu')
	h.tabel_l()
	h.kr("</form>")           
	h.k("OMADUSED/FEATURES: ")
	h.kr("tõstutundlikkuse tuge veel pole. Tegelikult on, aga veebiliideses veel ei värvita selliseid sõnu ning seepärast pole seda sisselülitatud.")

def otsi2(sona,x):
	import re
	h.kr("<h4>Tulemused:</h4>")
	h.k("Sõna oli: \"")
	h.k(sona)
	h.kr("\"")
	sona2 = re.escape(sona)
	sona = sona.replace("\'","\\''")
	if (x == '1'):
		sone="""SELECT e.id AS eid, e.nr AS enr, e.lausenr AS elnr, e.lause AS el, v.lause AS vl FROM wilaused_et e, wilaused_vro v WHERE e.lause ilike '%%%s%%' AND e.nr=v.nr AND v.lausenr=e.lausenr ORDER BY enr,elnr;""" % sona
	elif (x == '2'):
		sone="""SELECT e.id AS eid, e.nr AS enr, e.lausenr AS elnr, e.lause AS el, v.lause AS vl FROM wilaused_et e, wilaused_vro v WHERE v.lause ilike '%%%s%%' AND e.nr=v.nr AND v.lausenr=e.lausenr ORDER BY enr,elnr;""" % sona
	else:
		h.kr("Keelevalik puudus?")

	h.tabel_a()
	h.tr_l()
	h.td("töö nr",'d')
	h.td("lause nr",'d')
	h.td("lause",'d')
	h.td("lause",'d')
	h.tr_l()
	for r in s.sqle(d.n,sone):
		h.tr_l()
		enr = str(r['enr'])
		viide = "wi.py?z=vati&nr=" + enr
		h.atd('aeg r',viide,enr)
		elnr = str(r['elnr'])
		viide2 = "wi.py?z=val&tnr=" + elnr + "&lnr=" + enr
		h.atd('aeg r',viide2,elnr)
		h.td(r['el'],'d')
		h.td(r['vl'],'d')
		h.tr_l()
	h.tabel_l()

def otsi3(sona,x):
	import re
	h.kr("<h4>Tulemused:</h4>")
	h.k("Sõne oli: \"")
	h.k(sona)
	h.kr("\"")
	sona = sona.split(' ')
	if (x == '3'):
		sone="""SELECT e.id AS eid, e.nr AS enr, e.lausenr AS elnr, e.lause AS el, v.lause AS vl FROM wilaused_et e, wilaused_vro v WHERE e.lause ~ ANY(ARRAY %s ) AND e.nr=v.nr AND v.lausenr=e.lausenr ORDER BY enr,elnr;""" % sona
	elif (x == '4'):
		sone="""SELECT e.id AS eid, e.nr AS enr, e.lausenr AS elnr, e.lause AS el, v.lause AS vl FROM wilaused_et e, wilaused_vro v WHERE v.lause ~ ANY(ARRAY %s ) AND e.nr=v.nr AND v.lausenr=e.lausenr ORDER BY enr,elnr;""" % sona
	elif (x == '5'):
		sone=""" WITH essa AS (SELECT e.id AS eid, e.nr AS enr, e.lausenr AS elnr, e.lause AS el, v.lause AS vl, CHAR_LENGTH(e.lause) AS epikk FROM wilaused_et e, wilaused_vro v WHERE e.lause ~ ANY(ARRAY %s ) AND e.nr=v.nr AND v.lausenr=e.lausenr ORDER BY enr,elnr), tessa AS ( SELECT regexp_split_to_table(el, E'\\\\s+') AS esõna,epikk,eid,enr,elnr FROM ESSA), kossa AS ( SELECT esõna,epikk,eid,enr,elnr FROM tessa WHERE esõna ~ ANY(ARRAY %s )), nessa AS ( SELECT COUNT(esõna) AS korda, epikk,enr,elnr FROM kossa GROUP BY epikk,enr,elnr ORDER BY korda DESC,epikk) SELECT e.lause AS el, v.lause AS vl,epikk,korda,enr,elnr from nessa n,wilaused_et e, wilaused_vro v WHERE enr=e.nr AND elnr=e.lausenr AND e.nr=v.nr AND v.lausenr=e.lausenr AND enr=v.nr AND elnr=v.lausenr ORDER BY korda DESC,epikk ;""" % (sona,sona)
	elif (x == '6'):
		sone=""" WITH essa AS (SELECT e.id AS eid, e.nr AS enr, e.lausenr AS elnr, e.lause AS el, v.lause AS vl, CHAR_LENGTH(e.lause) AS epikk FROM wilaused_et e, wilaused_vro v WHERE v.lause ~ ANY(ARRAY %s ) AND e.nr=v.nr AND v.lausenr=e.lausenr ORDER BY enr,elnr), tessa AS ( SELECT regexp_split_to_table(vl, E'\\\\s+') AS vsõna,epikk,eid,enr,elnr FROM ESSA), kossa AS ( SELECT vsõna,epikk,eid,enr,elnr FROM tessa WHERE vsõna ~ ANY(ARRAY %s )), nessa AS ( SELECT COUNT(vsõna) AS korda, epikk,enr,elnr FROM kossa GROUP BY epikk,enr,elnr ORDER BY korda DESC,epikk) SELECT e.lause AS el, v.lause AS vl,epikk,korda,enr,elnr FROM nessa n,wilaused_et e, wilaused_vro v WHERE enr=e.nr AND elnr=e.lausenr AND e.nr=v.nr AND v.lausenr=e.lausenr AND enr=v.nr AND elnr=v.lausenr ORDER BY korda DESC,epikk ;""" % (sona,sona)
	else:
		h.kr("Keelevalik puudus?")

	h.tabel_a()
	h.tr_l()
	h.td("töö nr",'d')
	h.td("lause nr",'d')
	h.td("lause",'d')
	h.td("lause",'d')
	h.tr_l()
	for r in s.sqle(d.n,sone):
		h.tr_l()
		enr = str(r['enr'])
		viide = "wi.py?z=vati&nr=" + enr
		h.atd('aeg r',viide,enr)
		elnr = str(r['elnr'])
		viide2 = "wi.py?z=val&tnr=" + elnr + "&lnr=" + enr
		h.atd('aeg r',viide2,elnr)
		if (x == '3'):
			kogulause = r['el']
		elif (x == '4'):
			kogulause = r['vl']
		elif (x == '5'):
			kogulause = r['el']
		elif (x == '6'):
			kogulause = r['vl']
		for i in sona:
			kogulause = kogulause.replace(i,"<font color=\"blue\">" + i + "</font>")
		if (x == '3'):
			h.td(kogulause,'d')
			h.td(r['vl'],'d')
		elif (x == '4'):
			h.td(kogulause,'d')
			h.td(r['el'],'d')
		elif (x == '5'):
			h.td(kogulause,'d')
			h.td(r['vl'],'d')
			h.td(r['korda'],'d')
			h.td(r['epikk'],'d')
		elif (x == '6'):
			h.td(kogulause,'d')
			h.td(r['el'],'d')
			h.td(r['korda'],'d')
			h.td(r['epikk'],'d')
		h.tr_l()
	h.tabel_l()

def witekstidearv():
	sql = "SELECT max(nr) AS summa FROM witekst;"
	for r in s.sqle(d.n,sql):
		return(r['summa'])

def et_sõnadearv():
	import string
	sql = """with essa as (select count(token) AS et from (select unnest(regexp_matches(w.lause, E'\\\\S+','g')) as token from wilaused_et as w ) as tokens)
        select sum(et) as et from essa;
        """
	for r in s.sqle(d.n,sql):
		return(r['et'])

def vro_sõnadearv():
	sql = """with essa as (select count(token) AS vro from (select unnest(regexp_matches(w.lause, E'\\\\S+','g')) as token from wilaused_vro as w ) as tokens)
        select sum(vro) as vro from essa ;"""
	for r in s.sqle(d.n,sql):
		return(r['vro'])

def sõnaka1_sõnnuarv():
	sql = """select count(*) as sum from dikt4_vro_et;"""
	for r in s.sqle(d.n,sql):
		return(r['sum'])

def sõnaka3_sõnnuarv():
	sql = """select count(*) as sum from dikt4_vro_et;"""
	for r in s.sqle(d.n,sql):
		return(r['sum'])

def vaatalauset(lnr,tnr):
	h.k("Töö nr: ")
	h.a(tnr)
	h.k(" Lause nr: ")
	h.a(lnr)
	h.kr(".")
	vlnr = int(lnr) - 2
	slnr = int(lnr) + 2
	sql = "SELECT et.lausenr AS nr, et.lause AS etlause, vro.lause AS vrolause FROM wilaused_et et, wilaused_vro vro WHERE et.nr='%s' AND vro.nr='%s' AND et.lausenr=vro.lausenr  AND et.lausenr >= '%s' and et.lausenr <= '%s' ORDER BY et.lausenr;" % (tnr,tnr,vlnr,slnr)
	h.tabel_a()
	for r in s.sqle(d.n,sql):
		h.tr_l()
		h.td(r['nr'],'d')
		h.td(r['etlause'],'d')
		h.td(r['vrolause'],'d')
		h.tr_l()
	h.tabel_l()

def otsinäitelausist():
	h.kr("<h4>OTSI (sõnaraamatute näitelausetest)</h4>")
	viide = str("wi.py?z=ontl2&x=3")
	h.vorm(viide)
	h.kr("<br>")
	h.tabel_a()
	h.inputval("s","sõna",100,100)
	h.submit('2','Otsida saab mitu sõna korraga. Vali otsitav sõna(d) eesti keeles')
	h.tabel_l()
	h.kr("</form>")           
	viide = str("wi.py?z=ontl2&x=4")
	h.vorm(viide)
	h.tabel_a()
	h.inputval("s","sõnna",100,100)
	h.submit('2','Otsi saat kõrraga üts kooni mitu sõnna. Kae otstavat sõnna/u võro keeleh')
	h.tabel_l()
	h.kr("</form>")           
	viide = str("wi.py?z=ontl2&x=5")
	h.vorm(viide)
	h.kr("<br>")
	h.tabel_a()
	h.inputval("s","sõna",100,100)
	h.submit('2','TEST, sorteerituna sõnade arvu ja lause pikkuse järgi')
	h.tabel_l()
	h.kr("</form>")           
	viide = str("wi.py?z=ontl2&x=6")
	h.vorm(viide)
	h.kr("<br>")
	h.tabel_a()
	h.inputval("s","sõna",100,100)
	h.submit('2','TEST, sõnnu ja lause pikkuse perrä sortitu')
	h.tabel_l()
	h.kr("</form>")           
	h.k("OMADUSED/FEATURES: ")
	h.kr("tõstutundlikkuse tuge veel pole. Tegelikult on, aga veebiliideses veel ei värvita selliseid sõnu ning seepärast pole seda sisselülitatud.")

def otsi2(sona,x):
	import re
	h.kr("<h4>Tulemused:</h4>")
	h.k("Sõna oli: \"")
	h.k(sona)
	h.kr("\"")
	sona2 = re.escape(sona)
	sona = sona.replace("\'","\\''")
	if (x == '1'):
		sone="""SELECT e.id AS eid, e.nr AS enr, e.lausenr AS elnr, e.lause AS el, v.lause AS vl FROM wilaused_et e, wilaused_vro v WHERE e.lause ilike '%%%s%%' AND e.nr=v.nr AND v.lausenr=e.lausenr ORDER BY enr,elnr;""" % sona
	elif (x == '2'):
		sone="""SELECT e.id AS eid, e.nr AS enr, e.lausenr AS elnr, e.lause AS el, v.lause AS vl FROM wilaused_et e, wilaused_vro v WHERE v.lause ilike '%%%s%%' AND e.nr=v.nr AND v.lausenr=e.lausenr ORDER BY enr,elnr;""" % sona
	else:
		h.kr("Keelevalik puudus?")

	h.tabel_a()
	h.tr_l()
	h.td("töö nr",'d')
	h.td("lause nr",'d')
	h.td("lause",'d')
	h.td("lause",'d')
	h.tr_l()
	for r in s.sqle(d.n,sone):
		h.tr_l()
		enr = str(r['enr'])
		viide = "wi.py?z=vati&nr=" + enr
		h.atd('aeg r',viide,enr)
		elnr = str(r['elnr'])
		viide2 = "wi.py?z=val&tnr=" + elnr + "&lnr=" + enr
		h.atd('aeg r',viide2,elnr)
		h.td(r['el'],'d')
		h.td(r['vl'],'d')
		h.tr_l()
	h.tabel_l()

def otsintl2(sona,x):
	import re
	h.kr("<h4>Tulemused:</h4>")
	h.k("Sõne oli: \"")
	h.k(sona)
	h.kr("\"")
	sona = sona.split(' ')
	if (x == '3'):
                sone="""SELECT i,id,et,vro,nr FROM sõ_eevro_laused WHERE et ~ ANY(ARRAY %s ) ORDER BY i,nr;""" % sona
	elif (x == '4'):
                sone="""SELECT i,id,et,vro,nr FROM sõ_eevro_laused WHERE vro ~ ANY(ARRAY %s ) ORDER BY i,nr;""" % sona
	elif (x == '5'):
		sone=""" with essa as (select i,id,et,vro,nr,CHAR_LENGTH(et) as ep FROM sõ_eevro_laused WHERE et ~ ANY(ARRAY %s ) ORDER BY i),
tessa as (SELECT regexp_split_to_table(et, E'\\\\s+') AS etsõna,i,id,et,vro,nr,ep FROM essa),
kossa as (SELECT etsõna,et,vro,i,id,nr,ep FROM tessa WHERE etsõna ~ ANY(ARRAY %s )),
nessa as (SELECT COUNT(etsõna) as korda, et,vro,nr,i,id FROM kossa GROUP BY et,vro,nr,i,id,ep ORDER BY korda DESC,ep)
select * from nessa;""" % (sona,sona)
	elif (x == '6'):
		sone=""" with essa as (select i,id,et,vro,nr,CHAR_LENGTH(et) as ep FROM sõ_eevro_laused WHERE vro ~ ANY(ARRAY %s ) ORDER BY i),
tessa as (SELECT regexp_split_to_table(vro, E'\\\\s+') AS vrosõna,i,id,et,vro,nr,ep FROM essa),
kossa as (SELECT vrosõna,et,vro,i,id,nr,ep FROM tessa WHERE vrosõna ~ ANY(ARRAY %s )),
nessa as (SELECT COUNT(vrosõna) as korda, et,vro,nr,i,id FROM kossa GROUP BY et,vro,nr,i,id,ep ORDER BY korda DESC,ep)
select * from nessa;""" % (sona,sona)
	else:
		h.kr("Keelevalik puudus?")

	h.tabel_a()
	h.tr_l()
	h.td("rea nr",'d')
	h.td("otsikeel",'d')
	h.td("paralleelkeel",'d')
	h.td("lause nr",'d')
	h.tr_l()
	for r in s.sqle(d.n,sone):
		h.tr_l()
		if (x == '3'):
			kogulause = r['et']
		elif (x == '4'):
			kogulause = r['vro']
		elif (x == '5'):
			kogulause = r['et']
		elif (x == '6'):
			kogulause = r['vro']
		for i in sona:
			kogulause = kogulause.replace(i,"<font color=\"blue\">" + i + "</font>")
		if (x == '3'):
			h.td(r['i'],'d')
			h.td(kogulause,'d')
			h.td(r['vro'],'d')
			h.td(r['nr'],'d')
		elif (x == '4'):
			h.td(r['i'],'d')
			h.td(kogulause,'d')
			h.td(r['et'],'d')
			h.td(r['nr'],'d')
		elif (x == '5'):
			h.td(kogulause,'d')
			h.td(r['vro'],'d')
			h.td(r['i'],'d')
			h.td(r['id'],'d')
			h.td(r['nr'],'d')
		elif (x == '6'):
			h.td(kogulause,'d')
			h.td(r['et'],'d')
			h.td(r['i'],'d')
			h.td(r['id'],'d')
			h.td(r['nr'],'d')
		h.tr_l()
	h.tabel_l()
