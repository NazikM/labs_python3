#!/usr/bin/env python3

from http import cookies
import os
import cgi

form = cgi.FieldStorage()
name = form.getfirst("firstname", "Default name")
surname = form.getfirst("secondname", "Default surname")
if form.getvalue("dropdown"):
    gender = form.getvalue("dropdown")
else:
    gender = 'Not chosen'

langs = [form.getvalue("python"), form.getvalue("js"), form.getvalue("java"), form.getvalue("other_lang")]


# витягуємо кукі
cs = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
if "form_counter" in cs:
    form_counter = cs.get("form_counter").value
    print(f"Set-cookie: form_counter={int(form_counter) + 1}")
else:
    form_counter = "1"
    print("Set-cookie: form_counter=1")


def myfunc(langs_list):
    res = ""
    for i in langs_list:
        if i:
            res += f"<p>{i}</p>"
    if not res:
        res = "<p>Not chosen</p>"
    return res

HTML = f'''<!DOCTYPE html>
<html lang="en-US">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
    <title>My test page</title>
  </head>
  <body>
  <h4>Name: {name}</h4>
  <h4>Surname: {surname}</h4>
  <h5>Gender: {gender}</h5>
  <h5>Favorite programming languages:</h5>
  {myfunc(langs)}
  <h5>Form counter (cookie) {form_counter}</h5>
  </body>
</html>'''

print("Content-type: text/html\r\n\r\n")
print()
print(HTML)
# print(form)
