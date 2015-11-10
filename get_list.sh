#!/bin/bash

# https://publicsuffix.org/
URL="https://publicsuffix.org/list/public_suffix_list.dat"

curl -L "${URL}" -o "public_suffix_list.dat";
