-- @block V.P. de Sentencias total
SELECT COUNT(*) AS cantidad_sentencias
FROM sentencias
WHERE estatus = 'A';
-- @block V.P. de Sentencias por año
SELECT
    EXTRACT(YEAR FROM sentencia_fecha) AS anio,
    COUNT(*) AS cantidad_sentencias
FROM sentencias
WHERE estatus = 'A'
GROUP BY anio
ORDER BY anio DESC;
