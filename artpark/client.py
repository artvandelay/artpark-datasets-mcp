"""
ARTPARK Public Data Client
Reads local CSV files and metadata.yaml from the publicdata repo.
Architecture adapted from mospi/client.py in esankhyiki-mcp.

Architecture:
    publicdata/data/
      {dataset_id}/
        metadata.yaml       # Column schema, table definitions
        *.csv                # Data files
        {subdir}/            # Optional subdirectories with more CSVs
          metadata.yaml
          *.csv

Key behaviors:
    - Table names in metadata.yaml may differ from CSV filenames (hyphens vs underscores)
    - _resolve_csv_path tries multiple name variants and subdirectories
    - Filter values are case-insensitive (str.lower() comparison)
    - Summary stats are auto-computed for up to 10 numeric columns
"""

import os
import yaml
import pandas as pd
from typing import Dict, Any, Optional, List


class ARTPARKData:
    """
    Local data reader for ARTPARK public datasets.
    Reads CSVs and metadata.yaml files from publicdata/data/*/.
    """

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "publicdata", "data")
        self.data_dir = data_dir
        self._catalogue: Optional[Dict[str, Any]] = None

    # =========================================================================
    # Catalogue / Discovery
    # =========================================================================

    def _build_catalogue(self) -> Dict[str, Any]:
        """Scan data directory and build catalogue from metadata.yaml files."""
        catalogue = {}
        if not os.path.isdir(self.data_dir):
            return catalogue

        for entry in sorted(os.listdir(self.data_dir)):
            dataset_path = os.path.join(self.data_dir, entry)
            if not os.path.isdir(dataset_path):
                continue

            meta_path = os.path.join(dataset_path, "metadata.yaml")
            csv_files = self._find_csv_files(dataset_path)

            info = {"dataset_id": entry, "tables": [], "csv_files": csv_files}

            tables_from_meta = []
            if os.path.exists(meta_path):
                meta = self._load_yaml(meta_path)
                tables_meta = meta.get("tables", {})
                for table_name, table_data in tables_meta.items():
                    if not isinstance(table_data, dict):
                        continue
                    table_info = table_data.get("info", {})
                    if not isinstance(table_info, dict):
                        table_info = {}
                    tables_from_meta.append({
                        "name": table_name,
                        "about": table_info.get("about", ""),
                        "source": table_info.get("source", ""),
                    })

            if tables_from_meta:
                info["tables"] = tables_from_meta
            else:
                # Fallback: metadata.yaml missing, empty, or failed to parse.
                for csv_file in csv_files:
                    table_name = os.path.splitext(csv_file)[0]
                    info["tables"].append({"name": table_name, "about": "", "source": ""})

            catalogue[entry] = info

        return catalogue

    def _load_yaml(self, path: str) -> dict:
        """Load a YAML file, returning empty dict on parse errors."""
        try:
            with open(path, "r") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError:
            return {}

    def _find_csv_files(self, dataset_path: str) -> List[str]:
        """Find all CSV files in a dataset directory (non-recursive)."""
        return sorted([
            f for f in os.listdir(dataset_path)
            if f.endswith(".csv")
        ])

    def get_catalogue(self) -> Dict[str, Any]:
        """Return cached catalogue of all datasets."""
        if self._catalogue is None:
            self._catalogue = self._build_catalogue()
        return self._catalogue

    def list_datasets(self) -> Dict[str, Any]:
        """List all available datasets with basic info."""
        catalogue = self.get_catalogue()
        datasets = {}
        for dataset_id, info in catalogue.items():
            table_summaries = [t["about"] for t in info["tables"] if t["about"]]
            datasets[dataset_id] = {
                "num_tables": len(info["tables"]),
                "num_csv_files": len(info["csv_files"]),
                "description": table_summaries[0] if table_summaries else "",
                "csv_files": info["csv_files"],
            }
        return {"total_datasets": len(datasets), "datasets": datasets}

    # =========================================================================
    # Dataset Exploration (Tables)
    # =========================================================================

    def get_dataset_tables(self, dataset_id: str) -> Dict[str, Any]:
        """List tables and their info for a specific dataset."""
        dataset_path = os.path.join(self.data_dir, dataset_id)
        if not os.path.isdir(dataset_path):
            return {"error": f"Dataset '{dataset_id}' not found."}

        meta_path = os.path.join(dataset_path, "metadata.yaml")
        csv_files = self._find_csv_files(dataset_path)

        # Check for subdirectories with additional data
        subdirs = []
        for entry in sorted(os.listdir(dataset_path)):
            sub_path = os.path.join(dataset_path, entry)
            if os.path.isdir(sub_path):
                sub_csvs = self._find_csv_files(sub_path)
                if sub_csvs:
                    subdirs.append({"name": entry, "csv_files": sub_csvs})

        result = {
            "dataset_id": dataset_id,
            "csv_files": csv_files,
            "subdirectories": subdirs,
            "tables": [],
        }

        tables_from_meta = []
        if os.path.exists(meta_path):
            meta = self._load_yaml(meta_path)
            tables_meta = meta.get("tables", {})
            for table_name, table_data in tables_meta.items():
                if not isinstance(table_data, dict):
                    continue
                table_info = table_data.get("info", {})
                if not isinstance(table_info, dict):
                    table_info = {}
                dd = table_data.get("data_dictionary", {})
                columns = list(dd.keys()) if isinstance(dd, dict) else []
                tables_from_meta.append({
                    "name": table_name,
                    "about": table_info.get("about", ""),
                    "source": table_info.get("source", ""),
                    "comments": table_info.get("comments", ""),
                    "num_columns": len(columns),
                    "columns": columns,
                })

        if tables_from_meta:
            result["tables"] = tables_from_meta
        else:
            # Fallback: metadata.yaml missing, empty, or failed to parse.
            # Infer tables from CSV filenames and read column headers.
            for csv_file in csv_files:
                table_name = os.path.splitext(csv_file)[0]
                csv_path = os.path.join(dataset_path, csv_file)
                try:
                    df = pd.read_csv(csv_path, nrows=0)
                    columns = list(df.columns)
                except Exception:
                    columns = []
                result["tables"].append({
                    "name": table_name,
                    "about": "",
                    "source": "",
                    "num_columns": len(columns),
                    "columns": columns,
                })

        return result

    # =========================================================================
    # Table Metadata (Data Dictionary + Filter Values)
    # =========================================================================

    def get_table_schema(self, dataset_id: str, table_name: str) -> Dict[str, Any]:
        """
        Get the data dictionary and summary stats for a specific table.
        Returns column descriptions + unique values for key columns (for filtering).
        """
        dataset_path = os.path.join(self.data_dir, dataset_id)
        if not os.path.isdir(dataset_path):
            return {"error": f"Dataset '{dataset_id}' not found."}

        # Load metadata.yaml
        meta_path = os.path.join(dataset_path, "metadata.yaml")
        data_dictionary = {}
        table_info = {}
        if os.path.exists(meta_path):
            meta = self._load_yaml(meta_path)
            tables_meta = meta.get("tables", {})
            table_meta = tables_meta.get(table_name, {})
            if isinstance(table_meta, dict):
                dd = table_meta.get("data_dictionary", {})
                data_dictionary = dd if isinstance(dd, dict) else {}
                ti = table_meta.get("info", {})
                table_info = ti if isinstance(ti, dict) else {}

        # Also check subdirectory metadata
        if not data_dictionary:
            for entry in os.listdir(dataset_path):
                sub_path = os.path.join(dataset_path, entry)
                sub_meta = os.path.join(sub_path, "metadata.yaml")
                if os.path.isdir(sub_path) and os.path.exists(sub_meta):
                    sub_yaml = self._load_yaml(sub_meta)
                    sub_tables = sub_yaml.get("tables", {})
                    if table_name in sub_tables:
                        st = sub_tables[table_name]
                        if isinstance(st, dict):
                            dd = st.get("data_dictionary", {})
                            data_dictionary = dd if isinstance(dd, dict) else {}
                            ti = st.get("info", {})
                            table_info = ti if isinstance(ti, dict) else {}
                        break

        # Find the CSV file
        csv_path = self._resolve_csv_path(dataset_id, table_name)
        csv_summary = {}
        filter_values = {}

        if csv_path and os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path, low_memory=False)
                csv_summary = {
                    "total_rows": len(df),
                    "total_columns": len(df.columns),
                    "columns": list(df.columns),
                    "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                }

                # Extract unique values for categorical/ID columns (useful for filtering)
                MAX_CATEGORICAL_VALUES = 50
                MAX_TEMPORAL_VALUES = 100
                omitted_columns = []
                for col in df.columns:
                    if df[col].dtype == "object" or "ID" in col or "name" in col.lower():
                        unique_vals = df[col].dropna().unique()
                        if 1 < len(unique_vals) <= MAX_CATEGORICAL_VALUES:
                            filter_values[col] = sorted(unique_vals.tolist())
                        elif len(unique_vals) > MAX_CATEGORICAL_VALUES:
                            omitted_columns.append(f"{col} ({len(unique_vals)} unique values)")
                    elif "year" in col.lower() or "round" in col.lower() or "date" in col.lower():
                        unique_vals = df[col].dropna().unique()
                        if 1 < len(unique_vals) <= MAX_TEMPORAL_VALUES:
                            filter_values[col] = sorted(unique_vals.tolist())
                        elif len(unique_vals) > MAX_TEMPORAL_VALUES:
                            omitted_columns.append(f"{col} ({len(unique_vals)} unique values)")
                if omitted_columns:
                    filter_values["_omitted"] = (
                        f"These columns have too many unique values to list: {', '.join(omitted_columns)}. "
                        f"You can still filter on them -- use values from the data rows returned by 4_get_data()."
                    )

            except Exception as e:
                csv_summary = {"error": f"Could not read CSV: {e}"}

        result = {
            "dataset_id": dataset_id,
            "table_name": table_name,
            "info": table_info,
            "data_dictionary": data_dictionary,
            "csv_summary": csv_summary,
            "filter_values": filter_values,
        }
        return result

    # =========================================================================
    # Data Query
    # =========================================================================

    def query_table(
        self,
        dataset_id: str,
        table_name: str,
        filters: Optional[Dict[str, str]] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """
        Read a CSV table, apply optional filters, return rows + summary.
        """
        csv_path = self._resolve_csv_path(dataset_id, table_name)
        if csv_path is None:
            return {"error": f"CSV not found for dataset '{dataset_id}', table '{table_name}'."}

        try:
            df = pd.read_csv(csv_path, low_memory=False)
        except Exception as e:
            return {"error": f"Failed to read CSV: {e}"}

        total_rows_before_filter = len(df)

        # Apply filters (case-insensitive for string columns)
        applied_filters = {}
        if filters:
            for col, value in filters.items():
                if col not in df.columns:
                    return {
                        "error": f"Column '{col}' not found.",
                        "valid_columns": sorted(df.columns.tolist()),
                        "hint": "Call 3_get_metadata() to see valid column names and filter values.",
                    }
                col_vals = df[col].astype(str)
                if isinstance(value, str) and "," in value:
                    values = [v.strip() for v in value.split(",")]
                    # Case-insensitive matching for string columns
                    lower_vals = [v.lower() for v in values]
                    df = df[col_vals.str.lower().isin(lower_vals)]
                else:
                    df = df[col_vals.str.lower() == str(value).lower()]
                applied_filters[col] = value

        total_rows_after_filter = len(df)

        # Build summary stats for numeric columns
        MAX_STATS_COLUMNS = 10
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        summary_stats = {}
        if numeric_cols and len(df) > 0:
            stats_cols = numeric_cols[:MAX_STATS_COLUMNS]
            desc = df[stats_cols].describe()
            summary_stats = {
                col: {
                    "min": round(desc.at["min", col], 4) if pd.notna(desc.at["min", col]) else None,
                    "max": round(desc.at["max", col], 4) if pd.notna(desc.at["max", col]) else None,
                    "mean": round(desc.at["mean", col], 4) if pd.notna(desc.at["mean", col]) else None,
                }
                for col in stats_cols
            }
            if len(numeric_cols) > MAX_STATS_COLUMNS:
                summary_stats["_note"] = (
                    f"Showing stats for {MAX_STATS_COLUMNS} of {len(numeric_cols)} numeric columns. "
                    f"Omitted: {', '.join(numeric_cols[MAX_STATS_COLUMNS:])}"
                )

        # Return limited rows
        rows = df.head(limit).to_dict(orient="records")

        return {
            "dataset_id": dataset_id,
            "table_name": table_name,
            "total_rows_before_filter": total_rows_before_filter,
            "total_rows_after_filter": total_rows_after_filter,
            "filters_applied": applied_filters,
            "rows_returned": len(rows),
            "limit": limit,
            "summary_stats": summary_stats,
            "data": rows,
        }

    # =========================================================================
    # Helpers
    # =========================================================================

    def _resolve_csv_path(self, dataset_id: str, table_name: str) -> Optional[str]:
        """
        Find the CSV file for a given dataset_id and table_name.

        Resolution order:
        1. Exact match: {table_name}.csv in dataset dir
        2. Hyphenated variant: underscores → hyphens
        3. Underscore variant: hyphens → underscores
        4. Same variants in subdirectories
        5. Fuzzy: any CSV in dataset dir whose stem contains table_name (or vice versa)
        """
        dataset_path = os.path.join(self.data_dir, dataset_id)
        if not os.path.isdir(dataset_path):
            return None

        # Build candidate filenames
        candidates = [
            f"{table_name}.csv",
            table_name.replace("_", "-") + ".csv",
            table_name.replace("-", "_") + ".csv",
        ]

        # Try exact matches in dataset dir
        for candidate in candidates:
            path = os.path.join(dataset_path, candidate)
            if os.path.exists(path):
                return path

        # Try exact matches in subdirectories
        for entry in os.listdir(dataset_path):
            sub_path = os.path.join(dataset_path, entry)
            if os.path.isdir(sub_path):
                for candidate in candidates:
                    sub_csv = os.path.join(sub_path, candidate)
                    if os.path.exists(sub_csv):
                        return sub_csv

        # Fuzzy fallback: find CSV files whose stem contains the table name or vice versa
        # This handles cases where metadata defines a merged table name that doesn't
        # directly correspond to any single CSV file (e.g., "nadcp-vaccination-progress"
        # when the actual files are round1.csv, round2.csv, etc.)
        normalized = table_name.lower().replace("-", "").replace("_", "")
        for csv_file in self._find_csv_files(dataset_path):
            stem = os.path.splitext(csv_file)[0].lower().replace("-", "").replace("_", "")
            if normalized in stem or stem in normalized:
                return os.path.join(dataset_path, csv_file)

        return None


# Global instance
artpark_data = ARTPARKData()
