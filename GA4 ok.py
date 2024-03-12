

#%%

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest, Filter, FilterExpression
from google.oauth2 import service_account
import pandas as pd
import pygsheets
from datetime import datetime, date, timedelta
import time

# Carga las credenciales de la cuenta de servicio
credentials = service_account.Credentials.from_service_account_file('undostresnew-0a269e925dc5.json')

# Construye el cliente de la API de Google Analytics Data
client = BetaAnalyticsDataClient(credentials=credentials)

# Configura los filtros para considerar los eventos de visita a página, compromiso de usuario y inicio de sesión
page_view_filter = Filter(
    field_name="eventName",
    string_filter=Filter.StringFilter(value="page_view")
)

user_engagement_filter = Filter(
    field_name="eventName",
    string_filter=Filter.StringFilter(value="user_engagement")
)

session_start_filter = Filter(
    field_name="eventName",
    string_filter=Filter.StringFilter(value="session_start")
)

# Configura la solicitud de informe para page_views
request_page_view = RunReportRequest(
    property=f"properties/{'276315931'}",
    date_ranges=[DateRange(start_date="2023-01-01", end_date="2024-02-29")],
    dimensions=[Dimension(name="date"), Dimension(name="operatingSystem")],
    metrics=[Metric(name="eventCount")],  # This is for 'page_view'
    dimension_filter=FilterExpression(filter=page_view_filter)
)

# Configura la solicitud de informe para user_engagement
request_user_engagement = RunReportRequest(
    property=f"properties/{'276315931'}",
    date_ranges=[DateRange(start_date="2023-01-01", end_date="2024-02-29")],
    dimensions=[Dimension(name="date"), Dimension(name="operatingSystem")],
    metrics=[Metric(name="eventCount")],  # This is for 'user_engagement'
    dimension_filter=FilterExpression(filter=user_engagement_filter)
)

# Configura la solicitud de informe para session_start
request_session_start = RunReportRequest(
    property=f"properties/{'276315931'}",
    date_ranges=[DateRange(start_date="2023-01-01", end_date="2024-02-29")],
    dimensions=[Dimension(name="date"), Dimension(name="operatingSystem")],
    metrics=[Metric(name="eventCount")],  # This is for 'session_start'
    dimension_filter=FilterExpression(filter=session_start_filter)
)

# Inicializa tres listas vacías para almacenar los datos
data_page_view = []
data_user_engagement = []
data_session_start = []

# Ejecuta la solicitud de informe para page_views y guarda las filas en la lista de datos
response_page_view = client.run_report(request_page_view)
for row in response_page_view.rows:
    data_page_view.append({
        'date': row.dimension_values[0].value,
        'operatingSystem': row.dimension_values[1].value, 
        'page_view': row.metric_values[0].value
    })

# Ejecuta la solicitud de informe para user_engagement y guarda las filas en la lista de datos
response_user_engagement = client.run_report(request_user_engagement)
for row in response_user_engagement.rows:
    data_user_engagement.append({
        'date': row.dimension_values[0].value,
        'operatingSystem': row.dimension_values[1].value, 
        'user_engagement': row.metric_values[0].value
    })

# Ejecuta la solicitud de informe para session_start y guarda las filas en la lista de datos
response_session_start = client.run_report(request_session_start)
for row in response_session_start.rows:
    data_session_start.append({
        'date': row.dimension_values[0].value,
        'operatingSystem': row.dimension_values[1].value, 
        'session_start': row.metric_values[0].value
    })

# Convierte las listas de datos en DataFrames
df_page_view = pd.DataFrame(data_page_view)
df_user_engagement = pd.DataFrame(data_user_engagement)
df_session_start = pd.DataFrame(data_session_start)

# Combina los tres DataFrames en uno solo, haciendo un merge en las columnas 'date' y 'operatingSystem'
df = pd.merge(df_page_view, df_user_engagement, on=['date', 'operatingSystem'], how='outer')
df = pd.merge(df, df_session_start, on=['date', 'operatingSystem'], how='outer')

# Ordena el DataFrame por las columnas 'date' y 'operatingSystem' en orden descendente
df = df.sort_values(by=['date', 'operatingSystem'], ascending=[False, True])

df.head(50)

# Agregar yearmonth y formatear la fecha
df['date'] = pd.to_datetime(df['date'])
df['yearmonth'] = df['date'].dt.strftime('%Y%m')
df['yearmonth'] = df['yearmonth'].astype(int)
df = df[['yearmonth', 'date', 'operatingSystem','page_view', 'user_engagement', 'session_start']]


#------ ----- ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ -----
print('------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------')
print('Open Google Sheet File & Paste Information.')
start_time = time.time()
print('')

gc = pygsheets.authorize(service_file = r'CredMc.json')
sh = gc.open_by_key('1OK0ungpds3_TLRy-XUWsEk7iGAIhRkZq3QX_8M8xZr4')
wks = sh.worksheet('id', 938196078)
wks.clear() #Borrar contenido del sheet para pegar nuevo contenido
wks.set_dataframe(df,start=(1,1), extend=True) #El extend=True aumenta automáticamente el número de filas y columnas que se requiere



# %%
