# 🗂️ data-descriptor

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**data-descriptor** is a lightweight Python utility designed to act as a mini Data Catalog for your local files. Given a directory containing tabular data (CSV or Parquet), it automatically generates a structured JSON metadata file. 

This file maps out the global database properties, translates internal Python/Arrow data types into standard SQL formats (like `VARCHAR` or `INTEGER`), counts rows efficiently, and allows you to define conceptual foreign-key relations between your flat files.

## ✨ Features

* **Automated Schema Extraction:** Instantly reads CSV and Parquet files to map column names and translate data types to standard SQL.
* **Highly Efficient:** Leverages `pyarrow` to read Parquet metadata in milliseconds without loading the actual data into memory.
* **Topology Mapping:** Supports defining conceptual relations (e.g., Many-to-One) between separate flat files.
* **Standardized JSON Output:** Produces clean, human-readable metadata files perfect for documentation or downstream data engineering pipelines.
* **CLI Ready:** Can be executed directly from your terminal with arguments.

## ⚙️ Installation

1. Clone this repository or download the source code.
2. Ensure you have Python 3.8 or higher installed.
3. Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```
(Dependencies: pandas and pyarrow)

### 🚀 Usage
**1. Command Line Interface (CLI)**
The easiest way to use data-descriptor is directly from your terminal. Just point it to the folder containing your data files.

**Basic usage:**

```Bash
python data_descriptor.py ./path/to/your/data_folder
```
**Advanced usage** (Custom Database Name and Output File):

```Bash
python data_descriptor.py ./sales_2024 --dbname "Sales CRM Database" --output "sales_metadata.json"
```

**Arguments:**
- 'directory': (Required) Path to the directory containing the CSV/Parquet files.

- '--dbname': (Optional) Name of your dataset/database. Default is "Generic Database".

- '--output': (Optional) Name of the generated JSON file. Default is "metadata.json".

2. Programmatic Usage (Python Module)
If you need to add custom table relations (Foreign Keys), since these are not stored natively in CSV/Parquet files, you can import the class and use it in your own Python scripts:

```Python
from data_descriptor import DataDescriptor


# 1. Initialize the descriptor
descriptor = DataDescriptor(
    directory_path="./my_ecommerce_data",
    database_name="E-Commerce Relational DB"
)

# 2. Define custom relations (From Column, To Column, Relation Type)
descriptor.add_relation("orders.user_id", "users.id", "Many-to-One")
descriptor.add_relation("order_items.order_id", "orders.id", "Many-to-One")
descriptor.add_relation("order_items.product_id", "products.id", "Many-to-One")

# 3. Generate and save the JSON
descriptor.save_to_json("ecommerce_metadata.json")
```

### 📄 Output Example
The script will generate a clean, highly readable JSON file resembling the following structure:


```JSON
{
    "system_metadata": {
        "database_name": "E-Commerce Relational DB",
        "last_update": "2026-04-29 10:45:00",
        "format": "Mixed"
    },
    "relations": [
        {
            "from": "orders.user_id",
            "to": "users.id",
            "type": "Many-to-One"
        }
    ],
    "tables": {
        "users": {
            "row_count": 150000,
            "columns": {
                "id": "INTEGER",
                "name": "VARCHAR",
                "email": "VARCHAR",
                "created_at": "TIMESTAMP"
            }
        },
        "orders": {
            "row_count": 850340,
            "columns": {
                "id": "INTEGER",
                "user_id": "INTEGER",
                "total_amount": "FLOAT"
            }
        }
    }
}
```

### 🛠️ How It Works under the Hood
- **Data Type Mapping**: It intercepts native types (like int64, float64, object) and converts them into standard SQL equivalents (INTEGER, FLOAT, VARCHAR, TIMESTAMP).

- **Parquet Handling**: Uses pq.ParquetFile() to read only the metadata chunk of Parquet files. This allows it to instantly retrieve schemas and row counts for massive files (GBs in size) without RAM overhead.

- **CSV Handling**: Reads the CSV using pandas to infer datatypes and get accurate row counts. (Note: Very large CSVs may consume considerable RAM. Converting large flat files to Parquet is highly recommended).

### 🤝 Contributing
Feel free to open an issue or submit a pull request if you want to add new features, like chunk-reading for massive CSV files or automatic relation inference heuristics!