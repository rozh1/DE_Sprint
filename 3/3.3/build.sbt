ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.12.10"

libraryDependencies ++= Seq( "org.apache.spark" %% "spark-core" % "3.0.0",
  "org.apache.spark" %% "spark-sql" % "3.0.0" )
libraryDependencies += "com.github.tototoshi" %% "scala-csv" % "1.3.10"

lazy val root = (project in file("."))
  .settings(
    name := "Practice_3.3"
  )
