# StockSense: AI-Powered Stock Market Analysis and Prediction

### In Progress -- Currently Paused Work Due to Other Obligations
Note that some of the functionality is proposed and something for me as the developer to work off of when developing the app. Therefore, it is subject to change.

## Introduction
**StockSense** is an API designed to provide comprehensive stock market analysis and AI-based predictions. By leveraging historical stock data, users can visualize trends, compare stocks, and receive future price predictions. The goal is to blend powerful data analytics with machine learning for stock price forecasting.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Behind the Scenes](#behind-the-scenes)

## Features
### User Authentication
- **Sign Up:** Users can create an account using their email and a password.
- **Login:** Registered users can log in to access personalized features.
- **Profile Management:** Users can manage their profile information and view favorited stocks.

### Stock Search and Visualization
- **Search:** Users can search for specific stocks by ticker symbol.
- **Historical Data:** Provides historical prices and volumes for stocks.
- **Stock Comparison:** Users can compare the performance of multiple stocks over time.

### AI-Based Predictions
- **Price Predictions:** Users can request AI-based predictions for future stock prices.
  
### News Integration
- **Financial News:** Provides the latest news related to selected stocks, aggregated from various sources.

## Tech Stack
### Backend
- **Django (Python):** Serving the API and handling business logic.
- **Django REST Framework:** Creating RESTful APIs.
- **Celery:** Task queue for handling asynchronous tasks (e.g., fetching news).
- **Redis:** Message broker for Celery tasks.

### Database
- **PostgreSQL:** Storing user data, stock information, and historical data. Hosted on railway.app.

### AI and Machine Learning
- **PyTorch:** Fine-tuning a Long Short-Term Memory (LSTM) model for stock price predictions.
- **Pandas/Numpy:** Data manipulation and preprocessing.

## Setup and Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd stocksense
   ```
3. Set up the virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the Django server:
   ```bash
   python manage.py runserver
   ```

## Usage
### Authentication
- Sign up and log in to access personalized stock data and prediction features.

### Stock Search and Visualization
- Search for stocks using the API endpoints to retrieve historical data.

### AI Predictions
- Use the provided API to request stock price predictions based on historical data.

### News
- Retrieve the latest financial news related to a particular stock via the news API.

## Behind the Scenes
### User Authentication
- Django handles user authentication using Django REST Framework's authentication system. User data is stored in PostgreSQL.

### Stock Data and Visualization
- Django serves historical stock data through RESTful API endpoints. The data is stored in PostgreSQL.

### AI Predictions
- Historical data is preprocessed using Pandas and Numpy. Machine learning models are built and trained using PyTorch, specifically fine-tuning a Long Short-Term Memory (LSTM) model for stock price predictions. Predictions are served through API endpoints.
- [**Dataset**](https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs/data)

### News Integration
- Celery handles asynchronous tasks to fetch and aggregate news from various sources. Django serves the news data through API endpoints.
