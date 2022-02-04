-- @block Autoridades que pueden subir Listas de Acuerdos con mas de un dia de antiguedad
SELECT clave,
    descripcion_corta,
    limite_dias_listas_de_acuerdos
FROM autoridades
WHERE estatus = 'A'
    AND limite_dias_listas_de_acuerdos > 0
ORDER BY clave;
