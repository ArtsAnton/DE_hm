create external table country_codes_external (
    COUNTRY varchar(100),
    ISO3 varchar(3),
    PHONE varchar(8),
    CURRENCY varchar(3)
) as copy from '/tmp/input/system_of_records/country_codes/*.parquet' parquet;

CREATE TABLE code AS SELECT * FROM country_codes_external ORDER BY COUNTRY;


CREATE EXTERNAL TABLE countries_and_capitals_external(
    COUNTRY varchar(100),
    CAPITAL varchar(30),
    ISO2 VARCHAR(2)
) AS COPY FROM '/tmp/input/system_of_records/countries_and_capitals/*.parquet' PARQUET;

CREATE TABLE capital AS SELECT * FROM countries_and_capitals_external ORDER BY COUNTRY;


CREATE EXTERNAL TABLE population_external (
    COUNTRY VARCHAR(100),
    POPULATION VARBINARY,
    AREA VARBINARY,
    POP_DENSITY VARBINARY,
    COASTLINE VARBINARY
) AS COPY FROM '/tmp/input/system_of_records/population/*.parquet' PARQUET;

CREATE TABLE population AS SELECT * FROM population_external ORDER BY COUNTRY;


CREATE EXTERNAL TABLE wealth_and_health_external (
    COUNTRY VARCHAR(100),
    NET_MIGRATION VARBINARY,
    INFANT_MORTALITY VARBINARY,
    GDP VARBINARY,
    BIRTHRATE VARBINARY,
    DEATHRATE VARBINARY
) AS COPY FROM '/tmp/input/system_of_records/wealth_and_health/*.parquet' PARQUET;

CREATE TABLE wealth AS SELECT * FROM wealth_and_health_external ORDER BY COUNTRY;


CREATE EXTERNAL TABLE education_external (
    COUNTRY VARCHAR(100),
    LITERACY VARBINARY
) AS COPY FROM '/tmp/input/system_of_records/education/*.parquet' PARQUET;

CREATE TABLE education AS SELECT * FROM education_external ORDER BY COUNTRY;


CREATE EXTERNAL TABLE areas_of_activity_external (
    COUNTRY VARCHAR(100),
    AGRICULTURE VARBINARY,
    INDUSTRY VARBINARY,
    SERVICE VARBINARY
) AS COPY FROM '/tmp/input/system_of_records/areas_of_activity/*.parquet' PARQUET;

CREATE TABLE area AS SELECT * FROM areas_of_activity_external ORDER BY COUNTRY;


CREATE EXTERNAL TABLE land_external (
    COUNTRY VARCHAR(100),
    ARABLE VARBINARY,
    CROPS VARBINARY,
    OTHER VARBINARY,
    CLIMATE VARBINARY
) AS COPY FROM '/tmp/input/system_of_records/land/*.parquet' PARQUET;

CREATE TABLE land AS SELECT * FROM land_external ORDER BY COUNTRY;


CREATE EXTERNAL TABLE location_external (
    COUNTRY VARCHAR(100),
    CONTINENT  VARCHAR(12),
    REGION  VARCHAR(30)
) AS COPY FROM '/tmp/input/system_of_records/location/*.parquet' PARQUET;

CREATE TABLE location AS SELECT * FROM location_external ORDER BY COUNTRY;


CREATE EXTERNAL TABLE world_cities_external (
    Country VARCHAR(3),
    City VARCHAR(30),
    Region VARCHAR(20),
    Population DOUBLE PRECISION,
    Latitude DOUBLE PRECISION,
    Longitude DOUBLE PRECISION
) AS COPY FROM '/tmp/input/system_of_records/world_cities/*.parquet' PARQUET;

CREATE TABLE city AS SELECT * FROM world_cities_external ORDER BY Country;


CREATE EXTERNAL TABLE laureate_table_external (
    COUNTRY VARCHAR(100),
    YEAR VARBINARY,
    CATEGORY VARCHAR(20),
    FULL_NAME VARCHAR(100)
) AS COPY FROM '/tmp/input/system_of_records/laureate_table/*.parquet' PARQUET;

CREATE TABLE laureate AS SELECT * FROM laureate_table_external ORDER BY COUNTRY;


CREATE EXTERNAL TABLE laureate_pers_inf_external(
    BIRTH_COUNTRY VARCHAR(100),
    BIRTH_CITY VARCHAR(50),
    BIRTH_DATE VARBINARY,
    ORGANIZATION_COUNTRY VARCHAR(100),
    ORGANIZATION_CITY VARCHAR(100),
    ORGANIZATION_NAME VARCHAR(100),
    DEATH_COUNTRY VARCHAR(100),
    DEATH_CITY VARCHAR(100),
    DEATH_DATE VARBINARY,
    SEX VARCHAR(4)
) AS COPY FROM '/tmp/input/system_of_records/laureate_pers_inf/*.parquet' PARQUET;

CREATE TABLE laureate_pers_inf AS SELECT * FROM laureate_pers_inf_external;