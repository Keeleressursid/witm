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
