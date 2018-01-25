UPDATE
	tõlkevormikud
SET
	slõd  = '%s'
	, ssõ = '%s'
        , rut = CASE
                WHEN rut IS NULL
                THEN 'lõpuliited+'::TEXT||'%s'
                ELSE rut||';'||'lõpuliited+'::TEXT||'%s'
                END

WHERE
	tvid='%s';
