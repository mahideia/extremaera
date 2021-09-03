import plotly as plt
import plotly.express as px
import json
from urllib.request import urlopen
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

def df_estados(Brazil):
    #acerta os estados
    state_id_map = {}
    for feature in Brazil ['features']:
        feature['id'] = feature['properties']['name']
        state_id_map[feature['properties']['sigla']] = feature['id']

    #faz um esqueminha de indicar qual estado é pra colorir
    df = pd.DataFrame.from_dict(state_id_map,orient='index').reset_index()
    df.columns=['sigla','estado']
    return df

def plota_estados(Brazil,df, estado):
    #colors
    colors = ['#F0f0f0','#086375']
    #pega o mapa



    if estado == 'BR':
        df['selecionado']=1
    else:
        df['selecionado']=0
        df.loc[df.sigla==estado,'selecionado']=1

    #plota estados
    fig=go.Figure()
    fig.add_trace(go.Choroplethmapbox(
        geojson=Brazil, locations=df['estado'], z=df['selecionado'],
        colorscale=colors, zmin=0, zmax=1,
        marker_opacity=0.5, marker_line_width=0.5,
    ))
    fig.update_traces(showscale=False)

    fig.update_layout(mapbox_style="white-bg",
                  mapbox_zoom=2.5, mapbox_center = {"lat": -15, "lon": -55})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    #fig.update_geos(fitbounds="locations", visible=False)

    return fig


def plot_barras_temperatura_precipitacao(estado):
    df = pd.read_csv('dados/dados_base.csv',header=None, low_memory=False)
    df.columns=['data','sigla','evento','estacao','criterio']
    df.data = pd.to_datetime(df.data)
    df = df[(df.data.dt.year >= 1960)  & (df.data.dt.year < 2021)]
    if estado != 'BR':
        df = df[(df.sigla==estado)]
    temperatura = df[(df.evento=='temperatura')]
    temperatura = temperatura.resample('D',on='data').estacao.count().reset_index()
    temperatura = temperatura[temperatura.estacao>0]
    temperatura = temperatura.resample('Y',on='data').estacao.count().reset_index()
    precipitacao = df[(df.evento=='precipitacao')]
    precipitacao = precipitacao.resample('D',on='data').estacao.count().reset_index()
    precipitacao = precipitacao[precipitacao.estacao>0]
    precipitacao = precipitacao.resample('Y',on='data').estacao.count().reset_index()

    fig = make_subplots(rows=2, cols=1,
                    shared_xaxes=False,
                    vertical_spacing=0.065)
    fig.add_trace(go.Bar(
        x=temperatura.data.dt.year,
        y=temperatura.estacao,
        name='Temperatura',
        marker_color='indianred',
        hovertemplate=
            'Ano: %{x}<br>'+
            'Dias: %{y}',
    ),row=1,col=1)
    fig.add_annotation(text='Dias por ano com <b>temperatura</b> máxima > 35°C',
        xref="paper", yref="paper",
        x=1.02, y=1.08, showarrow=False,
        font = {
            'family': "Arial",
            'size': 15,
            'color': "indianred"})

    fig.add_trace(go.Bar(
        x=precipitacao.data.dt.year,
        y=precipitacao.estacao,
        name='Precipitacao',
        marker_color='slateblue',
        hovertemplate=
            'Ano: %{x}<br>'+
            'Dias: %{y}',
    ),row=2,col=1)
    #fig.update_yaxes(autorange="reversed",row=2,col=1)
    fig.add_annotation(text='Dias por ano com <b>precipitação</b> total > 50mm',
        xref="paper", yref="paper",
        x=1.02, y=-.13, showarrow=False,
        font = {
            'family': "Arial",
            'size': 15,
            'color': "slateblue"})

    fig.update_yaxes(tickfont=dict(
        color='indianred',
        family='Arial'
    ),row=1,col=1)
    fig.update_yaxes(tickfont=dict(
        color='slateblue',
        family='Arial'
    ),row=2,col=1)
    fig.update_xaxes(tickfont=dict(
        color='grey',
        family='Arial',
        size=10
    ),row=1,col=1)
    fig.update_xaxes(tickfont=dict(
        color='grey',
        family='Arial',
        size=10
    ),row=2,col=1)
    fig.update_xaxes(visible=True,row=1,col=1)
    #fig.update_xaxes(visible=False,row=2,col=1)

    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor = 'white',
        height = 400,
        margin=dict(
            l=20,
            r=20,
            b=30,
            t=120,
            pad=1
        ),
        showlegend=False
    )


    return fig

def le_dados(tipo,evento, estado,ano=None,data=None):
    if tipo == 'dados_base':
        df = pd.read_csv('dados/dados_base.csv',header=None, low_memory=False)
        df.columns=['data','sigla','evento','estacao','criterio']
        df.data = pd.to_datetime(df.data)
        df = df[(df.data.dt.year >= 1960)  & (df.data.dt.year < 2021)]
        if estado!='BR':
            df=df[(df.sigla==estado)]
        dados = df[(df.evento==evento)]
        dados = dados.resample('D',on='data').estacao.count().reset_index()
        dados = dados[dados.estacao>0]
        dados = dados.resample('Y',on='data').estacao.count().reset_index()
    if tipo=='calendario':
        df = pd.read_csv('dados/dados_base.csv',header=None, low_memory=False)
        df.columns=['data','sigla','evento','estacao','criterio']
        df.data = pd.to_datetime(df.data)
        df = df[(df.data.dt.year == ano)]
        if estado!='BR':
            df=df[(df.sigla==estado)]
        dados = df[(df.evento==evento)]
        dados = dados.resample('D',on='data',origin=pd.Timestamp(str(ano)+'-01-01')).estacao.count().reset_index()
        dados['data'] = pd.to_datetime(dados['data'])
        dados['dia_semana']=dados['data'].dt.day_of_week
        dados['semana_ano']=dados['data'].dt.isocalendar().week
        for final in ['-12-25','-12-26','-12-27','-12-28','-12-29','-12-30','-12-31']:
            if len(dados[dados['data']==str(ano)+final]['semana_ano'])>0:
                if dados[dados['data']==str(ano)+final]['semana_ano'].values[0]==1 or dados[dados['data']==str(ano)+final]['semana_ano'].values[0]==0:
                    dados.loc[dados['data']==str(ano)+final,'semana_ano']=53

    if tipo == 'estacoes':
        df = pd.read_csv('dados/dados_base.csv',header=None, low_memory=False)
        df.columns=['data','sigla','evento','estacao','criterio']
        df.data = pd.to_datetime(df.data)
        if estado!='BR':
            df=df[(df.sigla==estado)]
        df = df[df['data']==data]
        df = df[df['evento']==evento]
        dados = df.estacao.unique()

    return dados

def plot_calendario(tipo,ano,estado):

    dados = le_dados('calendario',tipo,estado,ano=ano)
    ix = pd.date_range('1/1/'+str(ano),str(ano)+'-12-31',freq='D')
    df = pd.DataFrame(index=ix).reset_index()
    df.columns = ['data']
    dados = pd.merge(dados,df,how='outer').fillna(0)


    if tipo == 'temperatura':
        cores = [[0,'#f3f0f0'],[1,'indianred']]
    else:
        cores = [[0,'#f0f0f8'],[1,'slateblue']]

    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        y=dados['semana_ano'],
        x=dados['dia_semana'],
        z=dados['estacao'],
        type='heatmap',
        colorscale=cores,
        text=dados['data'],
        hovertemplate='%{text|%d-%m-%Y}<extra></extra>',
        xgap=2, # this
        ygap=2, # and this is used to make the grid-like apperance
        #showscale=False
        hoverongaps= False
    ))

    fig.update_layout(
        font={'size':12, 'color':'#9e9e9e'},
        plot_bgcolor=('#fff'),
        margin = dict(t=30,r=10,l=10,b=10),
        height=720,
        width=350,
        title=str(ano)
        )

    fig.update_xaxes(dict(
        title_font=dict(size=20,family='Raleway'),
        showline = False, showgrid = False, zeroline = False,
        tickmode="array",
        ticktext=["Seg ", "Ter ", "Qua ", "Qui ", "Sex ", "Sab ", "Dom "],
        tickvals=[0,1,2,3,4,5,6],
        #autorange="reversed"
        ))
    fig.update_yaxes(dict(
        title_font=dict(size=20,family='Raleway'),
        showline = False, showgrid = False, zeroline = False,
        tickmode="array",
        ticktext=["Jan ", "Fev ", "Mar ", "Abr ", "Mai ", "Jun ", "Jul ","Ago ","Set ","Out ","Nov ","Dez "],
        tickvals=[1,6,10,14,18,23,27,31,35,39,43,48],
        #autorange="reversed"
        ))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(autorange='reversed')



    #fig.show()
    return fig

def temp_prec(estacao,data):
    dados = pd.read_csv(f'dados/diarios/{estacao}.csv',header=None)
    if estacao[0]=='A' or estacao[0]=='B' or estacao[0]=='F' or estacao[0]=='S':
        dados.columns=['data','hora','precipitacao','temperatura','temperatura_max','evento']
    else:
        dados.columns=['data','hora','precipitacao','temperatura','evento']

    dados.hora = dados.hora/100
    dados.data = pd.to_datetime(dados.data)
    dados = dados[(dados.data ==data)]
    d = dados#[dados['evento']==evento]


    fig = make_subplots(specs=[[{"secondary_y": True}]])


    if len(d)>0:
        fig.add_trace(go.Bar(
            x= d.hora,
            y= d.precipitacao,
            name= "Precipitação",
            marker_color='slateblue',
            hovertemplate="Hora: %{x}<br>Precipitacao: %{y} mm<extra></extra>"
        ), secondary_y=False)


    if len(d)>0:
        fig.add_trace(go.Scatter(
            x=d.hora,
            y=d.temperatura,
            name="Temperatura",
            marker_color='indianred',
            hovertemplate="Hora: %{x}<br>Temperatura: %{y} °C<extra></extra>"
        ), secondary_y=True)

    fig.update_yaxes(title='Precipitação (mm)',secondary_y=False)
    fig.update_yaxes(title='Temperatura (°C)',secondary_y=True)
    fig.update_xaxes(title='Hora')
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor = 'white',
        height = 550,
        legend_orientation='h'
    )

    return fig

def temp_prec_semdados():
    fig = go.Figure()
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor = 'white',
        height = 550
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.add_annotation(text='Escolha uma estação para visualizar os dados',yref='paper',xref='paper',x=0.5,y=0.5,showarrow=False)
    return fig
