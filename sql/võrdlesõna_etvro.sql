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
