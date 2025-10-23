import pandas as pd #Para manipulación de datos
import plotly.express as px #Para Graficación
import plotly.graph_objects as go #Para Graficación
from dash import Dash, dcc, html, Input, Output #Para crear la aplicación web
import dash_bootstrap_components as dbc #Para estilos y componentes de Bootstrap
from datetime import datetime #Para manejo de fechas
import os #Para manejo de rutas de archivos

def cargar_datos():
    #Rutas de los archivos
    ruta_local_excel = r'D:\Analisis producción de gas 2025\Bases_produccion_crudo/produccion_crudo_anual.xlsx'

	#Rutas para producción
    ruta_prod_excel = 'produccion_crudo_anual.xlsx'
    
	#Detectar si estamos en local o en producción
    if os.path.exists(ruta_local_excel):
        ruta_excel = ruta_local_excel
        print("Cargando datos desde ruta local.")
    else:
        ruta_excel = ruta_prod_excel
        print("Cargando datos desde ruta de producción.")
        
    try:
        # Cargar datos principales de una sola hoja
        df = pd.read_excel(ruta_excel, sheet_name='Serie_Anual')
        df.columns = df.columns.str.strip()
        print(f"Datos cargados exitosamente desde: {ruta_excel}")
        return df
    except FileNotFoundError as e:
        print(f"Error: No se encontraron los archivos Excel: {e}")
        print("Contacta al administrador para configurar los archivos de datos")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error inesperado al cargar datos: {e}")
        return pd.DataFrame()

#Cargar datos
df = cargar_datos()
df['Año'] = pd.to_numeric(df['Año'], errors='coerce')

# Configuración de colores y estilo - KuenKa Branding
colores = ['#00a693', '#008b7a', '#006b5d', '#004d40', '#66c2b3', '#4db8a6', '#33ad99', '#1a9b8c', '#80ccc0', '#99d6cc', '#b3e0d9']
color_primario = '#00a693'  # Verde KuenKa principal
color_secundario = '#ffc107'  # Amarillo KuenKa
color_texto = '#2c3e50'  # Azul oscuro para texto
color_fondo = '#f8f9fa'  # Fondo claro

# Inicializar app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "KuenKa - Crudo Production Executive Dashboard"
server = app.server

# Layout principal
app.layout = dbc.Container([
    # Encabezado
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.H1("KuenKa Energy Research", 
                           style={'color': color_primario, 'fontWeight': 'bold', 'fontSize': '42px', 'marginBottom': '0'}),
                    html.H3("Crudo Production Executive Dashboard", 
                           style={'color': color_texto, 'fontWeight': '300', 'fontSize': '24px', 'marginTop': '0'}),

                ], className="text-center")
            ], style={
                'background': f'linear-gradient(135deg, {color_fondo} 0%, #ffffff 100%)',
                'padding': '30px',
                'borderRadius': '15px',
                'boxShadow': '0 8px 32px rgba(0, 166, 147, 0.1)',
                'border': f'1px solid {color_primario}20',
                'marginBottom': '30px'
            })
        ], width=12)
    ]),
    
    # Filtro de año
    dbc.Row([
        dbc.Col([
            html.Label("Filter by Year:", style={'fontWeight': 'bold', 'color': color_texto, 'fontSize': '18px', 'marginBottom': '15px'}),
            dcc.RangeSlider(
                id='year-slider',
                min=int(df['Año'].min()),
                max=int(df['Año'].max()),
                value=[int(df['Año'].min()), int(df['Año'].max())],
                marks={year: {'label': str(year), 'style': {'color': color_texto, 'fontSize': '14px', 'fontWeight': '500'}} 
                       for year in range(int(df['Año'].min()), int(df['Año'].max()) + 1)},
                step=1,
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], width=12, style={
            'padding': '20px 30px', 
            'backgroundColor': 'white', 
            'borderRadius': '10px',
            'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.08)',
            'marginBottom': '20px'
        })
    ], className="mb-4"),
    
    # Pestañas
    dcc.Tabs(id="tabs", value="tab-general", 
             style={'height': '60px', 'marginBottom': '20px'},
             children=[
        dcc.Tab(label="General Analysis", value="tab-general", 
                style={
                    'backgroundColor': 'white', 'color': color_texto, 'padding': '15px 30px', 
                    'fontSize': '16px', 'fontWeight': '600', 'border': f'2px solid {color_primario}20',
                    'borderRadius': '8px 8px 0 0', 'marginRight': '5px'
                },
                selected_style={
                    'backgroundColor': color_primario, 'color': 'white', 'padding': '15px 30px',
                    'fontSize': '16px', 'fontWeight': '600', 'border': f'2px solid {color_primario}',
                    'borderRadius': '8px 8px 0 0', 'marginRight': '5px'
                }),
        dcc.Tab(label="Production by Field", value="tab-campo",
                style={
                    'backgroundColor': 'white', 'color': color_texto, 'padding': '15px 30px',
                    'fontSize': '16px', 'fontWeight': '600', 'border': f'2px solid {color_primario}20',
                    'borderRadius': '8px 8px 0 0', 'marginRight': '5px'
                },
                selected_style={
                    'backgroundColor': color_primario, 'color': 'white', 'padding': '15px 30px',
                    'fontSize': '16px', 'fontWeight': '600', 'border': f'2px solid {color_primario}',
                    'borderRadius': '8px 8px 0 0', 'marginRight': '5px'
                }),
        dcc.Tab(label="Production by Basin", value="tab-cuenca",
                style={
                    'backgroundColor': 'white', 'color': color_texto, 'padding': '15px 30px',
                    'fontSize': '16px', 'fontWeight': '600', 'border': f'2px solid {color_primario}20',
                    'borderRadius': '8px 8px 0 0', 'marginRight': '5px'
                },
                selected_style={
                    'backgroundColor': color_primario, 'color': 'white', 'padding': '15px 30px',
                    'fontSize': '16px', 'fontWeight': '600', 'border': f'2px solid {color_primario}',
                    'borderRadius': '8px 8px 0 0', 'marginRight': '5px'
                }),
        dcc.Tab(label="Production by Department", value="tab-departamento",
                style={
                    'backgroundColor': 'white', 'color': color_texto, 'padding': '15px 30px',
                    'fontSize': '16px', 'fontWeight': '600', 'border': f'2px solid {color_primario}20',
                    'borderRadius': '8px 8px 0 0'
                },
                selected_style={
                    'backgroundColor': color_primario, 'color': 'white', 'padding': '15px 30px',
                    'fontSize': '16px', 'fontWeight': '600', 'border': f'2px solid {color_primario}',
                    'borderRadius': '8px 8px 0 0'
                })
    ]),
    
    # Contenido de las pestañas
    html.Div(id="tabs-content", style={'padding': '20px', 'borderRadius': '10px', 'backgroundColor': 'white', 'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.1)'})
])

# Callback para actualizar el contenido de las pestañas
@app.callback(
    Output("tabs-content", "children"),
    [Input("tabs", "value"),
     Input("year-slider", "value")]
)
def update_tab_content(tab_name, year_range):
    # Filtrar datos por rango de años
    dff = df[(df['Año'] >= year_range[0]) & (df['Año'] <= year_range[1])]
    
    if tab_name == "tab-general":
        kpi_content = crear_tab_general(dff)
   		 # Gráfica 1: Evolución anual de la producción de crudo (línea)
        df_anual = dff.groupby('Año', as_index=False)['Produccion crudo'].sum()
        fig_evolucion = go.Figure()
        fig_evolucion.add_trace(go.Scatter(
            x=df_anual['Año'],
            y=df_anual['Produccion crudo'],
            mode='lines+markers',
            line=dict(color=color_primario, width=4, shape='spline'),
            marker=dict(size=10, color=color_secundario, symbol='diamond'),
            name='Producción total',
            hovertemplate='<b>Año</b>: %{x}<br><b>Producción</b>: %{y:,.0f} barriles',
        ))
        fig_evolucion.update_layout(
            yaxis_title='Total Production (barrels)',
            xaxis_title='Year',
            template='plotly_white',
            hovermode='x unified',
            showlegend=False,
            margin=dict(t=30, b=40, l=40, r=20),
            plot_bgcolor=color_fondo,
            font=dict(family='Montserrat, Arial', size=16, color=color_texto)
        )
        grafica_lineas = dcc.Graph(
            figure=fig_evolucion,
            style={'height': '420px'}
        )
    	# Gráfica 2: Variación porcentual anual de la producción 
        df_anual['Variación %'] = df_anual['Produccion crudo'].pct_change() * 100
        fig_var = go.Figure()
        color_positivo = color_primario
        color_negativo = '#004d40' 
        colores_barra = [color_positivo if v >= 0 else color_negativo for v in df_anual['Variación %'].fillna(0)]
        fig_var.add_trace(go.Bar(
            x=df_anual['Año'],
            y=df_anual['Variación %'],
            marker_color=colores_barra,
            name='Variación %',
            text=[f"{v:+.2f}%" if not pd.isna(v) else '' for v in df_anual['Variación %']],
            textposition='outside',
            opacity=0.85
        ))
        fig_var.add_trace(go.Scatter(
            x=df_anual['Año'],
            y=df_anual['Variación %'],
            mode='lines+markers',
            name='Tendencia',
            line=dict(color=color_secundario, width=3, dash='dash'),
            marker=dict(size=8, color=color_secundario)
        ))
        fig_var.update_layout(
            yaxis_title='Variation (%)',
            xaxis_title='Year',
            template='plotly_white',
            hovermode='x unified',
            legend=dict(orientation='h', yanchor='top', y=-0.2, xanchor='center', x=0.5),
            margin=dict(t=30, b=40, l=40, r=20),
            bargap=0.25,
            title=None
        )
        grafica_variacion = dcc.Graph(
            figure=fig_var,
            style={'height': '400px'}
        )
        return html.Div([
            *kpi_content,
            html.Div([
                html.H4("Annual crude production evolution", style={'color': color_primario, 'fontWeight': 'bold', 'marginTop': '30px', 'textAlign': 'center'}),
                grafica_lineas
            ], style={'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 4px 12px rgba(0, 166, 147, 0.08)', 'padding': '20px', 'marginTop': '10px'}),
            html.Div([
                html.H4("Annual percentage variation in production", style={'color': color_primario, 'fontWeight': 'bold', 'marginTop': '30px', 'textAlign': 'center'}),
                grafica_variacion
            ], style={'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 4px 12px rgba(0, 166, 147, 0.08)', 'padding': '20px', 'marginTop': '10px'})
        ])

        fig_evolucion.update_layout(
            yaxis_title='Producción total (barriles)',
            xaxis_title='Año',
            template='plotly_white',
            hovermode='x unified',
            showlegend=False,
            margin=dict(t=30, b=40, l=40, r=20),
            plot_bgcolor=color_fondo,
            font=dict(family='Montserrat, Arial', size=16, color=color_texto)
        )
        grafica_lineas = dcc.Graph(
            figure=fig_evolucion,
            style={'height': '420px'}
        )
        # Gráfica 2: Variación porcentual anual de la producción 
        df_anual['Variación %'] = df_anual['Produccion crudo'].pct_change() * 100
        fig_var = go.Figure()
    	# Barras para variación positiva y negativa 
        color_positivo = color_primario
        color_negativo = '#004d40'  
        colores_barra = [color_positivo if v >= 0 else color_negativo for v in df_anual['Variación %'].fillna(0)]
        fig_var.add_trace(go.Bar(
            x=df_anual['Año'],
            y=df_anual['Variación %'],
            marker_color=colores_barra,
            name='Variación %',
            text=[f"{v:+.2f}%" if not pd.isna(v) else '' for v in df_anual['Variación %']],
            textposition='outside',
            opacity=0.85
        ))
    	# Línea para tendencia de variación 
        fig_var.add_trace(go.Scatter(
            x=df_anual['Año'],
            y=df_anual['Variación %'],
            mode='lines+markers',
            name='Tendencia',
            line=dict(color=color_secundario, width=3, dash='dash'),
            marker=dict(size=8, color=color_secundario)
        ))
        fig_var.update_layout(
            yaxis_title='Variación (%)',
            xaxis_title='Año',
            template='plotly_white',
            hovermode='x unified',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            margin=dict(t=30, b=40, l=40, r=20),
            bargap=0.25,
            title=None
        )
        grafica_variacion = dcc.Graph(
            figure=fig_var,
            style={'height': '400px'}
        )
        return html.Div([
            *kpi_content,
            html.Div([
                html.H4("Annual crude production evolution", style={'color': color_primario, 'fontWeight': 'bold', 'marginTop': '30px'}),
                grafica_lineas
            ], style={'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 4px 12px rgba(0, 166, 147, 0.08)', 'padding': '20px', 'marginTop': '10px'}),
            html.Div([
                html.H4("Annual percentage variation in production", style={'color': color_primario, 'fontWeight': 'bold', 'marginTop': '30px'}),
                grafica_variacion
            ], style={'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 4px 12px rgba(0, 166, 147, 0.08)', 'padding': '20px', 'marginTop': '10px'})
        ])
    elif tab_name == "tab-campo":
    	# KPIs para la pestaña de Campo
        if not dff.empty:
            df_field = dff.groupby('Campo', as_index=False)['Produccion crudo'].sum()
            best_field_row = df_field.loc[df_field['Produccion crudo'].idxmax()]
            best_field = best_field_row['Campo']
            best_field_prod = best_field_row['Produccion crudo']
            num_fields = df_field['Campo'].nunique()
        else:
            best_field = 'N/A'
            best_field_prod = 0
            num_fields = 0
        kpi_field = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Best Field", className="card-title text-center mb-2", style={'color': color_primario, 'fontWeight': '700'}),
                        html.H2(f"{best_field}", className="text-center", style={'fontSize': '28px', 'fontWeight': 'bold', 'color': color_texto}),
                        html.P(f"Total: {best_field_prod:,.0f} barrels", className="text-center text-muted", style={'fontSize': '14px'})
                    ], style={'padding': '20px'})
                ], style={'height': '170px', 'borderRadius': '15px', 'boxShadow': '0 8px 32px rgba(0, 166, 147, 0.10)', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'})
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Active Fields", className="card-title text-center mb-2", style={'color': color_secundario, 'fontWeight': '700'}),
                        html.H2(f"{num_fields}", className="text-center", style={'fontSize': '28px', 'fontWeight': 'bold', 'color': color_texto}),
                        html.P("Number of fields in selected period", className="text-center text-muted", style={'fontSize': '14px'})
                    ], style={'padding': '20px'})
                ], style={'height': '170px', 'borderRadius': '15px', 'boxShadow': '0 8px 32px rgba(255, 193, 7, 0.10)', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'})
            ], width=6)
        ], className="mb-4", style={'marginLeft': '10px', 'marginRight': '10px'})

    	# Evolución de la producción anual para los 5 campos principales
        df_field_total = dff.groupby('Campo', as_index=False)['Produccion crudo'].sum()
        top5_fields = df_field_total.sort_values('Produccion crudo', ascending=False).head(5)['Campo'].tolist()
        df_top5 = dff[dff['Campo'].isin(top5_fields)]
        df_evol5 = df_top5.groupby(['Año', 'Campo'], as_index=False)['Produccion crudo'].sum()
        fig_evol5 = go.Figure()
        color_palette5 = colores[:5] if len(top5_fields) >= 5 else colores[:len(top5_fields)]
        for i, campo in enumerate(top5_fields):
            df_campo = df_evol5[df_evol5['Campo'] == campo]
            fig_evol5.add_trace(go.Scatter(
                x=df_campo['Año'],
                y=df_campo['Produccion crudo'],
                mode='lines+markers',
                name=campo,
                line=dict(color=color_palette5[i], width=3, shape='spline'),
                marker=dict(size=8, color=color_palette5[i]),
                hovertemplate=f'<b>Field</b>: {campo}<br><b>Year</b>: %{{x}}<br><b>Production</b>: %{{y:,.0f}} barrels',
            ))
        fig_evol5.update_layout(
            yaxis_title='Annual Production (barrels)',
            xaxis_title='Year',
            template='plotly_white',
            hovermode='x unified',
            margin=dict(t=30, b=40, l=40, r=20),
            font=dict(family='Montserrat, Arial', size=16, color=color_texto),
            legend=dict(orientation='h', yanchor='top', y=-0.2, xanchor='center', x=0.5),
            showlegend=True
        )
        grafica_evol5 = dcc.Graph(
            figure=fig_evol5,
            style={'height': '420px'}
        )

    	# Gráficas individuales de líneas para la producción anual de los 10 campos principales (1 por gráfica, 2 por fila)
        top10_fields = df_field_total.sort_values('Produccion crudo', ascending=False).head(10)['Campo'].tolist()
        df_top10 = dff[dff['Campo'].isin(top10_fields)]
        df_evol10 = df_top10.groupby(['Año', 'Campo'], as_index=False)['Produccion crudo'].sum()
        color_palette10 = colores[:10] if len(top10_fields) >= 10 else colores[:len(top10_fields)]
        line_charts = []
        for i, campo in enumerate(top10_fields):
            df_campo = df_evol10[df_evol10['Campo'] == campo]
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_campo['Año'],
                y=df_campo['Produccion crudo'],
                mode='lines+markers',
                name=campo,
                line=dict(color=color_palette10[i], width=3, shape='spline'),
                marker=dict(size=8, color=color_palette10[i]),
                hovertemplate=f'<b>Field</b>: {campo}<br><b>Year</b>: %{{x}}<br><b>Production</b>: %{{y:,.0f}} barrels',
            ))
            fig.update_layout(
                yaxis_title='Annual Production (barrels)',
                xaxis_title='Year',
                template='plotly_white',
                hovermode='x unified',
                margin=dict(t=50, b=30, l=30, r=10),
                font=dict(family='Montserrat, Arial', size=11, color=color_texto),
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                showlegend=False,
                title=dict(text=f"Annual Production: {campo}", font=dict(size=13), x=0.5, y=0.95),
                yaxis=dict(range=[0, None], tickformat=",.0f")
            )
            line_charts.append(dbc.Col(
                dcc.Graph(figure=fig, style={'height': '300px'}), width=6, style={'marginBottom': '18px'}
            ))
    	# Organizar gráficas en una cuadrícula (2 por fila)
        grid_rows = []
        for i in range(0, len(line_charts), 2):
            grid_rows.append(dbc.Row(line_charts[i:i+2], className="mb-2"))
        return html.Div([
            kpi_field,
            html.Div([
                html.H4("Annual Production Evolution of Top 5 Fields", style={'color': color_primario, 'fontWeight': 'bold', 'marginTop': '30px', 'textAlign': 'center'}),
                grafica_evol5
            ], style={'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 4px 12px rgba(0, 166, 147, 0.08)', 'padding': '20px', 'marginTop': '10px'}),
            html.Div([
                html.H4("Annual Production of Top 10 Fields (Individual Line Charts)", style={'color': color_primario, 'fontWeight': 'bold', 'marginTop': '30px', 'textAlign': 'center'}),
                *grid_rows
            ], style={'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 4px 12px rgba(0, 166, 147, 0.08)', 'padding': '20px', 'marginTop': '10px'})
        ])
    elif tab_name == "tab-cuenca":
    	# KPIs para la pestaña de Cuenca
        if not dff.empty:
            df_basin = dff.groupby('Cuenca', as_index=False)['Produccion crudo'].sum()
            best_basin_row = df_basin.loc[df_basin['Produccion crudo'].idxmax()]
            best_basin = best_basin_row['Cuenca']
            best_basin_prod = best_basin_row['Produccion crudo']
            num_basins = df_basin['Cuenca'].nunique()
            total_prod = df_basin['Produccion crudo'].sum()
            avg_annual_prod = dff.groupby(['Año', 'Cuenca'], as_index=False)['Produccion crudo'].sum().groupby('Cuenca')['Produccion crudo'].mean().mean()
        else:
            best_basin = 'N/A'
            best_basin_prod = 0
            num_basins = 0
            total_prod = 0
            avg_annual_prod = 0
        kpi_basin = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Best Basin", className="card-title text-center mb-2", style={'color': color_primario, 'fontWeight': '700'}),
                        html.H2(f"{best_basin}", className="text-center", style={'fontSize': '28px', 'fontWeight': 'bold', 'color': color_texto}),
                        html.P(f"Total: {best_basin_prod:,.0f} barrels", className="text-center text-muted", style={'fontSize': '14px'})
                    ], style={'padding': '20px'})
                ], style={'height': '170px', 'borderRadius': '15px', 'boxShadow': '0 8px 32px rgba(0, 166, 147, 0.10)', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'})
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Active Basins", className="card-title text-center mb-2", style={'color': color_secundario, 'fontWeight': '700'}),
                        html.H2(f"{num_basins}", className="text-center", style={'fontSize': '28px', 'fontWeight': 'bold', 'color': color_texto}),
                        html.P("Number of basins in selected period", className="text-center text-muted", style={'fontSize': '14px'})
                    ], style={'padding': '20px'})
                ], style={'height': '170px', 'borderRadius': '15px', 'boxShadow': '0 8px 32px rgba(255, 193, 7, 0.10)', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'})
            ], width=6)
        ], className="mb-4", style={'marginLeft': '10px', 'marginRight': '10px'})

    	# Evolución de la producción anual para las 5 cuencas principales
        df_basin_total = dff.groupby('Cuenca', as_index=False)['Produccion crudo'].sum()
        top5_basins = df_basin_total.sort_values('Produccion crudo', ascending=False).head(5)['Cuenca'].tolist()
        df_top5 = dff[dff['Cuenca'].isin(top5_basins)]
        df_evol5 = df_top5.groupby(['Año', 'Cuenca'], as_index=False)['Produccion crudo'].sum()
        fig_evol5 = go.Figure()
        color_palette5 = colores[:5] if len(top5_basins) >= 5 else colores[:len(top5_basins)]
        for i, cuenca in enumerate(top5_basins):
            df_cuenca = df_evol5[df_evol5['Cuenca'] == cuenca]
            fig_evol5.add_trace(go.Scatter(
                x=df_cuenca['Año'],
                y=df_cuenca['Produccion crudo'],
                mode='lines+markers',
                name=cuenca,
                line=dict(color=color_palette5[i], width=3, shape='spline'),
                marker=dict(size=8, color=color_palette5[i]),
                hovertemplate=f'<b>Basin</b>: {cuenca}<br><b>Year</b>: %{{x}}<br><b>Production</b>: %{{y:,.0f}} barrels',
            ))
        fig_evol5.update_layout(
            yaxis_title='Annual Production (barrels)',
            xaxis_title='Year',
            template='plotly_white',
            hovermode='x unified',
            margin=dict(t=30, b=40, l=40, r=20),
            font=dict(family='Montserrat, Arial', size=16, color=color_texto),
            legend=dict(orientation='h', yanchor='top', y=-0.2, xanchor='center', x=0.5),
            showlegend=True
        )
        grafica_evol5 = dcc.Graph(
            figure=fig_evol5,
            style={'height': '420px'}
        )

    	# Gráficas individuales de líneas para la producción anual de todas las cuencas (1 por gráfica, 2 por fila)
        all_basins = df_basin_total.sort_values('Produccion crudo', ascending=False)['Cuenca'].tolist()
        df_all = dff[dff['Cuenca'].isin(all_basins)]
        df_evol_all = df_all.groupby(['Año', 'Cuenca'], as_index=False)['Produccion crudo'].sum()
        color_palette_all = colores * ((len(all_basins) // len(colores)) + 1)
        line_charts = []
        for i, cuenca in enumerate(all_basins):
            df_cuenca = df_evol_all[df_evol_all['Cuenca'] == cuenca]
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_cuenca['Año'],
                y=df_cuenca['Produccion crudo'],
                mode='lines+markers',
                name=cuenca,
                line=dict(color=color_palette_all[i], width=3, shape='spline'),
                marker=dict(size=8, color=color_palette_all[i]),
                hovertemplate=f'<b>Basin</b>: {cuenca}<br><b>Year</b>: %{{x}}<br><b>Production</b>: %{{y:,.0f}} barrels',
            ))
            fig.update_layout(
                yaxis_title='Annual Production (barrels)',
                xaxis_title='Year',
                template='plotly_white',
                hovermode='x unified',
                margin=dict(t=50, b=30, l=30, r=10),
                font=dict(family='Montserrat, Arial', size=11, color=color_texto),
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                showlegend=False,
                title=dict(text=f"Annual Production: {cuenca}", font=dict(size=13), x=0.5, y=0.95),
                yaxis=dict(range=[0, None], tickformat=",.0f"),
                xaxis=dict(tickmode='array', tickvals=list(df_cuenca['Año'].astype(int)), tickformat='d')
            )
            line_charts.append(dbc.Col(
                dcc.Graph(figure=fig, style={'height': '300px'}), width=6, style={'marginBottom': '18px'}
            ))
    	# Organizar gráficas en una cuadrícula (2 por fila)
        grid_rows = []
        for i in range(0, len(line_charts), 2):
            grid_rows.append(dbc.Row(line_charts[i:i+2], className="mb-2"))
        return html.Div([
            kpi_basin,
            html.Div([
                html.H4("Annual Production Evolution of Top 5 Basins", style={'color': color_primario, 'fontWeight': 'bold', 'marginTop': '30px', 'textAlign': 'center'}),
                grafica_evol5
            ], style={'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 4px 12px rgba(0, 166, 147, 0.08)', 'padding': '20px', 'marginTop': '10px'}),
            html.Div([
                html.H4("Annual Production of All Basins (Individual Line Charts)", style={'color': color_primario, 'fontWeight': 'bold', 'marginTop': '30px', 'textAlign': 'center'}),
                *grid_rows
            ], style={'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 4px 12px rgba(0, 166, 147, 0.08)', 'padding': '20px', 'marginTop': '10px'})
        ])
    elif tab_name == "tab-departamento":
    	# KPIs para la pestaña de Departamento
        if not dff.empty:
            df_dept = dff.groupby('Departamento', as_index=False)['Produccion crudo'].sum()
            best_dept_row = df_dept.loc[df_dept['Produccion crudo'].idxmax()]
            best_dept = best_dept_row['Departamento']
            best_dept_prod = best_dept_row['Produccion crudo']
            num_depts = df_dept['Departamento'].nunique()
        else:
            best_dept = 'N/A'
            best_dept_prod = 0
            num_depts = 0
        kpi_dept = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Best Department", className="card-title text-center mb-2", style={'color': color_primario, 'fontWeight': '700'}),
                        html.H2(f"{best_dept}", className="text-center", style={'fontSize': '28px', 'fontWeight': 'bold', 'color': color_texto}),
                        html.P(f"Total: {best_dept_prod:,.0f} barrels", className="text-center text-muted", style={'fontSize': '14px'})
                    ], style={'padding': '20px'})
                ], style={'height': '170px', 'borderRadius': '15px', 'boxShadow': '0 8px 32px rgba(0, 166, 147, 0.10)', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'})
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Active Departments", className="card-title text-center mb-2", style={'color': color_secundario, 'fontWeight': '700'}),
                        html.H2(f"{num_depts}", className="text-center", style={'fontSize': '28px', 'fontWeight': 'bold', 'color': color_texto}),
                        html.P("Number of departments in selected period", className="text-center text-muted", style={'fontSize': '14px'})
                    ], style={'padding': '20px'})
                ], style={'height': '170px', 'borderRadius': '15px', 'boxShadow': '0 8px 32px rgba(255, 193, 7, 0.10)', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'})
            ], width=6)
        ], className="mb-4", style={'marginLeft': '10px', 'marginRight': '10px'})

    	# Mapa de burbujas (scatter_mapbox) para la producción por departamento
        coords = {
            'ARAUCA': {'lat': 7.0889, 'lon': -70.7591},
            'BOYACA': {'lat': 5.4544, 'lon': -73.3624},
            'CASANARE': {'lat': 5.3356, 'lon': -72.4056},
            'CESAR': {'lat': 10.4636, 'lon': -73.2532},
            'CUNDINAMARCA': {'lat': 4.7110, 'lon': -74.0721},
            'HUILA': {'lat': 2.9273, 'lon': -75.2819},
            'LA GUAJIRA': {'lat': 11.5444, 'lon': -72.9072},
            'META': {'lat': 4.1420, 'lon': -73.6266},
            'PUTUMAYO': {'lat': 0.5136, 'lon': -76.3567},
            'SANTANDER': {'lat': 7.1193, 'lon': -73.1227},
            'TOLIMA': {'lat': 4.4389, 'lon': -75.2322},
            'NORTE DE SANTANDER': {'lat': 7.8939, 'lon': -72.5078},
            'ANTIOQUIA': {'lat': 6.2442, 'lon': -75.5812},
            'CORDOBA': {'lat': 8.7479, 'lon': -75.8814},
            'MAGDALENA': {'lat': 11.2408, 'lon': -74.1990},
            'BOLIVAR': {'lat': 10.3910, 'lon': -75.4794},
            'VALLE DEL CAUCA': {'lat': 3.4516, 'lon': -76.5320},
            'CAUCA': {'lat': 2.4418, 'lon': -76.6063},
            'NARIÑO': {'lat': 1.2136, 'lon': -77.2811},
            'CHOCO': {'lat': 5.6837, 'lon': -76.6581}
        }
        dept_map_data = []
        for _, row in dff.groupby('Departamento')['Produccion crudo'].sum().reset_index().iterrows():
            dept = row['Departamento']
            prod = row['Produccion crudo']
            lat = coords.get(dept, {'lat': 4.5, 'lon': -74.0})['lat']
            lon = coords.get(dept, {'lat': 4.5, 'lon': -74.0})['lon']
            dept_map_data.append({'Departamento': dept, 'Produccion crudo': prod, 'lat': lat, 'lon': lon})
        df_map = pd.DataFrame(dept_map_data)
        fig_map = px.scatter_mapbox(
            df_map,
            lat='lat',
            lon='lon',
            size='Produccion crudo',
            color='Produccion crudo',
            hover_name='Departamento',
            hover_data={'Produccion crudo':':,.0f'},
            color_continuous_scale=colores,
            size_max=60,
            zoom=5,
            center={'lat': 4.5, 'lon': -74.0},
            title='Geographic Distribution - Crude Production by Department',
            mapbox_style='open-street-map'
        )
        fig_map.update_layout(
            font=dict(family='Montserrat, Arial', size=14, color=color_texto),
            title_font=dict(size=18, color=color_texto, family='Montserrat, Arial'),
            height=520,
            showlegend=False,
            margin=dict(t=60, b=40, l=40, r=40),
            coloraxis_colorbar=dict(title="Production Volume", tickformat=",.0f")
        )
        grafica_map = dcc.Graph(
            figure=fig_map,
            style={'height': '520px'}
        )
    	# Gráfica de líneas - Evolución anual para los 5 departamentos principales
        df_dept_total = dff.groupby('Departamento', as_index=False)['Produccion crudo'].sum()
        df_dept_total = df_dept_total.sort_values('Produccion crudo', ascending=False)
        top5_depts = df_dept_total.head(5)['Departamento'].tolist()
        df_top5 = dff[dff['Departamento'].isin(top5_depts)]
        df_evol5 = df_top5.groupby(['Año', 'Departamento'], as_index=False)['Produccion crudo'].sum()
        fig_evol5 = go.Figure()
        color_palette5 = colores[:5] if len(top5_depts) >= 5 else colores[:len(top5_depts)]
        for i, dept in enumerate(top5_depts):
            df_dept = df_evol5[df_evol5['Departamento'] == dept]
            fig_evol5.add_trace(go.Scatter(
                x=df_dept['Año'],
                y=df_dept['Produccion crudo'],
                mode='lines+markers',
                name=dept,
                line=dict(color=color_palette5[i], width=3, shape='spline'),
                marker=dict(size=8, color=color_palette5[i]),
                hovertemplate=f'<b>Department</b>: {dept}<br><b>Year</b>: %{{x}}<br><b>Production</b>: %{{y:,.0f}} barrels',
            ))
        fig_evol5.update_layout(
            yaxis_title='Annual Production (barrels)',
            xaxis_title='Year',
            template='plotly_white',
            hovermode='x unified',
            margin=dict(t=30, b=40, l=40, r=20),
            font=dict(family='Montserrat, Arial', size=14, color=color_texto),
            legend=dict(orientation='h', yanchor='top', y=-0.2, xanchor='center', x=0.5),
            showlegend=True,
            height=420
        )
        grafica_evol5 = dcc.Graph(
            figure=fig_evol5,
            style={'height': '420px'}
        )

    	# Treemap: Participación de la producción total por municipio (con información de cuenca)
        if 'Municipio' in dff.columns and 'Cuenca' in dff.columns:
            df_muni_basin = dff.groupby(['Municipio', 'Cuenca'], as_index=False)['Produccion crudo'].sum()
            df_muni_basin = df_muni_basin.sort_values('Produccion crudo', ascending=False).head(15)
            fig_treemap = px.treemap(
                df_muni_basin,
                path=['Municipio'],
                values='Produccion crudo',
                color='Produccion crudo',
                color_continuous_scale=colores,
                title='Share of Total Production by Top 15 Municipalities',
                hover_data={'Cuenca': True, 'Produccion crudo':':,.0f'},
            )
            fig_treemap.update_traces(
                texttemplate='<b>%{label}</b><br>%{value:,.0f} barrels',
                marker=dict(line=dict(width=2, color='white')),
                hovertemplate='<b>Municipality:</b> %{label}<br><b>Basin:</b> %{customdata[0]}<br><b>Production:</b> %{value:,.0f} barrels<extra></extra>'
            )
            fig_treemap.update_layout(
                font=dict(family='Montserrat, Arial', size=13, color=color_texto),
                title_font=dict(size=16, color=color_texto, family='Montserrat, Arial'),
                margin=dict(t=40, b=20, l=20, r=20),
                height=420,
                paper_bgcolor='white',
                plot_bgcolor='white',
                coloraxis_colorbar=dict(title="Production", tickformat=",.0f")
            )
            grafica_treemap = dcc.Graph(
                figure=fig_treemap,
                style={'height': '420px'}
            )
        elif 'Municipio' in dff.columns:
            df_muni_total = dff.groupby('Municipio', as_index=False)['Produccion crudo'].sum()
            df_muni_total = df_muni_total.sort_values('Produccion crudo', ascending=False).head(15)
            fig_treemap = px.treemap(
                df_muni_total,
                path=['Municipio'],
                values='Produccion crudo',
                color='Produccion crudo',
                color_continuous_scale=colores,
                title='Share of Total Production by Top 15 Municipalities',
                hover_data={'Produccion crudo':':,.0f'},
            )
            fig_treemap.update_traces(
                texttemplate='<b>%{label}</b><br>%{value:,.0f} barrels',
                marker=dict(line=dict(width=2, color='white')),
                hovertemplate='<b>Municipality:</b> %{label}<br><b>Production:</b> %{value:,.0f} barrels<extra></extra>'
            )
            fig_treemap.update_layout(
                font=dict(family='Montserrat, Arial', size=13, color=color_texto),
                title_font=dict(size=16, color=color_texto, family='Montserrat, Arial'),
                margin=dict(t=40, b=20, l=20, r=20),
                height=420,
                paper_bgcolor='white',
                plot_bgcolor='white',
                coloraxis_colorbar=dict(title="Production", tickformat=",.0f")
            )
            grafica_treemap = dcc.Graph(
                figure=fig_treemap,
                style={'height': '420px'}
            )
        else:
            grafica_treemap = html.Div("No municipality data available.", style={'color': 'red', 'textAlign': 'center', 'marginTop': '40px'})

    	# Mostrar treemap y gráfica de líneas lado a lado
        charts_row = dbc.Row([
            dbc.Col([
                html.H4("Share of Total Production by Municipality (Treemap)", style={'color': color_primario, 'fontWeight': 'bold', 'marginTop': '30px', 'textAlign': 'center'}),
                grafica_treemap
            ], width=6),
            dbc.Col([
                html.H4("Annual Production Evolution of Top 5 Departments", style={'color': color_primario, 'fontWeight': 'bold', 'marginTop': '30px', 'textAlign': 'center'}),
                grafica_evol5
            ], width=6)
        ], className="mb-2")

        return html.Div([
            kpi_dept,
            html.Div([
                html.H4("Geographic Distribution - Crude Production by Department", style={'color': color_primario, 'fontWeight': 'bold', 'marginTop': '30px', 'textAlign': 'center'}),
                grafica_map
            ], style={'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 4px 12px rgba(0, 166, 147, 0.08)', 'padding': '20px', 'marginTop': '10px'}),
            html.Div([
                charts_row
            ], style={'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 4px 12px rgba(0, 166, 147, 0.08)', 'padding': '20px', 'marginTop': '10px'})
        ])
    return html.Div()

def crear_tab_general(df_filtered):
    """KPIs para la pestaña de análisis general de crudo"""
    prod_total = df_filtered['Produccion crudo'].sum() if not df_filtered.empty else 0
    año_actual = df_filtered['Año'].max() if not df_filtered.empty else None
    año_anterior = año_actual - 1 if año_actual is not None else None
    prod_total_actual = df_filtered[df_filtered['Año'] == año_actual]['Produccion crudo'].sum() if año_actual is not None else 0
    prod_total_anterior = df_filtered[df_filtered['Año'] == año_anterior]['Produccion crudo'].sum() if año_anterior is not None else 0
    if prod_total_anterior > 0:
        variacion_total = ((prod_total_actual - prod_total_anterior) / prod_total_anterior) * 100
        variacion_total_str = f"{variacion_total:.2f}%"
    else:
        variacion_total_str = "N/A"
    prod_promedio = df_filtered['Produccion crudo'].mean() if not df_filtered.empty else 0
    if not df_filtered.empty:
        año_mejor = df_filtered.loc[df_filtered['Produccion crudo'].idxmax(), 'Año']
        prod_mejor = df_filtered[df_filtered['Año'] == año_mejor]['Produccion crudo'].sum()
    else:
        año_mejor = 'N/A'
        prod_mejor = 0

    return [
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Production", className="card-title text-center mb-2", style={'color': color_primario, 'fontWeight': '700'}),
                        html.H2(f"{prod_total:,.0f}", className="text-center", style={'fontSize': '28px', 'fontWeight': 'bold', 'color': color_texto}),
                        html.P("Accumulated crude production", className="text-center text-muted", style={'fontSize': '14px'})
                    ], style={'padding': '20px'})
                ], style={'height': '170px', 'borderRadius': '15px', 'boxShadow': '0 8px 32px rgba(0, 166, 147, 0.10)', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'})
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Variation vs Previous Year", className="card-title text-center mb-2", style={'color': '#0059b3', 'fontWeight': '700'}),
                        html.H2(variacion_total_str, className="text-center", style={'fontSize': '28px', 'fontWeight': 'bold', 'color': color_texto}),
                        html.P("% compared to previous year", className="text-center text-muted", style={'fontSize': '14px'})
                    ], style={'padding': '20px'})
                ], style={'height': '170px', 'borderRadius': '15px', 'boxShadow': '0 8px 32px rgba(0, 59, 179, 0.10)', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'})
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Average Annual Production", className="card-title text-center mb-2", style={'color': color_secundario, 'fontWeight': '700'}),
                        html.H2(f"{prod_promedio:,.0f}", className="text-center", style={'fontSize': '28px', 'fontWeight': 'bold', 'color': color_texto}),
                        html.P("Annual average crude production", className="text-center text-muted", style={'fontSize': '14px'})
                    ], style={'padding': '20px'})
                ], style={'height': '170px', 'borderRadius': '15px', 'boxShadow': '0 8px 32px rgba(255, 193, 7, 0.10)', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'})
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Best Production Year", className="card-title text-center mb-2", style={'color': '#ff9800', 'fontWeight': '700'}),
                        html.H2(f"{año_mejor}", className="text-center", style={'fontSize': '28px', 'fontWeight': 'bold', 'color': color_texto}),
                        html.P(f"Total: {prod_mejor:,.0f}", className="text-center text-muted", style={'fontSize': '14px'})
                    ], style={'padding': '20px'})
                ], style={'height': '170px', 'borderRadius': '15px', 'boxShadow': '0 8px 32px rgba(255, 152, 0, 0.10)', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'})
            ], width=3)
        ], className="mb-4", style={'marginLeft': '10px', 'marginRight': '10px'})
    ]

# Ejecutar el servidor de la app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=True, port=port, host="0.0.0.0")

