import barcode
from barcode.writer import ImageWriter
from barcode.codex import Code128

text="BENONI TEXT TEST"

code = Code128(
    text,
    writer=ImageWriter()
)
code.save("static/barcode")

