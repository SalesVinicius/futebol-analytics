WITH tb_base AS (

SELECT
    t1.*,
    CASE 
        WHEN t1.isHome = 1 
            THEN t2.nomeTimeCasa 
        ELSE t2.nomeTimeVisitante 
    END as nomeTime,
    CASE 
        WHEN t1.isHome = 1 
            THEN t2.codigoTimeCasa
        ELSE t2.codigoTimeVisitante 
    END as codigoTime

from tb_shot as t1
LEFT JOIN tb_match as t2
ON t1.idPartida = t2.idPartida

)

SELECT * FROM tb_base