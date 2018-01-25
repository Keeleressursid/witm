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
