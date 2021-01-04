# emailsanta
 A Python library to "send a letter to Santa" using emailSanta.com and receive a properly-formatted automated reply "as fast as reindeer fly"!  

 Licensed under AGPL 3.0.  
 Reminder: If you use this library in a Discord bot or any other network application, you have to disclose the source code, even if the bot is accessed over the Internet. 

 Any data submitted will be processed by emailSanta.com in accordance to [their privacy policy](https://www.emailsanta.com/privacy.asp). I, Félix An, am not responsible for the processing of the data.

 Disclaimer: Santa Claus is not real. This library and emailSanta.com are for entertainment purposes only.
## Installing
 Install using pip:  
 ```
 pip install emailsanta
 ```


 ## Usage
 The library provides two classes: `SantaEmail` and `SantaReply`. Simply import them like this:
 ```python
 from emailsanta import *
 ```

 ### Writing a letter
 To prepare an email to "send to Santa", create an instance of `SantaEmail`, and fill in the arguments.  

 Required arguments:  

`firstname` - The sender's first name as a string. The first letter
of the name will automatically be capitalized by the server if not
already capitalized.

`gender` - The sender's gender as an integer. Use `1` to denote
`"boy"` and `2` to denote `"girl"`. If the gender is any other value other
than `1` or `2`, then it will be silently converted to `"boy"`. emailSanta.com
does not currently support unspecified or non-binary genders as of
2020-12-14.

`age` - The user's age as an integer. If the value is a float, it
will be silently converted to an integer. If the age is less than `0`,
a ValueError will be raised.

`city` - The name of the sender's city as a string.

`country` - The name of the sender's country as a string.

`good` - How good the sender has been this year as an integer.
`0` denotes "my halo has been to the repair shop a few times".  
`1` denotes "I should still be on the 'Nice' list!"  
`2` denotes "my halo is just a little bit crooked!!"  
`3` denotes "I should be the angel at the top of the tree!"  
Any other value will raise a ValueError.

`present1` - The sender's first present request as a string.

`present2` - The sender's second present request as a string.

`present3` - The sender's third present request as a string.

Optional arguments:  

`comment` - An additional message to Santa from the sender as a string.
Defaults to empty.

`consent` - Whether or not the sender consents to his/her comments
being shared here: https://www.emailsanta.com/read_santa_letters.asp,
as a boolean. Defaults to ``False`` (the letter will not be shared publicly.)

`email` - The sender's email. If the sender appears to be in crisis,
the staff at emailSanta.com might email them regarding the issue using
the given email.

`stamp` - Chooses a graphical "stamp" on the letter. As this library
removes any images in Santa's response, changing this does not have any
effect in this library. The choice, as an integer, can be one of four
choices:  
`1` - "HO! HO! HO! It's Santa on a stamp!" (default)  
`2` - "Frosty always thought his nose looked too big in this photo!"  
`3` - "Rudolph had trouble keeping his nose from glowing too brightly so
the picture would turn out!"  
`4` - "Mrs. Claus is always smiling!"  
Any other value will raise a ValueError.  
Defaults to stamp `1`.


For example:
```python
# assuming you already imported everything
mySantaLetterToSend = SantaEmail(
    "Rudolph",      # name
    1,              # gender (in this case it is boy)
    4,              # age
    "New York",     # city
    "United States",# country
    3,              # how good have you been? (in this case it's really really good!)
    "carrots",      # your first present
    "food",         # your second present
    "phone",        # your third present
    comment="Hi Santa, this is a test.",    # any additional comments for Santa
)
```

### Getting a reply
Once you have created your `SantaEmail` object, you can create a `SantaReply` object. Upon initialization of a `SantaReply`, it will automatically make a POST request to the emailSanta.com reply generator and save the response as a plaintext string, without any text formatting. The raw `Response` object created using the `requests` library is also available for you to process if desired. The website likes to use Unicode emojis, so make sure you use the encoding `utf-8` if necessary.

For example, to obtain a reply for the letter you created above, you could write the following code:

```python
# continued from above
myReplyFromSanta = SantaReply(mySantaLetterToSend)  # get your reply "from Santa"!
print(mySantaLetterToSend.replyText)    # this prints the plaintext reply
```