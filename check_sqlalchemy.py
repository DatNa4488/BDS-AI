import sqlalchemy
print(f"Version: {sqlalchemy.__version__}")
try:
    from sqlalchemy import case
    print("Direct import: OK")
except ImportError:
    print("Direct import: FAIL")

try:
    from sqlalchemy.sql import case
    print("From sql: OK")
except ImportError:
    print("From sql: FAIL")

try:
    from sqlalchemy.sql.expression import case
    print("From sql.expression: OK")
except ImportError:
    print("From sql.expression: FAIL")

print("Dir:", dir(sqlalchemy))
