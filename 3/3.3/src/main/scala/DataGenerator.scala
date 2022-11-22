import java.io.File
import com.github.tototoshi.csv._

import java.util.Date
import scala.collection.mutable

object DataGenerator {
  var AccountId: Long = 0
  var TimeStamp: Integer = 0
  val rand = new scala.util.Random
  val CurrentTimeStamp: Int = (new Date().getTime / 1000).toInt
  var UserList = new mutable.HashSet[Any]()

  def GenData(clickFilePath: String, accountFilePath: String, rowCount: Integer): Unit = {
    TimeStamp = (new Date().getTime / 1000).toInt

    val f = new File(clickFilePath)
    val writer = CSVWriter.open(f)
    var rowIndex = 0
    while (rowIndex < rowCount) {
      writer.writeRow(GenRow())
      rowIndex += 1
    }
    writer.close()

    val accountFile = new File(accountFilePath)
    val accountWriter = CSVWriter.open(accountFile)
    UserList.foreach(userId => {
      accountWriter.writeRow(GenAccount(userId))
    })
    accountWriter.close()
  }

  def GenAccount(userId: Any): Seq[Any] = {
    Seq(GetNextAccountId(), userId, GetNextUserName(), GetNextUserBirthday(), GetNextUserRegDate())
  }

  def GenRow(): Seq[Any] = {
    val row = Seq(GetNextId(), GetNextTimeStamp(), GetNextType(), GetNextPageId(), GetNextTag(), GetNextSign())
    if (row(5) == true) {
      if (!UserList.contains(row(0)))
        UserList.add(row(0))
    }
    row
  }

  def GetNextId(): Long = {
    rand.nextInt(1000)
  }

  def GetNextTimeStamp(): Integer = {
    TimeStamp += rand.nextInt(60) + 1
    TimeStamp
  }

  def GetNextType(): String = {
    val t = rand.nextInt(4)
    if (t == 0) return "visit"
    if (t == 1) return "click"
    if (t == 2) return "scroll"
    "move"
  }

  def GetNextPageId(): Integer = {
    rand.nextInt(20)
  }

  def GetNextTag(): String = {
    val t = rand.nextInt(5)
    if (t == 0) return "sport"
    if (t == 1) return "politics"
    if (t == 2) return "medicine"
    if (t == 3) return "science"
    null
  }

  def GetNextSign(): Boolean = {
    val p = rand.nextFloat()
    if (p > 0.5) return true
    false
  }

  def GetNextAccountId(): Long = {
    AccountId += 1
    AccountId
  }

  def GetNextUserName(): String = {
    "Посетитель " + AccountId
  }

  def GetNextUserBirthday(): Integer = {
    val age = rand.nextInt(60*60*24*365*60)
    CurrentTimeStamp - age
  }

  def GetNextUserRegDate(): Integer = {
    val age = rand.nextInt(60 * 60 * 24 * 365)
    CurrentTimeStamp - age
  }
}