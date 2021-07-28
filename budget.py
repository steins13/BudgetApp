class Category:
  def __init__(self, name):
      self.name = name
      self.ledger = []
      self.balance = 0

  def deposit(self, amount, description = None):
    if description == None:
      description = ""

    self.ledger.append({"amount": amount, "description": description})
    self.balance = self.balance + amount

  def get_balance(self):
    return self.balance
   
  def check_funds(self, amount):
    if amount > self.balance:
      return False
    else:
      return True

  def withdraw(self, amount, description = None):
    if description == None:
      description = ""
        
    canWithdraw = self.check_funds(amount)

    if canWithdraw:
      self.ledger.append({"amount": -amount, "description": description})
      self.balance = self.balance - amount
      return True
    else:
      return False

  def transfer(self, amount, category):
    withdrawDone = self.withdraw(amount, "Transfer to " + category.name)
    
    if withdrawDone:
      category.deposit(amount, "Transfer from " + self.name)
      return True
    else:
      return False

  def __repr__(self):
    #for title
    title = ''
    numOfAst = (30 - len(self.name))
    while numOfAst > 0:
      title = title + "*"
      if numOfAst - 1 == (30 - len(self.name)) / 2 or numOfAst - 1 == ((30 - len(self.name)) / 2) - 0.5:
        title = title + self.name
      numOfAst = numOfAst - 1

    #for transactions
    body = ''
    for transaction in self.ledger:
      amount = "{:.2f}".format(transaction["amount"])
      description = transaction["description"][:23]
      numOfSpaces = 30 - (len(amount) + len(description))
      
      body = body + description
      while numOfSpaces > 0:
        body = body + " "
        numOfSpaces = numOfSpaces - 1

      body = body + amount + "\n"

    #for total
    total = "Total: " + "{:.2f}".format(self.balance)

    return title + "\n" + body + total


def create_spend_chart(categories):
  #setup
  totalWithdraw = 0
  withdrawPerCategory = []
  withdraw = 0
  for category in categories:
    for transaction in category.ledger:
      if transaction["amount"] < 0:
        withdraw = withdraw - transaction["amount"]

    totalWithdraw = totalWithdraw + withdraw
    withdrawPerCategory.append(withdraw)
    withdraw = 0

  #chart
  percentage = totalWithdraw / 10
  chartArr = ["\n  0| ", "\n 10| ", "\n 20| ", "\n 30| ", "\n 40| ", "\n 50| ", "\n 60| ", "\n 70| ", "\n 80| ", "\n 90| ", "\n100| "]

  for amount in withdrawPerCategory:
    loop = 0
    loopPercentage = 0
    while amount > loopPercentage:
      chartArr[loop] = chartArr[loop] + "o  "
      loopPercentage = loopPercentage + percentage
      loop = loop + 1
    while loopPercentage <= totalWithdraw:
      chartArr[loop] = chartArr[loop] + "   "
      loopPercentage = loopPercentage + percentage
      loop = loop + 1

  chart = ""
  for item in reversed(chartArr):
    chart = chart + item 

  #dashes
  loop = 0
  dashes = "\n    -"
  while loop < len(categories):
    dashes = dashes + "---"
    loop = loop + 1

  #name
  categoryNames = []
  longestName = 0
  for category in categories:
    if len(category.name) > longestName:
      longestName = len(category.name)
    categoryNames.append(category.name)

  verticalName = [""]
  perLine = "     "
  index = 0
  while index < longestName:
    for name in categoryNames:
      try:
        perLine = perLine + name[index] + "  "
      except:
        perLine = perLine + "   "
    if index == longestName - 1:
      verticalName[0] = verticalName[0] + perLine
      perLine = "     "
      index = index + 1  
    else:    
      verticalName[0] = verticalName[0] + perLine + "\n"
      perLine = "     "
      index = index + 1

  result = "Percentage spent by category" + chart + dashes + "\n" + verticalName[0]
  return result  


