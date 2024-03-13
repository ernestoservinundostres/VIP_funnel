#%%

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest, Filter, FilterExpression
from google.oauth2 import service_account
import pandas as pd
import pygsheets
from datetime import datetime, date, timedelta
import time

# Carga las credenciales de la cuenta de servicio
credentials = service_account.Credentials.from_service_account_file('C:/Users/UNDOSTRES/Documents/GitHub/VIP_funnel/Quickstart-482c000987ec.json')

# Construye el cliente de la API de Google Analytics Data
client = BetaAnalyticsDataClient(credentials=credentials)

cfilt= Filter(
    field_name="streamId",
    string_filter=Filter.StringFilter(value="3862526192")
)

campaign= RunReportRequest(
    property=f"properties/{'276315931'}",
    date_ranges=[DateRange(start_date="2023-01-01", end_date="2024-02-29")],
    dimensions=[Dimension(name="campaignName")],
    metrics=[Metric(name="conversions")],
    dimension_filter=FilterExpression(filter=cfilt)# This is for 'page_view',
)

data_campaigns= []
campaigns = client.run_report(campaign)
for row in campaigns.rows:
    data_campaigns.append({
        'date': row.dimension_values[0].value,
        'operatingSystem': row.dimension_values[1].value,
        'user_engagement': row.metric_values[0].value
    })
df = pd.DataFrame(data_campaigns)

print(df.head())