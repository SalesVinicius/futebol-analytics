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

),

tb_metricas_chute AS 
(
    SELECT 
        jogadorId,
        jogadorNome ||' ('|| codigoTime ||')' AS jogadorCodigoNome,
        jogadorPosição,
        nomeTime,
        COALESCE(SUM(CASE WHEN resultadoChute = "goal" THEN 1 END), 0) AS gols,
        count(*) AS totalChutes,
        COALESCE(SUM(CASE WHEN isHome = 1 THEN 1 ELSE 0 END), 0) AS totalChuteCasa,
        COALESCE(SUM(CASE WHEN isHome = 0 THEN 1 ELSE 0 END), 0) AS totalChuteVisitante,
        SUM(xG) AS somaXG,
        COALESCE(SUM(CASE WHEN isHome = 1 THEN xG END), 0) AS somaXGCasa,
        COALESCE(SUM(CASE WHEN isHome = 0 THEN xG END), 0) AS somaXGVisitante,
        1.0 * (SUM(xG)/count(*)) as avgXG,
        COALESCE(AVG(CASE WHEN resultadoChute = "miss" THEN xG END), 0) AS avgXGMiss

        
    FROM tb_base

    GROUP BY 1

)

SELECT * FROM tb_metricas_chute