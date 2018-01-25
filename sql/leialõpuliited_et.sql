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
