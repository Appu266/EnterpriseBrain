from app.readers.txt_reader import TXTReader


reader = TXTReader()

content = reader.read(
    "tests/sample_plsql.txt"
)

print(content)