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
