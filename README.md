# Microservice Usage Analyzer

## 🚀 Overview

This project is a backend engineering exercise for a fictional cloud service provider. It implements a portion of a **billing system** designed to allow engineering teams to effectively track and analyze **customer usage** of various microservices.

## 🛠️ Key Components and Focus

The system is built around several core components and emphasizes best practices in backend development:

* **FastAPI Web Service:** A robust API service built with **FastAPI** for efficiently receiving, processing, and storing usage data. This forms the core of the usage tracking mechanism.
* **`BillingClient` Library:** A dedicated **client library** designed to simplify the interaction with the FastAPI web service, providing an easy-to-use interface for other services to report usage.
* **Comprehensive Test Suite:** A suite of unit and integration tests to rigorously validate all core functionalities and edge cases, ensuring data accuracy and system reliability.
* **Simulations and Data Scripts:** Tools and scripts for generating realistic usage data and simulating various load patterns and edge case scenarios for thorough system testing.

---

## ✨ Engineering Principles

The development of this project focuses heavily on the following backend engineering principles:

* **Clean, Modular Code:** Emphasis on a well-organized, scalable codebase with clear separation of concerns.
* **Robust Error Handling:** Implementation of comprehensive error handling and validation across all layers of the system to maintain stability.
* **Effective Logging:** Strategic use of logging to provide clear observability into the system's operation, aiding in debugging and performance monitoring.
* **Idempotency:** Designing API endpoints and data processing logic to ensure that multiple identical requests have the same effect as a single request, crucial for reliable billing and tracking.
* **Rigorous Testing:** A commitment to extensive testing to ensure all business logic, data persistence, and API interactions are correct and reliable.

---
## Table of Contents
   1. Project Structure
   2. Setup
   3. Usage
   4. Client Library
   5. Testing and Simulation
   6. Error Handling
   7. Sample Outputs
   8. References & Acknowledgement
   
---
## Project Structure
MicroserviceUsageAnalyzer/
```
MicroserviceUsageAnalyzer/
├── src/
│   ├── __init__.py
│   ├── client.py
│   ├── client_logging.py
│   ├── crud.py
│   ├── api.py
│   ├── simulator.py
│   ├── simulator-test.py
│   ├── generator.py
│   ├── initialize.py
│   ├── service-utils.py
│   └── usage.py
├── tests/
│   ├── __init__.py
│   ├── test__client.py
│   ├── test__crud.py
│   ├── test__api.py
│   └── test__simulator.py
├── logs/
│   ├── client.log
│   ├── generator.log
│   └── simulator.log
├── data/
│   ├── customer__names.csv
│   ├── customers.json
│   └── services__list.json
├── prompts/
├── customers.db
├── test__customers.db
├── testing.db
├── customers__tests.db
├── status.json
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── reference.txt
└── LICENSE
```
---
### Root Directory Files and Folders
```
**customers.db** – Main SQLite database containing customer and usage data.

**test__customers.db** – Test database used for unit tests.

**testing.db** – Another testing database, likely for intermediate/test purposes.

**customers__tests.db** – Additional test database; used for test isolation.

status.json – Stores status information about the system or simulated runs.

docker-compose.yml – Docker Compose configuration file for running services.

Dockerfile – Dockerfile to containerize the application.

requirements.txt – Python dependencies required to run the project.

reference.txt – References and acknowledgements, including data sources and tools used.

LICENSE – License file for the project.

Folders

src/ – Source code for the application. Contains all main scripts:

client.py – Client library to interact with the internal usage tracking API. Handles requests, logging, and error tracking.

crud.py – CRUD operations for database access (create, read, update, delete usage and customer data).

api.py – FastAPI application exposing endpoints for usage tracking.

simulator.py – Generates simulated usage data for testing purposes.

simulator-test.py – Helper scripts for testing simulator outputs.

generator.py – Additional data generation utilities (e.g., random timestamps or usage).

client-logging.py – Logging utilities used by client and other scripts.

service-utils.py – Utility functions for common service tasks.

initialize.py – Sets up initial database structure and seeds sample data.

usage.py – Core logic for tracking and calculating usage for customers.

__init__.py – Marks src as a Python package.

tests/ – Unit tests for verifying code correctness:

test__client.py – Tests for the client library, including health checks, record usage, and idempotency.

test__crud.py – Tests CRUD operations against the test database.

test__api.py – Tests API endpoints (e.g., POST /usage).

test__simulator.py – Tests simulator functions and data generation.

__init__.py – Marks tests as a Python package.

logs/ – Contains log files generated during script execution:

client.log – Logs from client library actions and API requests.

generator.log – Logs from generator.py script operations.

simulator.log – Logs from simulator.py script operations.

data/ – Data files used for initializing the system:

customer__names.csv – CSV of sample customer names.

customers.json – Sample JSON customer data.

services__list.json – JSON file listing services that customers may consume.

prompts/ – Placeholder folder for future LLM integration (ran out of time).
```
