# Local Data Stack

An end-to-end local data stack featuring Python data generation, DuckDB, dbt, and Evidence.dev for generating, transforming, and visualizing synthetic user and transaction data.

## 🏗️ Architecture

- **Python**: Generates synthetic user and transaction data
- **DuckDB**: Local analytical database for data storage  
- **dbt**: Transforms raw data into staging and mart layers
- **Evidence.dev**: Interactive dashboards and visualizations
- **UV**: Python package management and virtual environments

## 📁 Project Structure

```
localdatastack/
├── pyproject.toml              # UV project configuration
├── run.sh                      # Simple execution script
├── user_analytics/
│   └── run.py                  # Main orchestration script
├── data_generation/
│   └── generate_data.py        # Synthetic data generation script
├── dbt_project/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── data.duckdb             # DuckDB database file
│   └── models/
│       ├── staging/            # 1:1 with source tables
│       └── marts/              # Final analytical models
└── evidence_dashboard/
    ├── package.json
    ├── pages/                  # Dashboard pages
    └── sources/                # SQL queries for Evidence
```

## 🚀 Quick Start

### Prerequisites

- [UV](https://docs.astral.sh/uv/) installed
- [Node.js](https://nodejs.org/) (for Evidence.dev)

### Run Everything

```bash
# Clone and navigate to project
cd localdatastack

# Run the complete pipeline (extract → transform → dashboard)
./run.sh
```

This single command will:
1. Install all dependencies
2. Generate synthetic user and transaction data
3. Transform data using dbt
4. Start the Evidence dashboard at http://localhost:3000

### Individual Steps

You can also run individual parts of the pipeline:

```bash
# Setup only
./run.sh --setup

# Generate data only
./run.sh --generate

# Transform data only  
./run.sh --transform

# Start dashboard only
./run.sh --dashboard

# Skip setup (if already done)
./run.sh --skip-setup
```

## 📊 Data Models

### Staging Layer
- `stg_users`: Clean user data from generated CSV
- `stg_transactions`: Clean transaction data from generated CSV

### Marts Layer
- `dim_users`: User dimension with behavioral metrics and segmentation
- `fct_transactions`: Transaction facts with user context and derived metrics

## 🎯 Dashboard Features

The Evidence dashboard includes:

- **Overview**: User activation rates and behavioral segmentation
- **User Analysis**: Detailed user metrics and activation patterns
- **Transaction Analysis**: Transaction patterns and timing analysis

## 🔧 Development

### Manual Data Generation
```bash
cd data_generation
uv run python generate_data.py
```

### Manual dbt Runs
```bash
cd dbt_project
uv run dbt run
uv run dbt test
```

### Evidence Development
```bash
cd evidence_dashboard
npm run dev
```

## 🧪 Testing

```bash
# Test dbt models
cd dbt_project
uv run dbt test

# Check data quality
uv run dbt run --full-refresh
```

## 📝 Configuration

### Data Generation
- Generates 1000 synthetic users with realistic behavior patterns
- Creates transactions spanning 2022 with various user segments
- Output: Raw data in DuckDB `raw_data` schema

### dbt Configuration  
- Database: DuckDB at `data.duckdb`
- Target: `dev` environment
- Materializations:
  - Staging: `view`
  - Marts: `table`

### Evidence Configuration
- Database: DuckDB connection to `../dbt_project/data.duckdb`
- Layout: Sidebar navigation

## 🛠️ Troubleshooting

### Common Issues

1. **UV not found**: Install UV using the instructions at https://docs.astral.sh/uv/
2. **Node.js missing**: Install Node.js from https://nodejs.org/
3. **Database locked**: Stop any running processes and retry
4. **API connection issues**: Check internet connectivity

### Clean Restart

```bash
# Remove database and start fresh
rm -f dbt_project/data.duckdb
./run.sh
```

## 🎨 Customization

- **Modify data generation**: Edit `data_generation/generate_data.py` to change user behaviors or data volume
- **Create new models**: Add SQL files to `dbt_project/models/`
- **Add dashboard pages**: Create new `.md` files in `evidence_dashboard/pages/`
- **Modify visualizations**: Edit existing pages or create new components

## 📚 Learn More

- [dbt Documentation](https://docs.getdbt.com/)
- [DuckDB Documentation](https://duckdb.org/docs/)
- [Evidence Documentation](https://evidence.dev/docs)
- [UV Documentation](https://docs.astral.sh/uv/)
- [pandas Documentation](https://pandas.pydata.org/docs/)