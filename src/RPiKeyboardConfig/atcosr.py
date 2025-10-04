# AtCoSR (C) 2025 by Mikael O. Bonnier, Lund, Sweden. License: Same as the original repo.
fgco=[30,91,32,93,94,95,96,97,92,37,90,31,33,35,34,36]
bgco=fgco[:]
for i in range(len(bgco)):
  bgco[i]+=10

def co(fg,bg):
  return "\x1B[%d;%dm"%(fgco[fg],bgco[bg])

def at(r,c):
  return "\x1B[%d;%dH"%(r+1,c+1)

def cls():
  return at(0,0)+"\x1B[2J"

def cll():
  return "\x1B[K"

def shcu(on):
  if on:
    return "\x1B[?25h"
  else:
    return "\x1B[?25l"

_rbsr=0

def rbsr():
  global _rbsr
  return _rbsr

def csr(rt,rb,cl,cr):
  global _rbsr
  _rbsr=rb
  return "\x1B[?69h\x1B[%d;%dr\x1B[%d;%ds\x1B[%d;%d;%d;%d$z"%(rt+1,rb+1,cl+1,cr+1,rt+1,cl+1,rb+1,cr+1)
  # DECLRMM (CSI?69h), DECSLRM (CSI;s), and DECERA (CSI;;;$z) needs VT420+/xterm to work; ignored otherwise.

def rmsr():
  return "\x1B[r\x1B[;s\x1B[?69l" # DECSLRM and DECLRMM as above.
