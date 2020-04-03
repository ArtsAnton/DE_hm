package com.example

import org.apache.spark.{SparkConf, SparkContext}
import org.json4s._
import org.json4s.jackson.JsonMethods._

case class User(id: Int = 0, country: String = "", points: Int = 0, title: String = "", variety: String = "", winery: String = "")

object JsonReader extends  App {
  implicit val formats: DefaultFormats.type = DefaultFormats
  val conf = new SparkConf().setMaster("local[*]").setAppName("JsonReader")
  val sc = new SparkContext(conf)
  sc.textFile(args(0)).map(json => parse(json).extract[User]).collect().map(line => println(line))

}