WITH tb_base AS (

SELECT
    t1.*,
    CASE 
        WHEN t1.isHome = 1 
            THEN t2.nomeTimeCasa 
        ELSE t2.nomeTimeVisitante 
    END as nomeTime

from tb_shot as t1
LEFT JOIN tb_match as t2
ON t1.idPartida = t2.idPartida

)

-- SELECT DISTINCT resultadoChute = miss FROM tb_base
SELECT 
    jogadorId,
    jogadorNome,
    jogadorPosição,
    nomeTime,
    COALESCE(SUM(CASE WHEN resultadoChute = "goal" THEN 1 END), 0) AS gols,
    count(*) AS totalChutes,
    COALESCE(SUM(CASE WHEN isHome = 1 THEN 1 ELSE 0 END), 0) AS totalChuteCasa,
    COALESCE(SUM(CASE WHEN isHome = 0 THEN 1 ELSE 0 END), 0) AS totalChuteVisitante,
    SUM(xG) AS somaXG,
    COALESCE(SUM(CASE WHEN isHome = 1 THEN xG END), 0) AS somaXGCasa,
    COALESCE(SUM(CASE WHEN isHome = 0 THEN xG END), 0) AS somaXGVisitante,
    COALESCE(SUM(CASE WHEN resultadoChute = "miss" THEN xG END), 0) AS somaXGMiss,
    1.0 * (SUM(xG)/count(*)) as avgXG

    
FROM tb_base

GROUP BY 1

ORDER BY gols DESC

