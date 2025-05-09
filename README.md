# ETL Pipeline for PostgreSQL to ClickHouse with Superset Dashboard

This project implements a complete ETL pipeline that collects, transforms, and loads data from a PostgreSQL database into ClickHouse, and provides interactive analytics through Apache Superset dashboards. The workflow is orchestrated with Apache Airflow and containerized using Docker Compose.

---

## 🔍 Project Overview

- **Source:** PostgreSQL mock e-commerce database (products, orders, reviews, deliveries).
- **Warehouse:** ClickHouse for high-performance analytics.
- **Orchestration:** Apache Airflow for scheduling and managing ETL tasks.
- **Visualization:** Apache Superset dashboards.
- **Deployment:** Docker Compose for easy setup of all components.

### Main Objectives

1. **Extract, Transform, Load:** Move and reshape data from PostgreSQL into ClickHouse.
2. **Statistics & Insights:** Build key business metrics (sales, reviews, inventory) in ClickHouse.
3. **Dashboard Analytics:** Visualize metrics in Superset dashboards.
4. **Scheduling & Automation:** Run ETL on custom schedules (daily, weekly, etc.) via Airflow.

---

## 🛠️ Technology Stack

| Component          | Purpose                                              |
|--------------------|------------------------------------------------------|
| PostgreSQL         | Source e-commerce OLTP database                      |
| ClickHouse         | Columnar data warehouse for analytics                |
| Apache Airflow     | Workflow orchestration (DAGs for ETL & test data)    |
| Docker & Compose   | Containerization of all services                     |
| Apache Superset    | BI tool for interactive dashboards                   |

---

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/GaganovAlexander/ETL-pipeline-course.git
   cd ETL-pipeline-course
   ```

2. **Start all services** (PostgreSQL, ClickHouse, Airflow, Superset, Nginx)

   ```bash
   docker-compose up --build
   ```
3. **Create ClickHouse database after it loaded:**
   ```bash
   chmod +x init_clickhouse.sh
   ./init_clickhouse.sh
   ```
   p.s. needed after first boot only
4. **Access services:**

   * Airflow UI: [http://localhost:8080](http://localhost:8080) (default **admin/admin**)
   * Superset UI: [http://localhost:8088](http://localhost:8088) (create admin via `docker exec` instructions)
5. **Trigger pipelines:**

   * Airflow → transfer_dag → run manually or schedule.
   * Airflow → create_data_dag → generate sample data.

---

## 📑 DAGs

### 1. Main ETL DAG (transfer_dag)

Performs data movement and transformation:

1. Extract from PostgreSQL.
2. Clean & transform data.
3. Load into ClickHouse tables.
4. Precompute summary tables for Superset.

### 2. Test Data DAG (create_data_dag)

Generates artificial orders, reviews, and deliveries to validate pipeline.

---

## 🔧 Configuration

### PostgreSQL

* Contains normalized e-commerce schema (products, orders, reviews, deliveries).
* Data integrity handled during ingestion.

### ClickHouse

* MergeTree tables optimized for time-series and high-cardinality joins.
* Summary tables and materialized views for dashboard performance.

### Apache Airflow

* Two DAGs deployed: *transfer\_dag*, *create\_data\_dag*.
* Use `schedule_interval` to control run frequency.

### Apache Superset

* Preconfigured datasources pointing to ClickHouse.

---

## 🎯 Usage

1. **Run ETL**: Trigger the `etl_pipeline` DAG in Airflow.
2. **Populate Test Data**: Trigger the `generate_test_data` DAG.
3. **Explore Dashboards**: Log into Superset and open the pre-built dashboards.
4. **Customize**: Add new charts or filters using Superset’s UI.

---

## ⚖️ License

This project is licensed under the MIT License. See [LICENSE](https://github.com/GaganovAlexander/ETL-pipeline-course/blob/main/LICENSE) for details.

---

## 🙏 Acknowledgements

* [Apache Airflow](https://airflow.apache.org)
* [ClickHouse](https://clickhouse.com)
* [Apache Superset](https://superset.apache.org)
* [Docker](https://www.docker.com)
* [PostgreSQL](https://www.postgresql.org)
