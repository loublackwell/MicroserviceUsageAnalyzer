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
    
