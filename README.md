# ETL Pipeline for PostgreSQL to ClickHouse

This project implements an ETL pipeline that collects and restructures data from a PostgreSQL database, loads it into ClickHouse, and generates statistics and visualizations. The pipeline is orchestrated using Apache Airflow and containerized with Docker Compose.

## Project Overview

The pipeline is designed for a mock e-commerce database that includes information about products, reviews, and delivery points. The main objectives of the project are:

- **Data Transformation and Loading**: Extract data from PostgreSQL and load it into ClickHouse.
- **Statistics and Visualizations**: Build statistics on popular products, reviews, delivery point usage, and other key business metrics.
- **Scheduling**: Run the pipeline either manually or on a scheduled basis (daily, weekly, monthly, quarterly, yearly).

### Main Tools Used:

- **PostgreSQL**: Source database containing e-commerce data.
- **ClickHouse**: Data warehouse used for storing and analyzing data.
- **Apache Airflow**: Workflow scheduler and orchestrator for running ETL tasks.
- **Docker & Docker Compose**: Containerization for easy deployment of all components.
- **Plotly / ClickHouse**: Visualization of business metrics.


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/GaganovAlexander/ETL-pipeline-course.git
   cd ETL-pipeline-course
   ```
2. Build and start services using Docker Compose:
```bash
docker-compose up --build
```
This command will start the following containers:

- **PostgreSQL**: A PostgreSQL container with the mock e-commerce database.
- **ClickHouse**: A ClickHouse container for data warehouse operations.
- **Airflow**: An Apache Airflow container for task orchestration.
- **Nginx**: A reverse proxy to access the Airflow web interface.
3. Access the Airflow web interface at http://localhost:8080. The default credentials are:
- **Username:** ```admin```
- **Password:** ```admin```
4. You can trigger the ETL pipeline manually or set it to run on a schedule via the Airflow web UI.

## DAGs
### Main DAG
The **main DAG** is responsible for transferring data from PostgreSQL to ClickHouse. It runs as scheduled or manually and performs the following tasks:

1. Extract data from PostgreSQL.
2. Transform and clean the data.
3. Load the data into ClickHouse.
4. Build statistics and visualizations on the transferred data.
### Test DAG
The **test DAG** generates artificial data to simulate transactions, reviews, and deliveries for testing the pipeline. It runs once to populate the database with test data.

## Configuration
### PostgreSQL
The PostgreSQL database is set up with an e-commerce schema that follows the 6th normal form, with all data integrity issues handled during the insertion phase. The database includes tables for products, reviews, deliveries, and order information.
### ClickHouse
ClickHouse stores the transformed data for efficient querying and analysis. The schema is designed to allow fast aggregation and filtering of large volumes of data.
### Airflow
Airflow is used to orchestrate the ETL tasks. Two DAGs are included:
- **The main DAG** for the regular ETL process.
- **The test DAG** for generating artificial data.

### Docker
All components (PostgreSQL, ClickHouse, Airflow, Nginx) are containerized using Docker. The ```docker-compose.yml``` file defines the services and their dependencies.

## Usage
1. **Trigger the ETL pipeline manually:** Access the Airflow web interface and trigger the main DAG to start the ETL process.
2. **Schedule the pipeline:** Set up the DAG to run on a schedule (daily, weekly, etc.) via the Airflow web interface.
3. **Monitor task execution:** Use the Airflow web interface to monitor task execution, review logs, and troubleshoot any issues.

## Visualizations
Once the data is loaded into ClickHouse, you can use ClickHouse's native visualization tools or connect with Plotly to create and display statistics, such as:
- Popular products.
- Review analytics.
- Delivery point usage.
- Revenue metrics.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/GaganovAlexander/ETL-pipeline-course/blob/main/LICENSE) file for details.

## Acknowledgements
- [Apache Airflow](https://airflow.apache.org)
- [ClickHouse](https://clickhouse.com)
- [Docker](https://www.docker.com)
- [PostgreSQL](https://www.postgresql.org)