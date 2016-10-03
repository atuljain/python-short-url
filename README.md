### python-short-url

<code>pip install flask</code>

<code>sqlite3 urls.db</code>

CREATE TABLE WEB_URL(ID INT PRIMARY KEY   AUTOINCREMENT,  URL  TEXT    NOT NULL );

### To run server

<code>python main.py</code>

Sample Post request to Get your short URL

Method == 'POST'
Heaader = {
   'Content-Type':'application/json'
}
url = 'https://python-short-url.herokuapp.com/v1/url/short'

data = {
      'url':'http://www.cricbuzz.com/live-cricket-scores/16823/ind-vs-nz-2nd-test-new-zealand-tour-of-india-2016'
   }

Response 

{
  "short_url": "http://python-short-url.herokuapp.com/s/8"
}


Base 64
refernce url http://tools.ietf.org/html/rfc3548.html

Base encoding of data is used in many situations to store or transfer
   data in environments that, perhaps for legacy reasons, are restricted
   to only US-ASCII [9] data.  Base encoding can also be used in new
   applications that do not have legacy restrictions, simply because it
   makes it possible to manipulate objects with text editors.

   In the past, different applications have had different requirements
   and thus sometimes implemented base encodings in slightly different
   ways.  Today, protocol specifications sometimes use base encodings in
   general, and "base64" in particular, without a precise description or
   reference.  MIME [3] is often used as a reference for base64 without
   considering the consequences for line-wrapping or non-alphabet
   characters.  The purpose of this specification is to establish common
   alphabet and encoding considerations.  This will hopefully reduce
   ambiguity in other documents, leading to better interoperability.

   The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
   "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this
   document are to be interpreted as described in RFC 2119 [1].
