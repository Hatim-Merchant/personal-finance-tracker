Personal Finance Tracker

A backend application for tracking personal income, expenses, budgets, and financial summaries.
Built as an end-to-end software engineering project to practice backend development, database management, API design, containerization, and cloud deployment.

Features

* Add and manage income/expense transactions
* Store transaction data using SQLite
* Search and filter transactions by category, amount, type, and date
* Generate monthly and overall financial summaries
* Export transaction history as CSV
* REST API built with FastAPI
* Dockerized application for portable deployment
* Deployed on AWS Elastic Beanstalk

**Run Locally**
pip install -r requirements.txt
uvicorn src.api:app --reload

**Open**
http://localhost:8000/docs

**Docker**
docker build -t finance-tracker .
docker run -p 8000:8000 finance-tracker

What I Learned

Through this project I gained hands-on experience with:

* REST API development
* SQL and database design
* Docker containerization
* AWS cloud deployment
* Input validation and error handling
* Backend architecture and modular code design
* Debugging production and environment issues    
