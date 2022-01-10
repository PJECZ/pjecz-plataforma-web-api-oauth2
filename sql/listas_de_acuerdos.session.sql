-- @block Listas de Acuerdos total
SELECT COUNT(*) AS cantidad_listas_de_acuerdos
FROM listas_de_acuerdos
WHERE estatus = 'A';
-- @block Listas de Acuerdos por año
SELECT
    EXTRACT(YEAR FROM fecha) AS anio,
    COUNT(*) AS cantidad_listas_de_acuerdos
FROM listas_de_acuerdos
WHERE estatus = 'A'
GROUP BY anio
ORDER BY anio DESC;
