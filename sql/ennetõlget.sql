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
