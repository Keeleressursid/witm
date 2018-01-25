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
