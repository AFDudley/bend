# A hash-addressed import's own qualified book key keeps the hash in its
# name (the real case: a bend-mathlib-style package import such as
# 0xcd4682.../nat.bend). js_key already quotes any string as a JS object
# key, so the JS lane needs no guard; the Python lane's exported def name
# must still parse, and the built module must still answer the call.
import Base

def Hash.import_export() -> IO(U32):
  import "./hash_import_export.js"

def main() -> IO(Unit):
  do IO<Unit>:
    value : U32 <- Hash.import_export()
    IO.print(U32.show(value))

#|0
