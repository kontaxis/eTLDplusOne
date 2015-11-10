#!/usr/bin/python -u

# kontaxis 2015-11-03

# Mozilla maintains a public list of DNS suffixes which are not under the
# control of individual registrants. The registered or registrable domain
# is the public suffix plus one additional label (eTLD+1).
#
# This program will take a hostname as input and return its eTLD+1
# or the hostname itself.
# e.g., ./eTLDplusOne.py foo.example.com will return example.com
# e.g., ./eTLDplusOne.py example.com     will return example.com
# e.g., ./eTLDplusOne.py example.invalid will return example.invalid
#
# Figuring out the eTLD+1 is useful when deciding the scope of a domain or
# grouping a set of domains under a common site.

# References:
# - https://publicsuffix.org/list/

from __future__ import print_function

import argparse
import os
import sys
import sqlite3

class eTLDplusOne:
	verbose = False

	_dbConnCursor = None

	def __init__(self, dbPath):
		conn = sqlite3.connect(dbpath)
		conn.text_factory = str
		self._dbConnCursor = conn.cursor()

	def calculate(self, domains):
		eTLDplusOneDomains = []

		for domain in domains:
			# A domain or rule can be split into a list of labels using the
			# separator "." (dot). The separator is not part of any of the labels.
			# Empty labels are not permitted, meaning that leading and trailing
			# dots are ignored.
			labels = domain.strip(".").split(".")

			# If not eTLD is found in the database,
			# make the current domain the eTLD+1.
			eTLDplusOneDomain = domain

			# If a domain matches more than one rule in the file, the longest
			# matching rule (the one with the most levels) will be used.
			for i in range(1, len(labels)):
				# A domain is said to match a rule if and only if all of the
				# following conditions are met:
				# When the domain and rule are split into corresponding labels,
				# that the domain contains as many or more labels than the rule.
				# Beginning with the right-most labels of both the domain and
				# the rule, and continuing for all labels in the rule, one finds
				# that for every pair, either they are identical, or that the label
				# from the rule is "*".
				# XXX We only check for wildcards in the left-most label.
				eTLD      = ".".join(        labels[i:len(labels)])
				eTLD_wild = ".".join(["*"] + labels[i+1:len(labels)])
				if eTLD_wild == "*":
					eTLD_wild = eTLD

				self.verbose and print("eTLD '%s' OR eTLD '%s' : " % (
					eTLD, eTLD_wild), end="")

				self._dbConnCursor.execute(
					'SELECT eTLD FROM eTLDs WHERE eTLD=? OR eTLD=?', (eTLD, eTLD_wild))
				match = self._dbConnCursor.fetchone()
				if not match:
					self.verbose and print("eTLD+1 NONE")
					continue

				# eTLD has been found.
				eTLDplusOneDomain = "%s" % ".".join(labels[i-1:len(labels)])

				if self.verbose:
					print("eTLD+1 '%s'" % eTLDplusOneDomain)

				break

			eTLDplusOneDomains.append(eTLDplusOneDomain)

		return eTLDplusOneDomains


if __name__ == "__main__":

	# Parse arguments.
	parser = argparse.ArgumentParser(description=
		"Given a domain return its suffix comprised of " +
		"the subdomain following its effective top-level domain " +
		"and the effective top-level domain itself.")

	parser.add_argument("--verbose", "-v",
		action="store_const", const=True, default=False,
		help = "Output information on the process.")

	parser.add_argument("domains", metavar="D", nargs="+",
		help="Domain to look up.")

	args = parser.parse_args()

	# Make sure the SQLite3 database file exists in the same directory.
	dirname = os.path.dirname(sys.argv[0])
	dbpath  = os.path.join(dirname, "db.sqlite3")

	if not os.path.exists(dbpath):
		print("ERROR. Path '%s' is unavailable." % dbpath, file=sys.stderr)
		sys.exit(-1)

	if not os.path.isfile(dbpath):
		print("ERROR. Path '%s' is not a file."  % dbpath, file=sys.stderr)
		sys.exit(-1)

	eTLDpOne = eTLDplusOne(dbpath)
	eTLDpOne.verbose = args.verbose

	eTLDpOneDomains = eTLDpOne.calculate(args.domains)
	for eTLDpOneDomain in eTLDpOneDomains:
		print("%s" % eTLDpOneDomain)

	# Success
	if eTLDpOneDomains:
		sys.exit(0)

	# Failure
	sys.exit(1)
