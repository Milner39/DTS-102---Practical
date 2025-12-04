from database import user__dataByAuth

username = input("Enter your username: ")
password = input("Enter your password: ")

userData = user__dataByAuth(username, password)

if (userData == None):
  print("Incorrect username/password combination")
else:
  print("Here's your data")
  print(userData)