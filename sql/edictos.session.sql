-- @block Edictos total
SELECT COUNT(*) AS cantidad_edictos
FROM edictos
WHERE estatus = 'A';
-- @block Edictos por año
SELECT
    EXTRACT(YEAR FROM fecha) AS anio,
    COUNT(*) AS cantidad_edictos
FROM edictos
WHERE estatus = 'A'
GROUP BY anio
ORDER BY anio DESC;
