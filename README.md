# eTLDplusOne

```
usage: eTLDplusOne.py [-h] [--verbose] D [D ...]

Given a domain return its suffix comprised of the subdomain following its
effective top-level domain and the effective top-level domain itself.

positional arguments:
  D              Domain to look up.

optional arguments:
  -h, --help     show this help message and exit
  --verbose, -v  Output information on the process.
```

```
# ./eTLDplusOne.py example.com bar.example.com foo.bar.example.com
example.com
example.com
example.com

# ./eTLDplusOne.py cloudfront.net bar.cloudfront.net foo.bar.cloudfront.net
cloudfront.net
bar.cloudfront.net
bar.cloudfront.net
```
