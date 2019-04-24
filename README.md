# SyntheticDatasetGenerator

## Dependencies

```
pip install -r requirements.txt
```
- python >=3.6
- liquibase in the path (in case documentation generation needed)
- postgresql database (in case both documentation & data loaded needed)

## Run

1. Push your base file into input
1. Fill config/sdgen.yaml
1. Run make clean run ddl


## Install

```
make
```

## Test

```
make test
```

## Principle

# Goal

- input:
    - a config file in yaml
    - csv files already existing (eg: terminologies)
- output: 
    - one ore multiple data csv reproductible

# Csv Format (input & output)

Csv must respect:
- encoding: utf-8
- separator: ";"
- quote: False
- header: None
- date format: "%Y-%M-%d"
- datetime format: "%Y-%M-%d %H:%m:%s"
- strings must not contain the separator (";")

# Table

- Primary Keys: each table must have an integer primary key
- Foreign Keys: they must refer a primary key.

# Yaml Configuration

- Table
  - existing table must have a "input" defined
  - generated table must not have "input" defined
- Fields Class
  - sequence: an autoincrement from 1 to "table.tableSize"
  - simple (percentNull)
    - integer (begin, end)
    - bigint (begin, end)
    - date (begin, end)
    - time (begin, end)
    - varchar (begin, end)
    - regexp (pattern)
    - real (begin, end, decimal)
  - lookup (fk, table, field)


# Data Type

- DBC Type      Java Type
- CHAR          String
- VARCHAR       String
- LONGVARCHAR   String
- NUMERIC       java.math.BigDecimal
- DECIMAL       java.math.BigDecimal
- BIT           boolean
- BOOLEAN       boolean
- TINYINT       byte
- SMALLINT      short
- INTEGER       int
- BIGINT        long
- REAL          float
- FLOAT         double
- DOUBLE        double
- BINARY        byte[]
- VARBINARY     byte[]
- LONGVARBINARY byte[]
- DATE          java.sql.Date
- TIME          java.sql.Time
- TIMESTAMP     java.sql.Timestamp
- CLOB          Clob
- BLOB          Blob
- ARRAY         Array
- DISTINCT      mapping of underlying type
- STRUCT        Struct
- REF           Ref
- DATALINK      java.net.URL
- JAVA_OBJECT   underlying Java class

# Generate schema

```
make load doc
```
