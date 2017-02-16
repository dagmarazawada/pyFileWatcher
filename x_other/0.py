#!/usr/bin/python

import os, time
path_to_watch = "."
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
  time.sleep (1)
  after = dict ([(f, None) for f in os.listdir (path_to_watch)])
  added = [f for f in after if not f in before]
  removed = [f for f in before if not f in after]
  if added: print("Added: ", ", ".join (added))
  if removed: print("Removed: ", ", ".join (removed))
  before = after

[os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(".")) for f in fn]
[os.path.join(dp, f) for dp, dn, fn in os.walk(".") for f in fn]



