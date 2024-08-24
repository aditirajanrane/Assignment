import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


# Function for loading the csv file
def load_data(file_path):
    return pd.read_csv(file_path)


# Function to calculate KPIs
def calculate_kpis(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year

    # Total Sales per Category
    total_sales_per_category = df.groupby('Category')['TotalSales'].sum().reset_index()

    # Average Order Value per Category
    avg_order_value_per_category = df.groupby('Category').apply(
        lambda x: x['TotalSales'].sum() / len(x)
    ).reset_index(name='AverageOrderValue')

    return total_sales_per_category, avg_order_value_per_category


# Function to create visualizations
def create_visualizations(total_sales_df, avg_order_value_df):
    # Total Sales per Category
    fig1 = px.bar(total_sales_df, x='Category', y='TotalSales', title='Total Sales per Category')

    # Avg Order Value per Category
    fig2 = px.bar(avg_order_value_df, x='Category', y='AverageOrderValue', title='Average Order Value per Category')

    # Saving visualizations to HTML
    fig1.write_html('total_sales_per_category.html')
    fig2.write_html('avg_order_value_per_category.html')

#Converting html documents to png
def html_to_png(html_file, output_file):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    driver.get(f"file://{html_file}")
    time.sleep(2)

    driver.save_screenshot(output_file)
    driver.quit()


# Convert HTML files to PNG
html_to_png('total_sales_per_category.html', 'total_sales_per_category.png')
html_to_png('avg_order_value_per_category.html', 'avg_order_value_per_category.png')


# Function to Generate PDF report
def generate_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="KPI Dashboard", ln=True, align='C')

    # Total Sales per Category
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Total Sales per Category", ln=True)

    # Add image for total sales
    pdf.image('total_sales_per_category.png', x=10, y=pdf.get_y() + 10, w=180)

    # Average Order Value per Category
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Average Order Value per Category", ln=True)

    # Add image for average order value
    pdf.image('avg_order_value_per_category.png', x=10, y=pdf.get_y() + 10, w=180)

    pdf.output("kpi_dashboard.pdf")


# Main function to run the script
def main():
    df = load_data(r"E:\aditi\DS Course\Job assignment\SalesData.csv")
    total_sales_df, avg_order_value_df = calculate_kpis(df)
    create_visualizations(total_sales_df, avg_order_value_df)

    # Convert HTML visualizations to PNG before generating PDF
    html_to_png('total_sales_per_category.html', 'total_sales_per_category.png')
    html_to_png('avg_order_value_per_category.html', 'avg_order_value_per_category.png')

    generate_pdf_report()


if __name__ == "__main__":
    main()