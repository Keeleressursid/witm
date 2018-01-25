WITH
nulla AS (
	SELECT
		'%s'::INT AS pid
	),
andmed AS (
	SELECT
		ts.id
		, tv.tvid
		, tv.stü
		, tv.ltkl
		, tv.llõd
	FROM
		nulla a
	LEFT JOIN
		tõlkesõnad ts
	ON
		(a.pid=ts.id)
	LEFT JOIN
		tõlkevormikud tv
	ON
		(ts.id=tv.tsid)
	),
algus AS (
	SELECT DISTINCT
		ltkl,llõd
	FROM
		andmed
	),
koolonid_eraldi AS (
	SELECT
		*,regexp_split_to_table(ltkl,';') AS eraldi_ritta
	FROM
		algus
	),
gr_sisu_eraldi AS (
	SELECT
		*,split_part(eraldi_ritta,':','2') as ll
	FROM
		koolonid_eraldi
	WHERE
		length(eraldi_ritta) > '0'
	),
liite_idid_eraldi AS (
	SELECT
		*
		,regexp_split_to_table(ll,'\+') AS liiteidid
	FROM
		gr_sisu_eraldi),
lidi_nr AS (
	SELECT
		l.*
		, NULLIF(liiteidid, '')::INT as liitenr
		, ROW_NUMBER() OVER() AS reanr
	FROM
		liite_idid_eraldi l),
l_kiri AS (
	SELECT
		l.*
		,countinstring(llõd,'+') as k
		, kiri
		, ni
		, vä
	FROM
		lidi_nr l
	LEFT JOIN
		et_gr_liited e
	ON
		(e.i=l.liitenr)
	LEFT JOIN
		et_gr_lii_om o
	ON
		(e.i = o.lid)
	),
sõna_prose AS (
	SELECT
		reanr
		, ni
		, CASE
			WHEN ni = 'kää' THEN 'N'::TEXT
			WHEN ni = 'sn' AND vä = 'v' THEN 'V'::TEXT
			ELSE NULL
		END AS sõnavorm
	FROM
		l_kiri
	WHERE
		ni = 'kää' OR (ni = 'v' AND vä = 'v' )
	),
min_arv AS (
	SELECT
		min(k) as k
	FROM
		l_kiri),
valik AS (
	SELECT
		ltkl,llõd,ll,liitenr,l.reanr,kiri,l.ni,l.vä,sõnavorm
	FROM
		min_arv m
	LEFT JOIN
		l_kiri l
	ON
		(m.k=l.k)
	LEFT JOIN
		sõna_prose sp
	ON
		(l.reanr = sp.reanr)
	WHERE sõnavorm IS NOT NULL
	),
vro_kiri AS (
	SELECT
		DISTINCT ON (l,vli)
		va.ltkl,llõd,liitenr
		, ll
		, reanr
		,length(llõd) as lpikk
		, vl.l
		, vl.i AS vli
		, va.kiri AS etkiri
		, vl.kiri AS vrokiri
		, sõnavorm
	FROM
		valik va
	LEFT JOIN
		vro_gr_liited vl
	ON
		(va.kiri=vl.kiri)
	),
maks_pikkus AS (
	SELECT
		max(lpikk) AS makspikkus
	FROM
		vro_kiri
	),
IIvalik AS (
	SELECT
		DISTINCT
		ltkl,llõd,liitenr,reanr,etkiri,vrokiri,l,ll,vli,sõnavorm
	FROM
		vro_kiri
		, maks_pikkus
	WHERE
		lpikk=makspikkus
	AND
		liitenr IS NOT NULL
	AND
		vli IS NOT NULL
	),
nimed AS (
	SELECT
		II.ltkl
		, II. llõd
		, liitenr
		, reanr
		, vrokiri
		, l

		, a.id
		, tvid AS vid
		, stü
		,CASE
			WHEN RIGHT(gr,2) = 'ma'
				OR
			RIGHT(gr,2) = 'mä' THEN 'v'::TEXT
			ELSE 'n'::TEXT
		END AS lõpukontroll
		,CASE
			WHEN RIGHT(gr,2) = 'ma'
				OR
			RIGHT(gr,2) = 'mä' THEN LEFT(gr,-2)||l::TEXT
			ELSE gr||l
		END AS vrosõna
		, v.gr AS vgr
	FROM
		IIvalik II
	LEFT JOIN
		andmed a
	ON
		(II.ltkl=a.ltkl AND II.llõd=a.llõd)
	LEFT JOIN
		vro_b_ms v
	ON
		(a.stü=v.di)
	WHERE
		v.ni='kää' AND v.vä='om' AND v.di=a.stü
	),
teod AS (
	SELECT
		II.ltkl
		, II. llõd
		, liitenr
		, reanr
		, vrokiri
		, l

		, a.id
		, tvid AS vid
		, stü
		,CASE
			WHEN RIGHT(gr,2) = 'ma'
				OR
			RIGHT(gr,2) = 'mä' THEN 'v'::TEXT
			ELSE 'n'::TEXT
		END AS lõpukontroll
		,CASE
			WHEN RIGHT(gr,2) = 'ma'
				OR
			RIGHT(gr,2) = 'mä' THEN LEFT(gr,-2)||l::TEXT
			ELSE gr||l
		END AS vrosõna
		, v.gr AS vgr
	FROM
		IIvalik II
	LEFT JOIN
		andmed a
	ON
		(II.ltkl=a.ltkl AND II.llõd=a.llõd)
	LEFT JOIN
		vro_b_ms v
	ON
		(a.stü=v.di)
	WHERE
		v.ni='is' AND v.vä='1' AND v.di=a.stü
	),
lõplik_tõlge AS (
SELECT
	vid
	, llõd
	, vrokiri
	, vrosõna
	, vgr
	, l
	, 'nimed'::TEXT AS kust
FROM
	nimed
UNION
SELECT
	vid
	, llõd
	, vrokiri
	, vrosõna
	, vgr
	, l
	, 'teod'::TEXT AS kust
FROM
	teod
	)
UPDATE
	tõlkevormikud
SET
	slõd=l.l
	, ssõ=l.vrosõna
	,rut=CASE WHEN rut IS NULL THEN 'vroliited'::TEXT
		ELSE rut||';'||'vroliited'::TEXT
		END
FROM
	lõplik_tõlge l
	WHERE tvid=l.vid;
