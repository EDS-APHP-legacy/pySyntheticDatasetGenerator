-- *********************************************************************
-- Update Database Script
-- *********************************************************************
-- Change Log: output/generate_schema.yml
-- Ran at: 03/02/18 11:40
-- Against: null@offline:postgresql
-- Liquibase version: 3.5.3
-- *********************************************************************

-- Changeset output/generate_schema.yml::1::null
DROP TABLE IF EXISTS principal CASCADE;

DROP TABLE IF EXISTS secondary CASCADE;

DROP TABLE IF EXISTS ref CASCADE;

CREATE TABLE principal (id_principal INT NOT NULL, cd_principal VARCHAR, moment TIMESTAMP WITHOUT TIME ZONE, length REAL, CONSTRAINT PK_PRINCIPAL PRIMARY KEY (id_principal));

COMMENT ON TABLE principal IS 'This is the principal table';

COMMENT ON COLUMN principal.id_principal IS 'unique identifier';

COMMENT ON COLUMN principal.cd_principal IS 'this is a functional code';

COMMENT ON COLUMN principal.moment IS 'this is a timestamp';

COMMENT ON COLUMN principal.length IS 'this is a length';

CREATE TABLE secondary (id_secondary INT NOT NULL, id_principal INT, id_ref INT, value_text VARCHAR, CONSTRAINT PK_SECONDARY PRIMARY KEY (id_secondary));

COMMENT ON TABLE secondary IS 'this is a secondary table';

COMMENT ON COLUMN secondary.id_secondary IS 'unique identifier';

CREATE TABLE ref (id_ref INT NOT NULL, cd_ref VARCHAR, CONSTRAINT PK_REF PRIMARY KEY (id_ref));

COMMENT ON TABLE ref IS 'terminology table';

COMMENT ON COLUMN ref.id_ref IS 'unique identifier';

COPY principal FROM '/app/edsr/projets/EDSI/REA/pySyntheticDataGenerator/output/principal.csv' CSV DELIMITER ';';

COPY secondary FROM '/app/edsr/projets/EDSI/REA/pySyntheticDataGenerator/output/secondary.csv' CSV DELIMITER ';';

COPY ref FROM '/app/edsr/projets/EDSI/REA/pySyntheticDataGenerator/output/ref.csv' CSV DELIMITER ';';

ALTER TABLE secondary ADD CONSTRAINT fk_secondary_principal_id_principal FOREIGN KEY (id_principal) REFERENCES principal (id_principal);

ALTER TABLE secondary ADD CONSTRAINT fk_secondary_ref_id_ref FOREIGN KEY (id_ref) REFERENCES ref (id_ref);

