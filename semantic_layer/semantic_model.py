"""Semantic layer definition for user lifecycle data using boring-semantic-layer.

This module defines the semantic models used to query user lifecycle data
without writing SQL directly.
"""

import os
import ibis
from boring_semantic_layer import SemanticModel


def get_duckdb_connection():
    """Get an Ibis DuckDB connection to the user analytics database.

    Returns:
        ibis.backends.duckdb.Backend: DuckDB connection
    """
    # Path to the DuckDB database
    db_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "evidence_dashboard",
        "sources",
        "user_analytics",
        "data.duckdb"
    )

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"DuckDB database not found at {db_path}")

    conn = ibis.duckdb.connect(db_path, read_only=True)
    return conn


def _load_tables():
    """Load DuckDB tables needed for semantic models.

    Returns:
        dict: Dictionary of table name to Ibis table expression
    """
    conn = get_duckdb_connection()

    # Load the mart_user_state_monthly table
    user_states_monthly_table = conn.table("mart_user_state_monthly")

    return {
        "user_states_monthly_table": user_states_monthly_table,
    }


def create_user_lifecycle_semantic_model():
    """Create semantic model for user lifecycle data from YAML configuration.

    Returns:
        SemanticModel: A semantic model for querying user lifecycle metrics
    """
    tables = _load_tables()

    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(current_dir, "semantic_models.yml")

    # Load the semantic model from YAML
    models = SemanticModel.from_yaml(yaml_path, tables=tables)

    return models["user_lifecycle"]
