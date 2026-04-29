import os
import json
import argparse
from datetime import datetime
import pandas as pd
import pyarrow.parquet as pq

class DataDescriptor:
    def __init__(self, directory_path, database_name="Generic Database"):
        self.directory_path = directory_path
        self.database_name = database_name
        self.relations = []

    def add_relation(self, from_col, to_col, rel_type="Many-to-One"):
        """Adds a manual relation to the metadata."""
        self.relations.append({
            "from": from_col,
            "to": to_col,
            "type": rel_type
        })

    def _map_dtype_to_sql(self, dtype):
        """Maps pandas/pyarrow data types to standard SQL types."""
        dtype_str = str(dtype).lower()
        if 'int' in dtype_str:
            return 'INTEGER'
        elif 'float' in dtype_str:
            return 'FLOAT'
        elif 'bool' in dtype_str:
            return 'BOOLEAN'
        elif 'datetime' in dtype_str or 'timestamp' in dtype_str:
            return 'TIMESTAMP'
        else:
            return 'VARCHAR'

    def _process_csv(self, file_path):
        """Processes a CSV file."""
        df = pd.read_csv(file_path)
        row_count = len(df)
        
        columns = {}
        for col_name, dtype in df.dtypes.items():
            columns[col_name] = self._map_dtype_to_sql(dtype)
            
        return row_count, columns

    def _process_parquet(self, file_path):
        """Processes a Parquet file efficiently without loading data into memory."""
        parquet_file = pq.ParquetFile(file_path)
        row_count = parquet_file.metadata.num_rows
        
        schema = parquet_file.schema
        columns = {}
        for i in range(len(schema)):
            col_name = schema.names[i]
            dtype = schema.column(i).physical_type 
            columns[col_name] = self._map_dtype_to_sql(dtype)
            
        return row_count, columns

    def generate_metadata(self):
        """Generates the complete metadata structure."""
        tables_metadata = {}
        general_format = "Mixed" 
        formats_found = set()

        if not os.path.exists(self.directory_path):
            raise FileNotFoundError(f"The directory {self.directory_path} does not exist.")

        for filename in os.listdir(self.directory_path):
            file_path = os.path.join(self.directory_path, filename)
            table_name, ext = os.path.splitext(filename)
            ext = ext.lower()

            if ext == '.csv':
                row_count, columns = self._process_csv(file_path)
                formats_found.add("CSV")
            elif ext == '.parquet':
                row_count, columns = self._process_parquet(file_path)
                formats_found.add("Parquet")
            else:
                continue 

            tables_metadata[table_name] = {
                "row_count": row_count,
                "columns": columns
            }

        if len(formats_found) == 1:
            general_format = list(formats_found)[0]
        elif len(formats_found) == 0:
            general_format = "Unknown"

        metadata_json = {
            "system_metadata": {
                "database_name": self.database_name,
                "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "format": general_format
            },
            "relations": self.relations,
            "tables": tables_metadata
        }

        return metadata_json

    def save_to_json(self, output_filename="metadata.json"):
        """Generates the metadata and saves it to a file."""
        data = self.generate_metadata()
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✅ Metadata generated successfully in '{output_filename}'")


# ==========================================
# CLI Execution
# ==========================================
if __name__ == "__main__":
    # Setup argument parser for command line usage
    parser = argparse.ArgumentParser(description="Extract metadata from a directory of CSV and Parquet files.")
    parser.add_argument("directory", help="Path to the directory containing the data files")
    parser.add_argument("--dbname", default="Generic Database", help="Name of the database/dataset (optional)")
    parser.add_argument("--output", default="metadata.json", help="Output JSON filename (optional)")
    
    args = parser.parse_args()

    # Instantiate and run the descriptor based on terminal arguments
    try:
        descriptor = DataDescriptor(
            directory_path=args.directory,
            database_name=args.dbname
        )
        
        # Note: If you need to add specific relations for a dataset, 
        # you would call descriptor.add_relation(...) here before saving.

        descriptor.save_to_json(args.output)
        
    except Exception as e:
        print(f"❌ Error generating metadata: {e}")