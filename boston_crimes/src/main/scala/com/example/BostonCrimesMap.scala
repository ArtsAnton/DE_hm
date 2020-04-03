package com.example

import org.apache.spark.sql.functions._
import org.apache.spark.sql.SparkSession

object BostonCrimesMap extends App {

  val spark = SparkSession
    .builder()
    .appName("crime")
    .master("local[*]")
    .getOrCreate()

  import spark.implicits._

  val crime = spark
    .read
    .option("header", value = true)
    .option("inferSchema", value = true)
    .csv(args(0))

  val codes = broadcast(spark
    .read
    .option("header", value = true)
    .option("inferSchema", value = true)
    .csv(args(1))
    .distinct()
    .select($"CODE", trim(split(col("NAME"),"-").getItem(0)).as("crime_type"))).toDF()

  crime.createOrReplaceTempView("crime")
  codes.createOrReplaceTempView("codes")

  //общее число преступлений в районе и ср. коор ВАРИАНТ 1
  val crimes_total = spark.sql(
    "SELECT DISTRICT as Dist, COUNT(INCIDENT_NUMBER) as crimes_total, AVG(Lat) as lat, AVG(Long) as lng " +
      "FROM crime GROUP BY Dist"
  )
  // рвсчет медианы
  val crimes_monthly = spark.sql(
    "SELECT DISTRICT as dist, APPROX_PERCENTILE(INCIDENT, 0.5) as crimes_monthly " +
      "FROM (Select DISTRICT, YEAR, MONTH, COUNT(INCIDENT_NUMBER) as INCIDENT FROM crime GROUP BY DISTRICT, YEAR, MONTH) GROUP BY dist"
  )

  //Поиск 3-х наиболее частых видов преступлений по районам
  val crime_type_df = spark.sql(
    "SELECT INC.DISTRICT, INC.crime_type " +
      "FROM (SELECT DISTRICT, crime_type, COUNT(*) as INCIDENT, " +
      "row_number() OVER(PARTITION BY DISTRICT ORDER BY COUNT(*) DESC) pos FROM crime JOIN codes " +
      "ON crime.OFFENSE_CODE=codes.CODE  GROUP BY DISTRICT, crime_type) AS INC WHERE pos<4"
  )
    .groupBy($"DISTRICT") //Объед. 3-х наиболее частых видов преступлений в одну строку
    .agg(concat_ws(", ", collect_list($"crime_type")).alias("frequent_crime_types"))

  crimes_total
    .join(crimes_monthly, crimes_total("Dist") === crimes_monthly("dist"))
    .join(crime_type_df, crimes_total("Dist") === crime_type_df("DISTRICT"))
    .select($"DISTRICT", $"crimes_total", $"lat", $"lng", $"crimes_monthly", $"frequent_crime_types")
    .repartition(1)
    .write
    .option("header", value = true)
    .parquet(args(2))
}
