CREATE DATABASE IF NOT EXISTS example_db;

CREATE TABLE IF NOT EXISTS example_db.FlujoAgua (
    ID_esp Int32,
    Time_stam DateTime,
    Flujo_de_agua Float32,
    Cantidad_agua Float32
) ENGINE = MergeTree()
ORDER BY ID_esp;

CREATE TABLE IF NOT EXISTS example_db.EstadoValvula (
    ID_esp Int32,
    Estado_valvula String
) ENGINE = MergeTree()
ORDER BY ID_esp;

CREATE TABLE IF NOT EXISTS example_db.ConsumoDiario (
    ID_esp Int32,
    Cantidad_diaria Float32,
    Tiempo_corriendo Float32
) ENGINE = MergeTree()
ORDER BY ID_esp;
