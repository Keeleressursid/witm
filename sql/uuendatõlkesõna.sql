UPDATE
	tõlkesõnad
SET
	ssõ='%s'
	, lkl = '%s'
	, sknr='1'
	, rut=CASE
			WHEN rut IS NOT NULL THEN rut||';'||'%s'
			ELSE '%s'
		END
WHERE
	id='%s';
