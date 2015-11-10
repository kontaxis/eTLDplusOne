#!/usr/bin/python -u

# kontaxis 2015-11-03

# References:
# - https://publicsuffix.org/list/

from __future__ import print_function

import os
import sqlite3
import sys
import time

dirname = os.path.dirname(sys.argv[0])

# Populate eTLDs records array
eTLDs = []

f = file(os.path.join(dirname, "public_suffix_list.dat"), "r")

# The list is a set of rules, with one rule per line.
for line in f:
	# The Public Suffix List consists of a series of lines, separated by \n.
	line = line.rstrip("\n")
	# Each line is only read up to the first whitespace;
	line = line.split(" ")[0]
	if line == "":
		continue
	# entire lines can also be commented using //.
	if len(line) > 1 and line[0:2] == "//":
		continue
	# Each line which is not entirely whitespace or
	# begins with a comment contains a rule.
	rule = line
	# A rule may begin with a "!" (exclamation mark). If it does, it is labelled
	# as a "exception rule" and then treated as if the exclamation mark is not
	# present.
	if rule[0] == "!":
		rule = rule[1:]
	eTLDs.append((rule,))

f.close()

# Make it happen
conn = sqlite3.connect("db.sqlite3")
conn.text_factory = str
c = conn.cursor()

# Create schema.
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",
	("last_generated",))
match = c.fetchone()
if not match:
	c.execute("CREATE TABLE last_generated (epoch integer);")
	c.execute("CREATE TABLE eTLDs (eTLD text);")
	c.execute("CREATE INDEX eTLD on eTLDs (eTLD);")

c.execute('DELETE FROM last_generated');
c.execute('INSERT INTO last_generated VALUES(?)',
	(str(int(time.time())),))

c.execute('DELETE FROM eTLDs');
c.executemany('INSERT INTO eTLDs VALUES (?)', eTLDs)

conn.commit()
conn.close()
