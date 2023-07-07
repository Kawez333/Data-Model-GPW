# Data-Model-GPW

![Nowy projekt (1)](https://github.com/Kawez333/Data-Model-GPW/assets/122210094/a71164be-002c-4c1e-9556-f7445b7a273b)


Ingest - Transform - Load - Visualization

I would like to present my data model project, which briefly ingests data from a website, transforms it, loads it into a data warehouse, and presents it visually. I started working on this project a month ago, and currently, the entire data flow is working correctly. I will continue developing and improving this project. Let me describe step by step how it works:

The whole process starts on a website where the stock prices of Polish companies are listed in a table. As a fan of trading and an active investor, I chose this dataset as a data source.

The data from the website is scraped using a Python script and the BeautifulSoup library. The script is deployed on my local machine. The entire table is scraped and saved to a CSV file, which is then transferred to an Azure Blob Storage container. The data is not cleaned at this stage.

When the file is placed in the container, a platform notification from Blob Storage is sent to Azure Data Factory, triggering a pipeline.

The Azure Data Factory (ADF) pipeline retrieves the file, cleans and transforms the data using a data flow. For example, empty rows are removed, data types are changed, and a timestamp column is added. Then the data is loaded into a table in Snowflake. After that, the file is deleted from the Blob Storage container.

In Snowflake, based on the loaded table, I created several views that prepare the data for visualization in the next step. I select data from the table based on specific parameters and order the data in these views.

The final element is the visualization of the collected data using Power BI dashboards. Power BI connects to Snowflake, retrieves the data, and presents it using charts and matrices. For example, it shows the companies with the highest trading volume, the top 5 most advanced companies, and more.

Creating this model has taught me a lot. I still have many ideas on how to expand and improve this project, such as using Apache Airflow for scheduling, deploying the Python script in Azure Functions or Docker, and using Snowflake streams to track data changes and capture them using CDC (change data capture). The longer I work on this project, the more ideas I have.
