with nulla as (select '%s'::TEXT as lähtesõna),
essa as ( select et,vro_grammar,et_grammar from dikt4_vro_et d, nulla n where vro=lähtesõna),
tessa AS (
SELECT lähtesõna,
	e.disõna AS edisõna,e.grammar,
	v.disõna,
	d.et,
	v2.grsõna
	FROM nulla n
	LEFT JOIN vro_sõnagrammar e ON (n.lähtesõna=e.grsõna)
	LEFT JOIN et_sõnagrammar v ON (e.grammar=v.grammar)
	LEFT JOIN dikt4_vro_et d ON (e.disõna=d.vro)
	LEFT JOIN et_sõnagrammar v2 ON (d.et=v2.disõna)
),
kossa as (
	select et,vro_grammar,et_grammar from essa
	UNION
	SELECT grsõna AS et, grammar AS vro_grammar,grammar AS et_grammar FROM tessa
)
select * from kossa WHERE et IS NOT NULL;
