package com.example

import org.apache.spark.sql.functions._
import org.apache.spark.sql.SparkSession
import org.apache.log4j.{Level, Logger}

object DataTransformation extends App{

  val spark = SparkSession
    .builder()
    .appName("DataTransformation")
    .master("local[*]")
    .getOrCreate()

  Logger.getLogger("org").setLevel(Level.OFF)
  import spark.implicits._

  val capital = spark.read.json("staging_area/capital.json").withColumn("ISO2", lit("CAPITAL"))
  val continent = spark.read.json("staging_area/continent.json").withColumn("ISO2", lit("CONTINENT"))
  val currency = spark.read.json("staging_area/currency.json").withColumn("ISO2", lit("CURRENCY"))
  val iso3 = spark.read.json("staging_area/iso3.json").withColumn("ISO2", lit("ISO3"))
  val names = spark.read.json("staging_area/names.json").withColumn("ISO2", lit("COUNTRY"))
  val phone = spark.read.json("staging_area/phone.json").withColumn("ISO2", lit("PHONE"))

  val WorldCountriesTable = spark
    .read
    .option("inferSchema", value = true)
    .csv("staging_area/countries_of_the_world.csv")

  val WorldCities = spark
    .read
    .option("inferSchema", value = true)
    .option("header", value = true)
    .csv("staging_area/worldcitiespop.csv")

  val NobelTable = spark
    .read
    .option("inferSchema", value = true)
    .option("delimiter", ";")
    .csv("staging_area/archive_tranform.csv")

  //_______________________  Work with files capital, continent, currency, iso3, names, phone  _________________________

  val CountryTemporaryTable = iso3
    .union(names)
    .union(capital)
    .union(continent)
    .union(currency)
    .union(phone)

  val cols = CountryTemporaryTable
    .columns
    .filter(_ != "ISO2")
    .map(n => struct(lit(n) as "c", col(n) as "v"))

  val exploded_df = CountryTemporaryTable
    .select(col("ISO2"), explode(array(cols : _*)))

  val CountryTable = exploded_df
    .groupBy(col("col.c").as("ISO2"))
    .pivot("ISO2")
    .agg(first(col("col.v")))

  val CountriesAndCapitals = CountryTable
    .select(trim(col("COUNTRY")).as("COUNTRY"), col("CAPITAL"), col("ISO2"))

  val CountryCodes = CountryTable
    .select(trim(col("COUNTRY")).as("COUNTRY"), col("ISO3"), col("PHONE"), col("CURRENCY"))

  CountriesAndCapitals.repartition(1)
    .write
    .option("header", value = true)
    .option("inferSchema", value = true)
    .parquet("system_of_records/countries_and_capitals")

  CountryCodes.repartition(1)
    .write
    .option("header", value = true)
    .option("inferSchema", value = true)
    .parquet("system_of_records/country_codes")
  
  //___________________________________  Work with file countries_of_the_world.csv _____________________________________

  val head = List("COUNTRY", "REGION", "POPULATION", "AREA", "POP_DENSITY", "COASTLINE", "NET_MIGRATION",
    "INFANT_MORTALITY", "GDP", "LITERACY", "PHONES", "ARABLE", "CROPS", "OTHER", "CLIMATE", "BIRTHRATE", "DEATHRATE",
  "AGRICULTURE", "INDUSTRY", "SERVICE")

  val columnsList = WorldCountriesTable.columns.toList

  val NewColumnsList = columnsList.zip(head).map(f => {col(f._1).as(f._2.toUpperCase())})


  val NewWorldCountriesTable = WorldCountriesTable
    .select(NewColumnsList: _*)
    .where(col("COUNTRY") !== "Country")

  val Population = NewWorldCountriesTable
    .select(trim(col("COUNTRY")).as("COUNTRY"), col("POPULATION"),
    col("AREA"), col("POP_DENSITY"), col("COASTLINE"))

  Population.repartition(1)
    .write
    .option("header", value = true)
    .option("inferSchema", value = true)
    .parquet("system_of_records/population")

  val WealthAndHealth = NewWorldCountriesTable
    .select(trim(col("COUNTRY")).as("COUNTRY"), col("NET_MIGRATION"), col("INFANT_MORTALITY"),
    col("GDP"), col("BIRTHRATE"), col("DEATHRATE"))

  WealthAndHealth.repartition(1)
    .write
    .option("header", value = true)
    .option("inferSchema", value = true)
    .parquet("system_of_records/wealth_and_health")

  val Education = NewWorldCountriesTable
    .select(trim(col("COUNTRY")).as("COUNTRY"), col("LITERACY"))

  Education.repartition(1)
    .write
    .option("header", value = true)
    .option("inferSchema", value = true)
    .parquet("system_of_records/education")

  val AreasOfActivity = NewWorldCountriesTable
    .select(trim(col("COUNTRY")).as("COUNTRY"), col("AGRICULTURE"), col("INDUSTRY"), col("SERVICE"))

  AreasOfActivity.repartition(1)
    .write
    .option("header", value = true)
    .option("inferSchema", value = true)
    .parquet("system_of_records/areas_of_activity")

  val Land = NewWorldCountriesTable
    .select(trim(col("COUNTRY")).as("COUNTRY"), col("ARABLE"), col("CROPS"),
      col("OTHER"), col("CLIMATE"))

  Land.repartition(1)
    .write
    .option("header", value = true)
    .option("inferSchema", value = true)
    .parquet("system_of_records/land")

  val Location = CountryTable.as("t1")
    .join(NewWorldCountriesTable.as("t2"), trim($"t1.COUNTRY") === trim($"t2.COUNTRY"))
    .select(trim($"t1.COUNTRY").as("COUNTRY"), $"t1.CONTINENT", $"t2.REGION")

  Location.repartition(1)
    .write
    .option("header", value = true)
    .option("inferSchema", value = true)
    .parquet("system_of_records/location")

  //___________________________________  Work with file worldcitiespop.csv _____________________________________

//  val WorldCitiesTable = CountryCodes.as("t1")
//    .join(WorldCities.as("t2"), $"t1.ISO2" === upper($"t2.Country"))
//    .select($"t1.Country", $"t2.City",$"t2.Population", $"t2.Latitude", $"t2.Longitude")
  WorldCities.select($"Country", $"City", $"Region", $"Population", $"Latitude", $"Longitude")
    .repartition(1)
    .write
    .option("header", value = true)
    .option("inferSchema", value = true)
    .parquet("system_of_records/world_cities")

  //___________________________________  Work with file archive_tranform.csv _____________________________________

  val head2 = NobelTable.head()
    .toSeq
    .map(item => item.toString.replaceAll(" ", "_"))

  val columnsList2 = NobelTable.columns.toList

  val NewColumnsList2 = columnsList2.zip(head2).map(f => {col(f._1).as(f._2.toUpperCase())})

  val NewNobelTable = NobelTable
    .select(NewColumnsList2: _*)
    .where(col("Year") !== "Year")

  val LaureateTable = NewNobelTable
    .select(col("Birth_Country").as("COUNTRY"), col("Year"), col("Category"), col("Full_name"))

  LaureateTable.repartition(1)
    .write
    .option("header", value = true)
    .option("inferSchema", value = true)
    .parquet("system_of_records/laureate_table")

  val LaureatePersInf = NewNobelTable
    .select(col("BIRTH_COUNTRY"), col("BIRTH_CITY"), col("BIRTH_DATE"),
      col("ORGANIZATION_COUNTRY"), col("ORGANIZATION_CITY"), col("ORGANIZATION_NAME"),
      col("DEATH_COUNTRY"), col("DEATH_CITY"), col("DEATH_DATE"), col("SEX"))

  LaureatePersInf.repartition(1)
    .write
    .option("header", value = true)
    .option("inferSchema", value = true)
    .parquet("system_of_records/laureate_pers_inf")

}
