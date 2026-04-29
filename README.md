# Data Descriptor
A lightweight Python tool designed to act as a mini Data Catalog for your local files. Given a directory containing tabular data (CSV or Parquet), it generates a structured JSON metadata file. This file maps out the global database properties, translates internal data types into standard SQL formats (like VARCHAR or INTEGER), counts rows efficiently, and allows you to define conceptual foreign-key relations between your flat files.

**Key Features:
**
- **Automated Schema Extraction**: Instantly reads CSV and Parquet files to map column names and translate data types to standard SQL.

- **Highly Efficient**: Leverages pyarrow to read Parquet metadata in milliseconds without loading data into memory.

- **Topology Mapping**: Supports defining conceptual relations (e.g., Many-to-One) between separate flat files.

- **Standardized JSON Output**: Produces clean, human-readable metadata files perfect for documentation or downstream data engineering pipelines.