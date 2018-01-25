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

def valitõlkesõnad(tõlkenumber):
	päring = """SELECT
	id,
	lsõ
FROM	
	tõlkesõnad
WHERE
	ssõ IS NULL
AND
	tnr = '%s'
AND
	t = 'sõna'
ORDER BY
	tasn;""" % (tõlkenumber)
	return päring

def valikõiksõnad(tõlkenumber):
	päring = """SELECT id,lsõ,lgr,lkl FROM tõlkesõnad WHERE tnr='%s' ORDER BY tasn;""" % (tõlkenumber)
	return päring

def sõnadsõnanumbrikaupa(tõlkenumber):
	päring = """SELECT DISTINCT ON (tasn) id,lsõ,tasn FROM tõlkesõnad WHERE tnr ='%s' ORDER BY tasn;""" % tõlkenumber
	return päring

def nummerdasõnadlausetes(snr,tvsn,lausenr,osalausenr,pid,tasn):
	päring = """UPDATE tõlkesõnad SET tvsn='%s',snr='%s',lnr='%s',olnr='%s' WHERE tasn = '%s';""" % (tvsn,snr,lausenr,osalausenr,tasn)
	return päring

def tõlkelausessetõlgejuurde(tõlgitudtekst,tõlkenumber):
	päring = "UPDATE tõlked SET sihtjutt=trim('%s') WHERE nr='%s';" % (tõlgitudtekst,tõlkenumber)
	return päring

def tekstandmetesse(tõlkenumber,lähtekeel,sihtkeel,lähtejutt):
	päring = "INSERT INTO tõlked (nr,lke,ske,lähtejutt) VALUES ('%s','%s','%s','%s'); " % (tõlkenumber,lähtekeel,sihtkeel,lähtejutt)
	return päring

def tükeldatekst(tõlkenumber):
	päring = "SELECT lähtejutt FROM tõlked WHERE nr='%s'" % tõlkenumber
	return päring

def toge(tõlkenumber,sõnanr,sõna,lipp):
	päring = """INSERT INTO tõlkesõnad (tnr,tasn,lsõ,t) VALUES ('%s','%s','%s','%s');""" % (tõlkenumber,sõnanr, sõna, lipp)
	return päring

def uustõlkenumber():
	return "SELECT coalesce(max(nr),0) FROM tõlked;"

def küsiliidetearvu(pid):
	return "SELECT max(countinstring(llõd,'\+')) FROM tõlkevormikud WHERE tsid = '%s' GROUP BY tsid;""" % (pid)
def võrdlesõna_etvro(sõna):
	päring = """
WITH
nulla AS (
	SELECT
		'%s'::TEXT as lähtesõna),
essa AS (
	SELECT
		DISTINCT ON (vro) vro AS vro0
		, CASE
			WHEN et=vro THEN NULL
			ELSE vro
		END
		AS tõlge
		, te
		, liik
		, '1'::INT AS hinne
	FROM
		dikt4_vro_et d,
		nulla n
	WHERE
		et=lähtesõna
	AND
		vro IS NOT NULL
	AND
		te = 'wi'
	),
tessa AS (
	SELECT
		DISTINCT ON (vro) vro AS vro0
		, CASE
			WHEN et=vro THEN NULL
			ELSE vro
		END
		AS tõlge
		, te
		, liik
		, '2'::INT AS hinne
	FROM
		dikt4_vro_et d,
		nulla n
	WHERE
		et=lähtesõna
	AND
		vro IS NOT NULL
	AND
		te IS NULL
	),
kossa AS (
	SELECT
		*
	FROM
		tessa
	UNION
	SELECT
		*
	FROM
		essa
	),
ph AS (
	SELECT min(hinne) AS pisim FROM kossa
	),
m AS (
	SELECT * from kossa, ph WHERE hinne = pisim
	)
SELECT
	vro0
	, liik
FROM
	m
WHERE EXISTS (
	SELECT
		tõlge
		, liik
	FROM
		m);
""" % (sõna)
	return päring
def võrdlesõna_vroet(sõna):
	päring = """WITH
nulla AS (
	SELECT
		'%s'::TEXT as lähtesõna),
essa AS (
	SELECT
		et,
		vro_grammar,
		et_grammar
	FROM
		dikt4_vro_et d,
		nulla n
	WHERE
		vro=lähtesõna)
SELECT
	et,
	vro_grammar,
	et_grammar
FROM
	essa
WHERE
	et IS NOT NULL;
""" % (sõna)
	return päring
def erindid_etvro(sõna):
	päring = """
WITH nulla AS (
	SELECT
		'%s'::TEXT AS lähtesõna),
essa AS (
	SELECT *
	FROM nulla n, et_ms e
	WHERE
		gr = lähtesõna
		AND ni!='sn'
	ORDER BY ni,vä
	),
tessa AS (
	SELECT di,gr,string_agg(ni,',') AS nii,string_agg(vä,',') AS vää
	FROM essa
	GROUP BY di,gr
	),
kossa AS (
	SELECT DISTINCT
		t.di,t.gr,t.nii,t.vää /* t */
		, d.vro  /* d */
		, v.di AS vdi, v.gr AS vgr
		, v.ni AS vni
		, v.vä AS vvä
	FROM tessa t
	LEFT JOIN dikt4_vro_et d
		ON (t.di=d.et)
	LEFT JOIN vro_b_ms v
		ON (d.vro=v.di)
	ORDER BY vro,vdi,vgr,vni,vvä
	),
nessa AS (
	SELECT
	di,gr,nii,vää /* t */
	, vro
	, vdi, vgr
	, string_agg(vni,',') AS vni
	, string_agg(vvä,',') AS vvä
	FROM kossa
	GROUP BY di,gr,nii,vää,vro,vdi,vgr
	)
SELECT vgr
	,vni||';'||vvä AS et_grammar
	,vni||';'||vvä AS vro_grammar
	FROM nessa
	WHERE nii=vni
		AND vää=vvä;
""" % (sõna)
	return päring
def erindid_vroet(sõna):
	päring = """
with nulla as (select '%s'::TEXT as lähtesõna),
essa as ( select et,vro_grammar,et_grammar from dikt4_vro_et d, nulla n where vro=lähtesõna),
tessa AS (
SELECT lähtesõna,
	e.disõna AS edisõna,e.grammar,
	v.disõna,
	d.et,
	v2.grsõna
	FROM nulla n
	LEFT JOIN vro_sõnagrammar e ON (n.lähtesõna=e.grsõna)
	LEFT JOIN et_sõnagrammar v ON (e.grammar=v.grammar)
	LEFT JOIN dikt4_vro_et d ON (e.disõna=d.vro)
	LEFT JOIN et_sõnagrammar v2 ON (d.et=v2.disõna)
),
kossa as (
	select et,vro_grammar,et_grammar from essa
	UNION
	SELECT grsõna AS et, grammar AS vro_grammar,grammar AS et_grammar FROM tessa
)
select * from kossa WHERE et IS NOT NULL;
""" % (sõna)
	return päring
def leialõpuliited_et(pid,sõna):
	päring = """
WITH
	lõpukesed AS (
	SELECT
		*
	FROM
		lõpukõsõq_et('%s')
	),
algus AS (
	SELECT
		'%s'::INT AS pid
	),
tooreqlõpuq AS (
	SELECT
		süg
		, l
		, i
		, sõna
		, tüvi
		, uuslõpp
		, lõpud
		, lid
		, k
	FROM
		lõpukesed
	),
ttõ_d AS (
	SELECT
		'dict'::TEXT AS dikt
		, tüvi
		, sõna
		, süg
		, lõpud
		, lid
		, d.vro
		, d.liik
		, k
	FROM
		tooreqlõpuq e
	LEFT JOIN
		dikt4_vro_et d
	ON
		(e.tüvi=d.et)
	WHERE
		d.vro IS NOT NULL
	AND
		d.te = 'wi'
	UNION
	SELECT
		'dict-vok'::TEXT AS dikt
		, CASE WHEN
			RIGHT(e.tüvi,1) =  ANY(ARRAY['a','e','i','o','u','õ','ä','ö','ü','y'])
			THEN LEFT(e.tüvi,-1)
			END AS tüvi
		, sõna
		, süg
		, lõpud
		, lid
		, d.vro
		, d.liik
		, k
	FROM
		tooreqlõpuq e
	LEFT JOIN
		dikt4_vro_et d
	ON
		d.et=CASE WHEN
			RIGHT(e.tüvi,1) =  ANY(ARRAY['a','e','i','o','u','õ','ä','ö','ü','y'])
			THEN LEFT(e.tüvi,-1)
			END
	WHERE
		d.vro IS NOT NULL
	AND
		d.te = 'wi'
	UNION
	SELECT
		'dict+ma'::TEXT AS dikt
		, tüvi
		, sõna
		, süg
		, lõpud
		, lid
		, d.vro
		, d.liik
		, k
	FROM
		tooreqlõpuq e
	LEFT JOIN
		dikt4_vro_et d
	ON
		(e.tüvi||'ma'=d.et)
	WHERE
		d.vro IS NOT NULL
	AND
		d.te = 'wi'
	UNION
	SELECT
		'dict-vok+ma'::TEXT AS dikt
		, CASE WHEN
			RIGHT(e.tüvi,1) =  ANY(ARRAY['a','e','i','o','u','õ','ä','ö','ü','y'])
			THEN LEFT(e.tüvi,-1)
			END AS tüvi
		, sõna
		, süg
		, lõpud
		, lid
		, d.vro
		, d.liik
		, k
	FROM
		tooreqlõpuq e
	LEFT JOIN
		dikt4_vro_et d
	ON
		(CASE
			WHEN
				RIGHT(e.tüvi,1) =  ANY(ARRAY['a','e','i','o','u','õ','ä','ö','ü','y'])
			THEN
				LEFT(e.tüvi,-1) ||'ma'=d.et
			ELSE
				e.tüvi||'ma'=d.et
			END
		)
	WHERE
		d.vro IS NOT NULL
	AND
		d.te = 'wi'
	),
ttõ_etms AS (
	SELECT
		'et_ms'::TEXT AS dikt
		, e.i AS ei
		, tüvi
		, k
		, sõnapuhtaks(e.gr) AS gr
		, sõnapuhtaks(e.di) AS di
		, t.sõna
		, t.lõpud
		, d.liik
		, lid
	FROM
		tooreqlõpuq t
	LEFT JOIN
		et_ms e
	ON
		(t.tüvi=sõnapuhtaks(e.gr))
	LEFT JOIN
		dikt4_vro_et d
	ON
		(sõnapuhtaks(e.di)=d.et)
	UNION
	SELECT
		'et_ms+ma'::TEXT AS dikt
		, e.i AS ei
		, tüvi
		, k
		, sõnapuhtaks(e.gr) AS gr
		, sõnapuhtaks(e.di) AS di
		, t.sõna
		, t.lõpud
		, d.liik
		, lid
	FROM
		tooreqlõpuq t
	LEFT JOIN
		et_ms e
	ON
		(t.tüvi||'ma'=(sõnapuhtaks(e.gr)))
	LEFT JOIN
		dikt4_vro_et d
	ON
		(sõnapuhtaks(e.di)=d.et)
	UNION
	SELECT
		'et_ms+gr-n'::TEXT AS dikt
		, e.i AS ei
		, tüvi
		, k
		, regexp_replace(sõnapuhtaks(e.gr),t.lõpud,'') AS gr
		, regexp_replace(sõnapuhtaks(e.di),t.lõpud,'') AS di
		, t.sõna
		, t.lõpud
		, d.liik
		, lid
	FROM
		tooreqlõpuq t
	LEFT JOIN
		et_ms e
	ON
		(
			(t.tüvi||'n'=(sõnapuhtaks(e.gr)) )
			OR
			(t.tüvi||'b'=(sõnapuhtaks(e.gr)) )
		)
	LEFT JOIN
		dikt4_vro_et d
	ON
		(sõnapuhtaks(e.di)=d.et)
	),
etms_vro AS (
	SELECT dikt,ei,tüvi,k,di,vro,gr,di,sõna,lõpud,liik,lid
	FROM (SELECT dikt,ei,tüvi,k,gr,di,sõna,lõpud,liik,lid FROM ttõ_etms t WHERE di IS NOT NULL ) o1
	LEFT JOIN LATERAL ( SELECT vro FROM et_vro_sõnnavaitüvvelöüdminõ(tüvi,liik)
	) o2 ON TRUE
	),
koos AS (
	SELECT
		pid
		, sõna
		, tüvi
		, vro
		, lõpud
		, liik
		, dikt
		, CASE
			WHEN dikt='dict' THEN 'n'
			WHEN dikt='dict+ma' THEN 'v'
			WHEN dikt='dict-vok+ma' THEN 'v'
			END AS grammar
		,'liited:'||lid||';' AS ltkl
		,'leialõpuliited_et:'||dikt||';' AS rut
		, lid
	FROM
		ttõ_d
		, algus
	WHERE
		vro IS NOT NULL
	UNION
	SELECT
		pid
		, sõna
		, tüvi
		, vro
		, lõpud
		, liik
		, dikt
		, CASE
			WHEN dikt='et_ms' THEN 'n'
			WHEN dikt='et_ms+ma' THEN 'v'
			WHEN dikt='et_ms+gr-n' THEN 'v+1.p'
			END AS grammar
		,'liited:'||lid||';' AS ltkl
		,'leialõpuliited_et:'||dikt||';' AS rut
		, lid
	FROM
		etms_vro
		, algus
	WHERE
		vro IS NOT NULL
	)

INSERT INTO
	tõlkevormikud (
		tsid
		, lsõ
		, ltü
		, stü
		, llõd
		, llõgr
		, ltkl
		, rut)
	(
	SELECT
		pid
		, sõna
		, tüvi
		, vro
		, lõpud
		, grammar
		, 'liited:'||lid||';'
		, 'leialõpuliited_et:'||dikt||';'
        FROM
		koos
	);
""" % ( sõna,pid)
	return päring
def leialõpuliited_vro(pid,sõna):
	päring = """
WITH RECURSIVE lõpukesed AS (
    SELECT 1 AS süg,
	'%s'::TEXT AS sõna,
	LEFT('%s'::TEXT,-LENGTH(lõpp)) AS tüvi,
	lõpp::TEXT,
	RIGHT('%s'::TEXT,LENGTH(lõpp)) AS uuslõpp,
	grammar,klass,
	grammar AS täisgrammar,
	lõpp::TEXT AS lõpud,
	klass AS täisklass
    FROM vro_lõpud
    WHERE RIGHT('%s'::TEXT,LENGTH(lõpp))=lõpp
	AND grammar!='kindla kõneviisi oleviku aktiivi ainsuse 1. pööre'
UNION ALL
    SELECT b.süg+1,
	b.tüvi AS sõna,
	LEFT(b.tüvi,-LENGTH(a.lõpp)) AS tüvi,
	RIGHT(b.tüvi,LENGTH(a.lõpp)) AS lõpp,
	RIGHT(b.tüvi,LENGTH(a.lõpp)) AS uuslõpp,
	a.grammar,a.klass,
	b.täisgrammar||';'||a.grammar AS täisgrammar,
	RIGHT(b.tüvi,LENGTH(a.lõpp))||'+'||b.lõpud AS lõpud,
	b.täisklass||';'||a.klass AS täisklass
	FROM vro_lõpud a
	JOIN lõpukesed b
	ON (a.lõpp=right(b.tüvi,length(a.lõpp) ) ) AND a.grammar!='kindla kõneviisi oleviku aktiivi ainsuse 1. pööre'
    ),
essa AS (SELECT '%s'::INT AS pid),
testitüvesid AS (
	SELECT sõna,tüvi,et
	FROM lõpukesed
	LEFT JOIN dikt4_vro_et d ON (tüvi=vro)
	WHERE et IS NOT NULL
UNION
	SELECT sõna,tüvi,vro
	FROM lõpukesed
	LEFT JOIN dikt4_vro_et d ON (tüvi||'ma'=vro)
	WHERE et IS NOT NULL
),
ühekordselt_tüved AS (
	SELECT DISTINCT tüvi FROM testitüvesid
),
vastetega_tüved AS (
        SELECT sõna,ü.tüvi,lõpp,grammar,täisgrammar,klass,täisklass,lõpud,'leialõpuliited_vro'::TEXT as rut
        FROM ühekordselt_tüved ü LEFT JOIN lõpukesed l ON (ü.tüvi=l.tüvi)
),
tessa AS (INSERT INTO tõlkevormikud (tsid,lsõ,ltü,llõ,lkl,ltkl,llõd,rut)
        (SELECT pid,sõna,tüvi,lõpp,klass,täisklass,lõpud,'leialõpuliited_vro'::TEXT as rut
        FROM vastetega_tüved, essa) )
SELECT *,row_number() over() as rnr FROM vastetega_tüved;

""" % ( sõna,sõna,sõna,
	sõna,
	pid)
	return päring
def genereerisõna_etvro(pid):
	päring = """
WITH
algus AS (
	SELECT
		'%s'::INT AS tid),
read AS (
	SELECT
		tid,
		tvid,
		ts.lsõ,
		ts.lgr,
		ts.rut AS tsrut,

		tv.ltü,
		tv.stü,
		tv.ssõ,
		tv.llõ,
		tv.lkl,
		tv.ltkl,
		tv.llõd,
		tv.rut AS tvrut
	FROM
		algus a
	LEFT JOIN
		tõlkesõnad ts
	ON
		(a.tid=ts.id)
	LEFT JOIN
		tõlkevormikud tv
	ON	(ts.id=tv.tsid)
	WHERE
		ts.ssõ IS NULL
),
ajutine AS (
	SELECT
		tid,
		tvid,
		lsõ,
		stü,
		llõd,  
		stü||võrolõpud(tid) AS ssõ,
		võrolõpud(tid) AS slõd
		, tsrut
		, tvrut
	FROM read
)
UPDATE tõlkevormikud
	SET
		ssõ=a.ssõ
		, slõd=a.slõd
		, rut=CASE WHEN tvrut IS NULL THEN 'genereerisõna'
			ELSE tvrut||';'||'genereerisõna'
			END
	FROM
		ajutine a
	WHERE
		tid=a.tid
	AND
		tõlkevormikud.tvid=a.tvid
	AND 
		tõlkevormikud.ssõ IS NULL;
""" % (pid)
	return päring
def uuendatõlkesõna(sõna,grammar,pid,rut):
	päring = """
UPDATE
	tõlkesõnad
SET
	ssõ='%s'
	, lkl = '%s'
	, sknr='1'
	, rut=CASE
			WHEN rut IS NOT NULL THEN rut||';'||'%s'
			ELSE '%s'
		END
WHERE
	id='%s';
""" % (sõna,grammar,rut,rut,pid)
	return päring
def sisestatõlkesõnadesse(sõna,grammar,pid,rut):
	päring = """
WITH
essa  AS (
	SELECT
		'%s'::TEXT AS ssõ,
		'%s'::TEXT AS lkl,
		'%s'::TEXT AS rut,
		'%s'::INT AS pid),
tessa AS (
	SELECT
		id,
		tnr,
		tasn,
		snr,
		tvsn,
		lnr,
		olnr,
		t,
		lsõ
	FROM
		tõlkesõnad
	WHERE
		id='%s'),
kossa as (
	SELECT
		id,
		pid,
		tnr,
		tasn,
		snr,
		tvsn,
		lnr,
		olnr,
		t,
		(SELECT
			COALESCE(MAX(sknr)+1,1) AS makssknr
		FROM
			tõlkesõnad tõ, tessa t
		WHERE
			tõ.tasn=t.tasn
		AND tõ.tnr=t.tnr),
		lsõ,
		ssõ,
		lkl,
		rut
	FROM
		tessa t
	LEFT JOIN
		essa e
	ON
		(e.pid=t.id))
INSERT INTO
	tõlkesõnad
		(tnr,
		tasn,
		snr,
		tvsn,
		lnr,
		olnr,
		sknr,
		lsõ,
		ssõ,
		lkl,
		t,
		rut)
	(SELECT
		tnr,
		tasn,
		snr,
		tvsn,
		lnr,
		olnr,
		makssknr,
		lsõ,
		ssõ,
		lkl,
		t,
		rut
	FROM
		kossa);
""" % (sõna,grammar,rut,pid,pid)
	return päring
def vormikutestsõnadesse(tõlkenumber):
	päring = """
WITH
nulla AS (
	SELECT
		'%s'::INT AS tõlkenr
	),
sisse AS (
        SELECT
                n.tõlkenr
		, ts.id
		, ts.tasn
		, ts.snr
		, ts.tvsn
		, ts.lnr
		, ts.olnr
		, ts.sknr
		, ts.lsõ
		, ts.rut AS tsrut
		, ts.ssõ AS tsssõ

                , tv.ssõ
                , tv.tsid
		, tv.rut AS tvrut
		, row_number() over() AS nr
        FROM
                nulla n
		, tõlkesõnad ts
        LEFT JOIN
                tõlkevormikud tv
                ON
                (tv.tsid=ts.id)
        WHERE
                ts.tnr=n.tõlkenr
	AND
		ts.ssõ IS NULL
	AND
		tv.ssõ IS NOT NULL
	),
uuendada AS (
	UPDATE
		tõlkesõnad t
	SET
		ssõ=s.ssõ
		,sknr='1'
	FROM
		sisse s
	WHERE
		t.id=s.id
	RETURNING s.ssõ
	)
INSERT INTO
		tõlkesõnad (
			tnr
			, tasn
			, snr
			, tvsn
			, lnr
			, olnr
			, sknr
			, lsõ
			, rut
			, ssõ
			)
SELECT
	tõlkenr AS tnr
	, tasn
	, snr
	, tvsn
	, lnr
	, olnr
	, nr
	, lsõ
	, tsrut AS rut
	, ssõ
FROM
	sisse
WHERE
	ssõ NOT IN (
		SELECT
			ssõ
		FROM
			tõlkesõnad
	);
""" % (tõlkenumber)
	return päring
def ennetõlget(tõlkenumber):
	päring = """
WITH
nulla AS (
	SELECT
		'%s'::INT AS tõlkenr),
tõlkesõnadest AS (
	SELECT
		tnr,id,lsõ,ssõ,
		CASE
			WHEN ssõ IS NOT NULL
			THEN similarity(lsõ,ssõ)
			ELSE '0'
		END AS sarnasus,
		COALESCE(t.ssõ,t.lsõ) AS tõlge,
		tasn,lnr,snr,tvsn
	FROM
		tõlkesõnad t,
		nulla n
	WHERE
		n.tõlkenr=t.tnr
	ORDER BY
		tasn),
essa0 AS (
	SELECT
		*
	FROM
		tõlkesõnadest
	WHERE
		sarnasus !='1'),
essa1 AS (
	SELECT
		max(sarnasus) AS makssarn,tasn
	FROM
		essa0
	GROUP BY
		tasn
	ORDER BY
		tasn),
essa2 AS (
	SELECT DISTINCT
		ON (e1.tasn) id,
		e1.tasn,
		tnr,
		makssarn,
		sarnasus,
		ssõ AS tõlge
	FROM
		essa1 e1
	LEFT JOIN
		tõlkesõnadest e0
		ON
			(e1.tasn=e0.tasn
			AND makssarn=sarnasus) ),
tõlkevormikutest AS (
	SELECT
		tnr,id,te.lsõ,te.ssõ,
		COALESCE(tõ.ssõ,te.tõlge) AS tõlge,
		tasn,lnr,snr,tvsn,
		tõ.ssõ as tõssõ
	FROM
		tõlkesõnadest te
	LEFT JOIN
		tõlkevormikud tõ
		ON te.id=tõ.tsid
	WHERE
		tõ.ssõ IS NOT NULL),
teise2 AS (
	SELECT
		lsõ,tõlge,
		similarity(lsõ,tõlge) AS sarnasus,
		tasn
	FROM
		tõlkevormikutest ),
tessa2b AS (
	SELECT
		*
	FROM
		teise2
	WHERE
		sarnasus !='1'),
teise3 AS (
	SELECT
		max(sarnasus) AS makssarn,
		tasn
	FROM
		tessa2b
	GROUP BY
		tasn),
teise4 AS (
	SELECT
		makssarn,sarnasus,t3.tasn,tõlge
	FROM
		teise3 t3
	LEFT JOIN
		teise2 t2
		ON (t2.tasn=t3.tasn
		AND makssarn=sarnasus)),
valikvormikutest AS (
	SELECT
		DISTINCT ON (e.tasn) e.tasn,
		e.lsõ,t4.tõlge
	FROM
		tõlkesõnadest e
	LEFT JOIN
		teise4 t4
		ON (e.tasn=t4.tasn) )
UPDATE
	tõlkesõnad tõ
SET
	ssõ=tõlge
	, rut=CASE WHEN rut IS NULL THEN 'ennetõlget'
		ELSE rut||';'||'ennetõlget'
		END
FROM
	valikvormikutest v,
	nulla n
WHERE
	(v.tõlge IS NOT NULL
	AND tõ.ssõ IS NULL)
	AND  v.tasn=tõ.tasn
	AND tõlkenr=tnr;
""" % (tõlkenumber)
	return päring
def tõlgilõpuliited_etvro(pid):
	päring = """
WITH nulla AS (
	SELECT
		'%s'::INT AS pid
	),
tänane AS (
	select
		snr
		, tvid AS vid
		, liited as l
		, stü
		, stü||liited AS tesõna
		, llõgr
		, k
		FROM (
			SELECT
				tsid as snr
				, tvid
				, stü
				, llõgr
			FROM
				nulla n
				, tõlkevormikud t
			WHERE
				tsid = pid
			ORDER BY
				aeg DESC
			) o1
		LEFT JOIN LATERAL (
			SELECT
				nr
				, liited
				, k
			FROM
				etvroliiteq(snr)
			) o2
			ON TRUE
	)
UPDATE
	tõlkevormikud
SET
	slõd=l
	, ssõ = tesõna
	,rut=CASE
		WHEN rut IS NULL
		THEN 'liited+'::TEXT
		ELSE rut||';'||'liited+'::TEXT
		END
	, llõgr = k
FROM
	tänane
WHERE
	tvid=vid;
""" % (pid)
	return päring
def valiparalleeltõlge(tõlkenumber):
	päring = """
WITH
nulla AS (
	SELECT
		'%s'::INT AS tõlkenr),
tõlkesõnadest AS (
	SELECT
		ts.tnr
		, ts.tasn
		, ts.tvsn
		, ts.snr
		, ts.id
		, ts.lsõ AS ts_lsõ
		, ts.ssõ AS ts_ssõ
		, tv.lsõ AS tv_lsõ
		, tv.ssõ AS tv_ssõ
	FROM
		nulla n,
		tõlkesõnad ts
	LEFT JOIN
		tõlkevormikud tv
	ON
		(tv.tsid=ts.id)
	WHERE
		n.tõlkenr=ts.tnr
	ORDER BY
		tasn),
kokku AS (
	SELECT
		tnr
		, tasn
		, tvsn
		, ts.snr
		, ts.id AS tid
		, ts_lsõ
		, CASE
			WHEN ts_ssõ IS NOT NULL THEN
				CASE
					WHEN  LEFT(ts_lsõ,1)=nõstaqedetäht(LEFT(ts_lsõ,1)) THEN nõstaqedetäht(ts_ssõ)
					ELSE ts_ssõ
					END
			WHEN tv_ssõ IS NOT NULL THEN
				CASE
					WHEN  LEFT(ts_lsõ,1)=nõstaqedetäht(LEFT(ts_lsõ,1)) THEN nõstaqedetäht(tv_ssõ)
					ELSE tv_ssõ
					END
			ELSE
				ts_lsõ
		END AS tõlkesõna

	FROM
		tõlkesõnadest AS ts
	),
lõpliktõlge AS (
	SELECT
		DISTINCT ON (tasn)
		tnr
		, tasn
		, snr
		, tvsn
		, snr
		,CASE
			WHEN (snr='1' AND left(tõlkesõna,1)=upper(left(tõlkesõna,1)))
			THEN nõstaqedetäht(tõlkesõna)
			ELSE tõlkesõna
		END AS tõlge
	FROM
		kokku
	ORDER BY tasn)
SELECT
	*
FROM
	lõpliktõlge;
""" % (tõlkenumber)
	return päring
def uuendalõpuliiteid(l,vid,vrosõna,kust):
	päring = """
UPDATE
	tõlkevormikud
SET
	slõd  = '%s'
	, ssõ = '%s'
        , rut = CASE
                WHEN rut IS NULL
                THEN 'lõpuliited+'::TEXT||'%s'
                ELSE rut||';'||'lõpuliited+'::TEXT||'%s'
                END

WHERE
	tvid='%s';
""" % (l,vrosõna,kust,kust,vid)
	return päring
def tüvekontra(pid):
	päring = """
WITH algus AS
	(
	SELECT '%s'::INT AS pid
	),
essa AS
	(
	SELECT
		ltü
		, stü
		, llõgr
		, slõd
	FROM
		tõlkevormikud
		, algus
	WHERE
		tsid = pid
	),
tessa AS (
	SELECT
		DISTINCT
		e.*
		, v.*
	FROM
		essa e
		
	LEFT JOIN
		vro_b_ms v
	ON
		(
			e.ltü = v.e
		AND
			e.stü = v.di
		AND
			v.vä = 'om'
		)
	WHERE
		llõgr = 'n'
	),
kossa AS (
	SELECT
		di
		, gr
		, pid
	FROM
		tessa
		, algus
	WHERE
		gr IS NOT NULL
	)
UPDATE
	tõlkevormikud t
SET
	stü=gr
FROM
	kossa k
WHERE
	t.tsid = k.pid
AND
	stü=di;
""" % (pid)
	return päring
