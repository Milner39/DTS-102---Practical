import pandas as _PD



"""This script defines formatting functions for the cli module"""



#region Format

class Format:

  @staticmethod
  def bookingsTable(bookings):
    table = {
      "User": [],
      "Film": [],
      "Date Time": [],
      "#Tickets": [],
      #"Cost": []
    }

    for booking in bookings:
      table["User"].append(booking["user"])
      table["Film"].append(booking["film"])
      table["Date Time"].append(booking["datetime"])
      table["#Tickets"].append(len(booking["tickets"]))
      #table["Cost"].append()

    df = _PD.DataFrame(table)
    print(df)

#region
