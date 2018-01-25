WITH RECURSIVE lõpukesed AS (
    SELECT 1 AS süg,
	'%s'::TEXT AS sõna,
	LEFT('%s'::TEXT,-LENGTH(lõpp)) AS tüvi,
	lõpp::TEXT,
	RIGHT('%s'::TEXT,LENGTH(lõpp)) AS uuslõpp,
	grammar,klass,
	grammar AS täisgrammar,
	lõpp::TEXT AS lõpud,
	klass AS täisklass
    FROM vro_lõpud
    WHERE RIGHT('%s'::TEXT,LENGTH(lõpp))=lõpp
	AND grammar!='kindla kõneviisi oleviku aktiivi ainsuse 1. pööre'
UNION ALL
    SELECT b.süg+1,
	b.tüvi AS sõna,
	LEFT(b.tüvi,-LENGTH(a.lõpp)) AS tüvi,
	RIGHT(b.tüvi,LENGTH(a.lõpp)) AS lõpp,
	RIGHT(b.tüvi,LENGTH(a.lõpp)) AS uuslõpp,
	a.grammar,a.klass,
	b.täisgrammar||';'||a.grammar AS täisgrammar,
	RIGHT(b.tüvi,LENGTH(a.lõpp))||'+'||b.lõpud AS lõpud,
	b.täisklass||';'||a.klass AS täisklass
	FROM vro_lõpud a
	JOIN lõpukesed b
	ON (a.lõpp=right(b.tüvi,length(a.lõpp) ) ) AND a.grammar!='kindla kõneviisi oleviku aktiivi ainsuse 1. pööre'
    ),
essa AS (SELECT '%s'::INT AS pid),
testitüvesid AS (
	SELECT sõna,tüvi,et
	FROM lõpukesed
	LEFT JOIN dikt4_vro_et d ON (tüvi=vro)
	WHERE et IS NOT NULL
UNION
	SELECT sõna,tüvi,vro
	FROM lõpukesed
	LEFT JOIN dikt4_vro_et d ON (tüvi||'ma'=vro)
	WHERE et IS NOT NULL
),
ühekordselt_tüved AS (
	SELECT DISTINCT tüvi FROM testitüvesid
),
vastetega_tüved AS (
        SELECT sõna,ü.tüvi,lõpp,grammar,täisgrammar,klass,täisklass,lõpud,'leialõpuliited_vro'::TEXT as rut
        FROM ühekordselt_tüved ü LEFT JOIN lõpukesed l ON (ü.tüvi=l.tüvi)
),
tessa AS (INSERT INTO tõlkevormikud (tsid,lsõ,ltü,llõ,lkl,ltkl,llõd,rut)
        (SELECT pid,sõna,tüvi,lõpp,klass,täisklass,lõpud,'leialõpuliited_vro'::TEXT as rut
        FROM vastetega_tüved, essa) )
SELECT *,row_number() over() as rnr FROM vastetega_tüved;

