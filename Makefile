.PHONY: all clean

all: db.sqlite3

public_suffix_list.dat:
	bash get_list.sh

db.sqlite3: public_suffix_list.dat
	python makedb.py

clean:
	rm -f public_suffix_list.dat db.sqlite3
