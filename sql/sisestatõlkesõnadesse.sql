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
