from emailsanta import *


myLetter = SantaEmail("Rudolph", 1, 4, "New York", "United States", 3, "carrots", "food", "phone", comment="Hi Santa, this is a test.")
theReply = SantaReply(myLetter)
print(theReply.replyText)