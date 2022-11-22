import DataGenerator.GenData
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.{col, desc, udf}
import org.apache.spark.sql.types.{BooleanType, IntegerType, LongType, StringType, StructType}

import java.util.Date
import scala.util.control.Breaks.breakable
import util.control.Breaks._

object Main {
  def main(args: Array[String]): Unit = {

    val spark = SparkSession.builder
      //.master("spark://192.168.1.138:7077")
      .master("local")
      .config("spark.executor.memory", "512M")
      .config("spark.driver.bindAddress", "localhost")
      .config("spark.ui.port", "4044") //4040 знят docker
      .appName("Practice 3.3")
      .getOrCreate()

    val dataSchema = new StructType()
      .add("id", LongType, nullable = false)
      .add("timestamp", IntegerType, nullable = false)
      .add("type", StringType, nullable = false)
      .add("page_id", IntegerType, nullable = false)
      .add("tag", StringType, nullable = true)
      .add("sign", BooleanType, nullable = false)

    //GenData("clicks.csv", "accounts.csv", 10000)

    val df = spark.read.format("csv")
      .schema(dataSchema)
      .load("clicks.csv")

    df.show(10)

    val accountSchema = new StructType()
      .add("id", LongType, nullable = false)
      .add("userId", LongType, nullable = false)
      .add("name", StringType, nullable = false)
      .add("birthday", IntegerType, nullable = false)
      .add("regDate", StringType, nullable = false)
    val accountDf = spark.read.format("csv")
      .schema(accountSchema)
      .load("accounts.csv")

    accountDf.show(10)

    val topActive = df
      .groupBy("id")
      .count()
      .orderBy(desc("count"))
    println("топ-5 самых активных посетителей сайта")
    topActive.show(5)

    println("процент посетителей, у которых есть ЛК = " + (df.where(df("sign") === true).count() / df.count().toFloat) * 100)

    println("топ-5 страниц сайта по показателю общего кол-ва кликов на данной странице")
    df.where(df("type") === "click")
      .groupBy("page_id")
      .count().orderBy(desc("count"))
      .show(5)

    val timeCoder: Int => String = (arg: Int) => {
      import java.text.SimpleDateFormat
      val format = new SimpleDateFormat("HH:mm:ss")
      val date = new Date(arg * 1000L)
      val fDate = format.format(date)
      var hour = 4
      val step = 4
      val periodDate = new Date(2000, 1, 1, hour, 0, 0)
      breakable {
        while (hour <= 20) {
          val fPeriodDate = format.format(periodDate)
          if (fDate <= fPeriodDate) {
            break
          }
          hour += step
          periodDate.setHours(hour)
        }
      }
      "" + (hour - step) + "-" + hour
    }

    val timeCoderSqlFunc = udf(timeCoder)
    val df2 = df.withColumn("time_period", timeCoderSqlFunc(col("timestamp")))
    df2.show()

    println("временной промежуток на основе предыдущего задания, в течение которого было больше всего активностей на сайте")
    df2.groupBy("time_period")
      .count()
      .orderBy(desc("count"))
      .show(1)

    println("фамилии посетителей, которые читали хотя бы одну новость про спорт")
    val df3 = df2.filter(col("tag") === "sport" && col("sign") === true)
      .join(accountDf, df2("id") === accountDf("userId"), "inner")
      .select(col("name"))
      .distinct()
      .orderBy(col("name"))

    df3.show(numRows = df3.count().toInt, truncate = false)
    println(df3.count())
  }

}