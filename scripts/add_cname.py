"""
Just a script that is ran by GitHub actions to add the CNAME file to the built website.
"""

CNAME = "devgoldy.xyz"

open("./build/CNAME", mode="w").write(CNAME)