# Stock Market Data Engineering Pipeline

<text></text>

**Status:** 🚧 Work in Progress

An end-to-end data engineering project designed to build a daily stock market data pipeline for Indian stock exchanges (NSE/BSE). The project focuses on extracting historical stock market data, validating it, storing it in PostgreSQL, and eventually building a cloud-based automated data pipeline using AWS.

The pipeline is being developed incrementally, starting with a local environment and gradually moving towards cloud deployment.

## Project Objectives

- Extract historical stock market data for NSE/BSE-listed companies.
- Validate and clean raw stock market data.
- Load structured data into PostgreSQL.
- Design a normalized relational database.
- Automate daily data ingestion.
- Integrate AWS services for cloud-based storage and processing.
- Build analytical dashboards using Metabase.
- Implement logging, monitoring, backup, and data quality checks.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas |
| Data Source | Yahoo Finance (`yfinance`) |
| Database | PostgreSQL |
| Database Connectivity | SQLAlchemy, psycopg2 |
| Migrations | Alembic |
| Cloud Storage | AWS S3 |
| Cloud Processing | AWS Lambda |
| Cloud Database | AWS RDS |
| Scheduling | AWS EventBridge |
| Monitoring | AWS CloudWatch |
| Visualization | Metabase |
| Version Control | Git, GitHub |

*Technologies listed for future phases are planned integrations, not necessarily implemented yet.*

## Current Project Progress

### Phase 1: Data Extraction — Completed

- Integrated Yahoo Finance using the `yfinance` Python library.
- Extracted historical stock market data.
- Tested extraction using `RELIANCE.NS`.
- Generated CSV files containing OHLCV data.
- Generated JSON metadata containing extraction details.

### Phase 2: Data Validation — Completed

- Checked column names and data types.
- Identified missing values.
- Checked duplicate records.
- Validated price-related values.
- Checked whether High is greater than or equal to Low.

### Phase 3: PostgreSQL Data Loading — Completed

- Installed and configured PostgreSQL locally.
- Created the `stock_market_db` database.
- Configured database connectivity using SQLAlchemy.
- Used environment variables to manage database credentials.
- Created the `stock_prices_staging` table.
- Developed a Python loader to insert stock market data.
- Implemented conflict handling using PostgreSQL `ON CONFLICT` for repeatable loads.

### Phase 4: Database Design — In Progress

Planned activities:

- Design a normalized database schema.
- Create an `exchanges` table.
- Create a `stocks` table.
- Create a `daily_stock_prices` table.
- Define primary key and foreign key relationships.
- Migrate existing staging data into the normalized schema.
- Add indexes and optimize database queries.
- Implement database migrations using Alembic.

## Upcoming Development Roadmap

### Phase 5: ETL Pipeline Improvements

- Organize extraction, transformation, and loading into reusable modules.
- Implement incremental data loading.
- Handle missing and duplicate records.
- Improve error handling and logging.
- Make the pipeline idempotent.

### Phase 6: Database Optimization

- Create appropriate indexes.
- Analyze queries using `EXPLAIN ANALYZE`.
- Improve database performance.
- Implement data quality checks.

### Phase 7: AWS Cloud Integration

- Upload raw stock market data to AWS S3.
- Configure AWS RDS for PostgreSQL.
- Deploy ingestion logic using AWS Lambda.
- Configure AWS EventBridge for scheduled execution.
- Store configuration and credentials securely.

### Phase 8: Monitoring and Automation

- Configure AWS CloudWatch monitoring.
- Track pipeline execution and failures.
- Implement automated error notifications.
- Configure scheduled database backups.
- Validate daily pipeline execution.

### Phase 9: Data Visualization

- Connect Metabase to PostgreSQL.
- Create stock market dashboards.
- Visualize historical prices and trading volumes.
- Analyze daily and historical stock performance.

## High-Level Architecture

```text
Yahoo Finance
     |
     v
Python Data Extraction
     |
     v
Raw CSV + JSON Metadata
     |
     v
Data Validation
     |
     v
PostgreSQL Staging Table
     |
     v
Normalized Database
     |
     v
Data Processing & Optimization
     |
     v
AWS S3 + Lambda + RDS
     |
     v
CloudWatch Monitoring
     |
     v
Metabase Dashboards
```
## Important Notes

- This is an ongoing learning and development project.
- The current implementation uses historical daily stock data, not real-time market streaming.
- Yahoo Finance through `yfinance` is an unofficial data-source integration.
- AWS deployment, automation, and dashboards are planned but not yet completed.
- Project features and architecture may evolve during development.

## Project Goal

To develop a reliable, scalable, and automated end-of-day stock market data engineering pipeline that demonstrates practical skills in Python, SQL, PostgreSQL, ETL development, database design, cloud computing, and data visualization.

**More updates will be added as development progresses.**