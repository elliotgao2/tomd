# June 27 2017
# Andrew Xia
# main program (for testing stuff)

import tomd

# FOLDER = "/home/andrew/Documents/Evernote_170625/"
FOLDER = "/home/andrew/Documents/Github/evernote-analysis"
# FILE = "Week11.html"
FILE = "pensive.html"
CONTENT = ""

FOLDER = "/home/andrew/Documents/Evernote_170625/Log/2016"
FILE = "Week 10 37 to 313.html"

f = open(FOLDER + "/" + FILE)
for line in f:
  CONTENT += line

# CONTENT = """
# <p>For <em>Implementing</em>, working with <a href="http://chiraag.scripts.mit.edu/wiki/start" target="_blank"><strong>Chiraag Juvekar</strong></a> and <a href="http://www-mtl.mit.edu/~anantha/" target="_blank"><strong>Prof. Anantha Chandrakasan</strong></a>.</p>

# <h3 id="abstract">Abstract</h3>

# <p>Having an
# is </p>
# <hr/>
# <p>My paper can be found <a href="/files/superUROP.pdf"><strong>here</strong></a></p>
# """

# CONTENT = """
# <table bgcolor="#D4DDE5" border="0">
# <tr><td><b>Created:</b></td><td><i>10/31/2011 8:59 PM</i></td></tr>
# <tr><td><b>Updated:</b></td><td><i>5/12/2012 5:42 PM</i></td></tr>
# <tr><td><b>Tags:</b></td><td><i>birthday</i></td></tr>
# </table>
# """

# CONTENT = """<table border="1" cellpadding="2" cellspacing="0" style="font-size: 13px;" width="100%"><tbody><tr><td valign="top">Day (Sleep)</td><td valign="top">Internet</td><td valign="top">SAT Plan/Actual</td><td valign="top">PRIMES</td><td valign="top">Homework</td><td valign="top">Athletics</td></tr><tr><td valign="top">Monday<br/>
# 7hr</td><td valign="top">2.30hr<br/>
# 4LOL</td><td valign="top"><br/></td><td valign="top">0.05min<br/>
# Email, </td><td valign="top">Dartmouth</td><td valign="top"><br/></td></tr><tr><td valign="top">Tuesday<br/>
# 10hr</td><td valign="top">1.50hr<br/>
# LOL</td><td valign="top">:SAT K8</td><td valign="top">1.00hr<br/>
# 7Zip Data</td><td valign="top"><br/></td><td valign="top">Swim</td></tr><tr><td valign="top">Wednesday<br/>
# 11hr</td><td valign="top">1.54hr<br/>
# LOL</td><td valign="top">SAT 36</td><td valign="top">1.10hr<br/>
# HIV Data, trying excel convert</td><td valign="top">College</td><td valign="top">Swim</td></tr><tr><td valign="top">Thursday<br/>
# 10hr</td><td valign="top">1.37min<br/>
# 4LOL</td><td valign="top">SAT 36, 35</td><td valign="top"><br/></td><td valign="top"><br/></td><td valign="top">Swim</td></tr><tr><td valign="top">Friday<br/>
# 10hr</td><td valign="top">0.30min</td><td valign="top"><br/></td><td valign="top"><br/></td><td valign="top">Driving Lesson</td><td valign="top">Swim</td></tr><tr><td valign="top">Saturday<br/>
# 8hr</td><td valign="top">2.10hr<br/>
# 3LOL</td><td valign="top"><br/></td><td valign="top"><br/></td><td valign="top"><br/></td><td valign="top">Swim Meet</td></tr><tr><td valign="top">Sunday<br/>
# 9hr</td><td valign="top">1.08hr<br/>
# 2LOL</td><td valign="top"><br/></td><td valign="top"><br/></td><td valign="top"><br/></td><td valign="top">Swim Meet</td></tr></tbody></table>
# """

converter = tomd.Tomd(CONTENT,FOLDER,FILE)
# print(converter.markdown())

