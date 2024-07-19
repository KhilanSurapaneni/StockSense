# StockSense: AI-Powered Stock Market Analysis and Prediction

## Introduction
**StockSense** is a web application designed to provide users with comprehensive stock market analysis and AI-based predictions. By leveraging historical stock data, users can visualize trends, compare stocks, and receive future price predictions. The application aims to blend powerful data analytics with an intuitive user experience.

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
- **Profile Management:** Users can manage their profile information and view saved stocks.

### Dashboard
- **Overview:** Provides a summary of the stock market's current state, highlighting major indices and trends.
- **Favorite Stocks:** Displays a quick view of the user's favorite stocks.

### Stock Search and Visualization
- **Search:** Users can search for specific stocks by ticker symbol.
- **Historical Data Visualization:** Interactive charts displaying historical prices and volumes using Chart.js.
- **Stock Comparison:** Users can compare the performance of multiple stocks over time.

### AI-Based Predictions
- **Price Predictions:** Users can request AI-based predictions for future stock prices.
- **Visualization:** Predicted prices are overlaid on historical data charts for easy comparison.

### News Integration
- **Financial News:** Displays the latest news related to the user's selected stocks, aggregated from various sources.

## Tech Stack
### Frontend
- **React.js:** Building user interfaces.
- **Axios:** Making HTTP requests to the backend API.
- **Chart.js:** Visualizing stock data through interactive charts.

### Backend
- **Django (Python):** Serving the API and handling business logic.
- **Django REST Framework:** Creating RESTful APIs.
- **Celery:** Task queue for handling asynchronous tasks (e.g., fetching news).

### Database
- **MongoDB:** Storing user data, stock information, and historical data.

### AI and Machine Learning
- **PyTorch:** Fine-tuning a Long Short-Term Memory (LSTM) model for stock price predictions.
- **Pandas/Numpy:** Data manipulation and preprocessing.

## Setup and Installation
### Prerequisites
- Node.js and npm installed
- Python and pip installed
- MongoDB installed and running

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stocksense.git
   cd stocksense/backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Django development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install the required packages:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

## Usage
### Sign Up and Login
- Navigate to the Sign-Up page to create an account.
- Use the Login page to access your account.

### Dashboard
- View the market overview and your favorite stocks.
- Search for specific stocks using the search bar.

### Stock Visualization
- Search for a stock to view its historical data.
- Use interactive charts to analyze trends.

### AI Predictions
- Select a stock and request AI-based predictions.
- View predicted prices overlaid on historical data charts.

### News
- Stay updated with the latest financial news related to your selected stocks.

## Behind the Scenes
### User Authentication
- **Frontend:** React components handle user input and form submission. Axios sends requests to the backend.
- **Backend:** Django handles user authentication using Django REST Framework's authentication system. User data is stored in MongoDB.

### Data Visualization
- **Frontend:** React components fetch data from the backend using Axios. Chart.js renders interactive charts.
- **Backend:** Django serves historical stock data from MongoDB. Endpoints are created using Django REST Framework.

### AI Predictions
- **Frontend:** Users request predictions through React components. Predicted data is displayed on charts.
- **Backend:** Historical data is preprocessed using Pandas and Numpy. Machine learning models are built and trained using PyTorch, specifically fine-tuning a Long Short-Term Memory (LSTM) model for stock price predictions. Predictions are served through API endpoints.
- [**Dataset**](https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs/data)

### News Integration
- **Frontend:** React components display news articles related to selected stocks.
- **Backend:** Celery handles asynchronous tasks to fetch and aggregate news from various sources. Django serves the news data through API endpoints.
