CREATE DATABASE IF NOT EXISTS riego;

CREATE TABLE IF NOT EXISTS riego.FlujoAgua (
    ID_esp Int32,
    Time_stam DateTime,
    Cantidad_agua Float32
) ENGINE = MergeTree()
ORDER BY ID_esp;

CREATE TABLE IF NOT EXISTS riego.EstadoValvula (
    ID_esp Int32,
    Estado_valvula String
) ENGINE = MergeTree()
ORDER BY ID_esp;

/* CREATE TABLE IF NOT EXISTS riego.ConsumoDiario (
    ID_esp Int32,
    Cantidad_diaria Float32,
    Tiempo_corriendo Float32
) ENGINE = MergeTree()
ORDER BY ID_esp;
 */
CREATE TABLE IF NOT EXISTS riego.Umbral (
    ID_esp Int32,
    Umbral String,
    Contra String
) ENGINE = MergeTree()
ORDER BY ID_esp;
