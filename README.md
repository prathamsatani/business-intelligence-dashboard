# Interactive Business Intelligence Dashboard

## Overview

The **Interactive Business Intelligence Dashboard** is a self-service analytics platform designed to democratize data access for business professionals. It allows users to upload raw datasets (CSV or Excel), automatically cleans and processes the data, and generates interactive visualizations and statistical insights on the fly. This tool bridges the gap between raw data files and actionable intelligence, enabling users to focus on the "why" behind the data rather than the "how" of processing it.

## Features

### 1. Data Upload & Processing
- **File Support**: Upload CSV or Excel (`.xlsx`, `.xls`) files.
- **Automatic Cleaning**: 
  - Removes duplicate columns.
  - Auto-detects and converts date columns.
  - Coerces numeric columns to handle non-numeric characters gracefully.
- **Data Overview**: Displays dataset shape, column names, data types, missing value statistics, and preview of the first/last 5 rows.

### 2. Interactive Visualizations
Powered by **Plotly Express**, the dashboard offers a variety of interactive charts:
- **Time Series Plots**: Visualize trends over time with optional color grouping.
- **Distribution Plots**: Analyze the frequency distribution of numerical variables (histograms).
- **Bar Charts**: Compare categories with aggregated metrics (Sum, Mean, Count, Median).
- **Scatter Plots**: Explore relationships between two numerical variables with optional color coding.

### 3. Automated Insights
Generate statistical insights without writing code:
- **Top/Bottom Performers**: Identify the highest and lowest ranking entities for any metric.
- **Trend Detection**: Analyze seasonal patterns (e.g., best and worst performing months on average).
- **Anomaly Detection**: Automatically detect outliers using Z-score analysis (standard deviation threshold).

### 4. Data Filtering
- Filter the dataset based on specific column values to focus analysis on a subset of data.
- Visualizations and insights update dynamically based on the filtered data.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/prathamsatani/business-intelligence-dashboard.git
   cd business-intelligence-dashboard
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**
   ```bash
   python app.py
   ```

2. **Access the Dashboard:**
   Open your web browser and navigate to the local URL provided in the terminal (usually `http://127.0.0.1:7860`).

3. **Workflow:**
   - **Upload Tab**: Drag and drop your CSV/Excel file. Review the data summary.
   - **Filter Tab**: (Optional) Apply filters to narrow down your dataset.
   - **Visualization Tab**: Select chart types and columns to generate plots.
   - **Insights Tab**: Select columns to generate automated text-based insights.

## Project Structure

```
├── app.py                 # Main application entry point (Gradio UI logic)
├── data_processor.py      # Data loading, cleaning, and summary statistics
├── visualizations.py      # Plotly visualization functions
├── insights.py            # Statistical analysis and insight generation
├── utils.py               # Helper functions
├── requirements.txt       # Python dependencies
├── Final_Project_Report.md # Detailed project report and architecture
└── data/                  # Directory for sample datasets
```

## Dependencies

- **Gradio**: For building the web-based user interface.
- **Pandas**: For high-performance data manipulation and analysis.
- **Plotly**: For creating interactive, publication-quality graphs.
- **Yfinance**: For downloading stock market data (used in data processing utilities).

## Architecture

The system follows a modular architecture:
1.  **Presentation Layer (UI)**: Built with Gradio, handling user interactions and state management.
2.  **Data Processing Layer**: Powered by Pandas for robust data ingestion and cleaning.
3.  **Analysis Layer**: Custom modules for statistical heuristics and anomaly detection.
4.  **Visualization Layer**: Uses Plotly Express for generating dynamic charts.

