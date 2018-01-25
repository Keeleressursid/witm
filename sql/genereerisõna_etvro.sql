WITH
algus AS (
	SELECT
		'%s'::INT AS tid),
read AS (
	SELECT
		tid,
		tvid,
		ts.lsõ,
		ts.lgr,
		ts.rut AS tsrut,

		tv.ltü,
		tv.stü,
		tv.ssõ,
		tv.llõ,
		tv.lkl,
		tv.ltkl,
		tv.llõd,
		tv.rut AS tvrut
	FROM
		algus a
	LEFT JOIN
		tõlkesõnad ts
	ON
		(a.tid=ts.id)
	LEFT JOIN
		tõlkevormikud tv
	ON	(ts.id=tv.tsid)
	WHERE
		ts.ssõ IS NULL
),
ajutine AS (
	SELECT
		tid,
		tvid,
		lsõ,
		stü,
		llõd,  
		stü||võrolõpud(tid) AS ssõ,
		võrolõpud(tid) AS slõd
		, tsrut
		, tvrut
	FROM read
)
UPDATE tõlkevormikud
	SET
		ssõ=a.ssõ
		, slõd=a.slõd
		, rut=CASE WHEN tvrut IS NULL THEN 'genereerisõna'
			ELSE tvrut||';'||'genereerisõna'
			END
	FROM
		ajutine a
	WHERE
		tid=a.tid
	AND
		tõlkevormikud.tvid=a.tvid
	AND 
		tõlkevormikud.ssõ IS NULL;
