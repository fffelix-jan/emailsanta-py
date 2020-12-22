"""
emailsanta: Python module to simulate emailing the legendary Christmas 
character Santa, powered by Alan Kerr's emailSanta.com.
"""

# Standard library imports
import re as _re

# Third-party library imports
from bs4 import BeautifulSoup as _BeautifulSoup
import html2text as _html2text
import requests as _requests

# URL of emailSanta.com's reply generator
_emailSantaReplyGen = "https://www.emailsanta.com/letsanta_reg.asp"


class SantaEmail:
    """
    A class to store an "email to Santa", ready to be sent.
    """

    def __init__(
        # Required arguments
        self,
        firstname: str,
        gender: int,
        age: int,
        city: str,
        country: str,
        good: int,
        present1: str,
        present2: str,
        present3: str,
        # Optional arguments
        comment: str = "",
        consent: bool = False,
        email: str = "",
        stamp: int = 1,
    ):
        """
        Constructs a :class:`SantaEmail` which stores an letter that can be
        sent to the emailSanta.com server for an instant, automated reply
        "from Santa".

        Required arguments:
        :param firstname: The sender's first name as a string. The first letter
        of the name will automatically be capitalized by the server if not
        already capitalized.

        :param gender: The sender's gender as an integer. Use `1` to denote
        `"boy"` and `2` to denote `"girl"`. If the gender is any other value other
        than `1` or `2`, then it will be silently converted to `"boy"`. emailSanta.com
        does not currently support unspecified or non-binary genders as of
        2020-12-14.

        :param age: The user's age as an integer. If the value is a float, it
        will be silently converted to an integer. If the age is less than `0`,
        a ValueError will be raised.

        :param city: The name of the sender's city as a string.

        :param country: The name of the sender's country as a string.

        :param good: How good the sender has been this year as an integer.  
        `0` denotes "my halo has been to the repair shop a few times".  
        `1` denotes "I should still be on the 'Nice' list!"  
        `2` denotes "my halo is just a little bit crooked!!"  
        `3` denotes "I should be the angel at the top of the tree!"  
        Any other value will raise a ValueError.

        :param present1: The sender's first present request as a string.

        :param present2: The sender's second present request as a string.

        :param present3: The sender's third present request as a string.

        Optional arguments:
        :param stamp: Chooses a graphical "stamp" on the letter. As this library
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

        :param email: The sender's email. If the sender appears to be in crisis,
        the staff at emailSanta.com might email them regarding the issue using
        the given email.

        :param comment: An additional message to Santa from the sender as a string.
        Defaults to empty.

        :param consent: Whether or not the sender consents to his/her comments
        being shared here: https://www.emailsanta.com/read_santa_letters.asp,
        as a boolean. Defaults to ``False`` (the letter will not be shared publicly.)
        """

        # Input Validation

        if isinstance(firstname, str):
            self.firstname = firstname
        else:
            raise TypeError("firstname must be a string")

        if isinstance(gender, int):
            self.gender = gender
        else:
            raise TypeError("gender must be an integer that is either 1 or 2")

        if isinstance(age, int) or isinstance(age, float):
            if age < 0:
                raise ValueError("age cannot be less than 0")
            else:
                self.age = int(age)
        else:
            raise TypeError("age must be an integer")

        if isinstance(city, str):
            self.city = city
        else:
            raise TypeError("city must be a string")

        if isinstance(country, str):
            self.country = country
        else:
            raise TypeError("country must be a string")

        if isinstance(good, int):
            if not 0 <= good <= 3:
                raise ValueError(
                    "integer for value of good given, but it is not between 0 and 3 inclusive"
                )
            else:
                self.good = good
        else:
            raise TypeError("good must be an integer between 0 and 3 inclusive")

        if isinstance(present1, str):
            self.present1 = present1
        else:
            raise TypeError("present1 must be a string")

        if isinstance(present2, str):
            self.present2 = present2
        else:
            raise TypeError("present2 must be a string")

        if isinstance(present3, str):
            self.present3 = present3
        else:
            raise TypeError("present3 must be a string")

        if isinstance(stamp, int):
            if not 1 <= stamp <= 4:
                raise ValueError(
                    "integer for value of stamp given, but it is not between 1 and 4 inclusive"
                )
            else:
                self.stamp = stamp
        else:
            raise TypeError("stamp must be an integer between 1 and 4 inclusive")

        if isinstance(email, str):
            if _re.match(r"[^@]+@[^@]+\.[^@]+", email) or email == "":
                self.email = email
            else:
                raise ValueError("email does not appear to be a valid email address")
        else:
            raise TypeError("email must be a string")

        if isinstance(comment, str):
            self.comment = comment
        else:
            raise TypeError("comment must be a string")

        if isinstance(consent, bool):
            self.consent = consent
        else:
            raise TypeError("consent must be a boolean")


class SantaReply:
    """
    A class that defines the reply generation of letters from Santa. Upon
    initialization of a `SantaReply`, the data will be sent to the server, and
    Santa's reply will be saved in the object.
    """

    def __init__(self, toSendLetter: SantaEmail):
        """
        Creates a `SantaReply`, which will automatically access the emailSanta.com
        server and generate Santa's letter upon initialization. If the Internet
        is not working or the servers are down, the object creation will fail.

        Required argument:
        :param toSendLetter: An instance of `SantaEmail` containing the letter
        to be sent to Santa.
        """

        def __genderString(genderInt: int):
            """
            Converts a gender integer to a string used by emailSanta.com.
            Returns one of the following:
            `2` - "girl"
            anything else - "boy"
            Non-binary genders are not supported by emailSanta.com yet.

            Required argument:
            :param genderInt: The gender integer.
            """
            if genderInt == 2:
                return "girl"
            else:
                return "boy"

        def __goodString(goodInt: int):
            """
            Converts a good-ness integer to a string used by emailSanta.com.
            Returns one of the following:
            `3` - "REALLY REALLY good"
            `2` - "really good"
            `1` - "good"
            anything else - "sorta good"

            Required argument:
            :param goodInt: The good-ness integer.
            """
            if goodInt == 3:
                return "REALLY REALLY good"
            elif goodInt == 2:
                return "really good"
            elif goodInt == 1:
                return "good"
            else:
                return "sorta good"

        def __decodeCFEmail(e: str):
            """
            Decodes an obfuscated email address.
            :param e: The obfuscated email address as a string.
            """
            de = ""
            k = int(e[:2], 16)

            for i in range(2, len(e) - 1, 2):
                de += chr(int(e[i : i + 2], 16) ^ k)

            return de

        if not isinstance(toSendLetter, SantaEmail):
            raise TypeError("letter to send must be a SantaEmail")

        # Prepare the data to send
        userSendPOST = {
            "lang": "EN",
            "firstname": toSendLetter.firstname,
            "email": toSendLetter.email,
            "gender": __genderString(toSendLetter.gender),
            "age": str(toSendLetter.age),
            "city": toSendLetter.city,
            "region": " ",  # not in use by emailSanta.com (formerly used to store the user's province/state)
            "country": toSendLetter.country,
            "good": __goodString(toSendLetter.good),
            "present1": toSendLetter.present1,
            "present2": toSendLetter.present2,
            "present3": toSendLetter.present3,
            "comment": toSendLetter.comment,
            "consent": "Yes" if toSendLetter.consent else "No",
            "stamp": toSendLetter.stamp,
            "treat": " ",  # not in use (formerly to attach a "treat" such as hugs and kisses, cookies, etc.)
            "ATT": "",  # not in use; not sure what this is for
            "PageCheckqElf": "1",  # not sure what this is for
        }

        # Make the POST request and save the response
        self.rawResponse = _requests.post(_emailSantaReplyGen, data=userSendPOST)

        # Scrape the "letter" part of the webpage using BeautifulSoup
        __soup = _BeautifulSoup(self.rawResponse.text, features="lxml")

        # Remove noprint div's
        for div in __soup.find_all("div", {"class": "noprint"}):
            div.decompose()

        # Remove noprint paragraphs
        for p in __soup.find_all("p", {"class": "noprint"}):
            p.decompose()

        # Remove noprint headings
        for h1 in __soup.find_all("h1", {"class": "noprint"}):
            h1.decompose()

        # Remove "skip to main content"
        for a in __soup.find_all("a", {"class": "skip-main"}):
            a.decompose()

        # Remove the no JavaScript warning
        for noscript in __soup.select("noscript"):
            noscript.decompose()

        # Un-obfuscate the email addresses
        for a in __soup.find_all("a", {"class": "__cf_email__"}):
            a.string = __decodeCFEmail(a["data-cfemail"])

        # Replace the image of Santa's signature with text
        for img in __soup.find_all("img", {"class": "santaSig"}):
            img.string = img["alt"]
            img.attrs = {}
            img.name = "b"

        # Set up the text maker
        textMaker = _html2text.HTML2Text()

        textMaker.ignore_links = True
        textMaker.ignore_images = True
        textMaker.emphasis_mark = ""
        textMaker.strong_mark = ""
        textMaker.body_width = 0

        # Convert the HTML to plain text
        self.replyText = textMaker.handle(str(__soup))