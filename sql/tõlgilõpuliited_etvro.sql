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
