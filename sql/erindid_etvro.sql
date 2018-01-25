WITH nulla AS (
	SELECT
		'%s'::TEXT AS lähtesõna),
essa AS (
	SELECT *
	FROM nulla n, et_ms e
	WHERE
		gr = lähtesõna
		AND ni!='sn'
	ORDER BY ni,vä
	),
tessa AS (
	SELECT di,gr,string_agg(ni,',') AS nii,string_agg(vä,',') AS vää
	FROM essa
	GROUP BY di,gr
	),
kossa AS (
	SELECT DISTINCT
		t.di,t.gr,t.nii,t.vää /* t */
		, d.vro  /* d */
		, v.di AS vdi, v.gr AS vgr
		, v.ni AS vni
		, v.vä AS vvä
	FROM tessa t
	LEFT JOIN dikt4_vro_et d
		ON (t.di=d.et)
	LEFT JOIN vro_b_ms v
		ON (d.vro=v.di)
	ORDER BY vro,vdi,vgr,vni,vvä
	),
nessa AS (
	SELECT
	di,gr,nii,vää /* t */
	, vro
	, vdi, vgr
	, string_agg(vni,',') AS vni
	, string_agg(vvä,',') AS vvä
	FROM kossa
	GROUP BY di,gr,nii,vää,vro,vdi,vgr
	)
SELECT vgr
	,vni||';'||vvä AS et_grammar
	,vni||';'||vvä AS vro_grammar
	FROM nessa
	WHERE nii=vni
		AND vää=vvä;
