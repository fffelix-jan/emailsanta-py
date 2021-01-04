from emailsanta import *


myLetter = SantaEmail("Rudolph", 1, 4, "New York", "United States", 3, "carrots", "food", "phone", comment="Hi Santa, this is a test.", consent=False, email="test@example.com")
theReply = SantaReply(myLetter)
print(theReply.replyText)