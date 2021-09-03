import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.graph_objs as go


from util import layout_app as la
from util import graficos as gr

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../dados").resolve()

config = {
    'scrollZoom': False,
    'displayModeBar': False,
    'editable': False,
    'showLink':False,
    'displaylogo': False
}
#df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
#df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))


def create_layout(app):
    # Page layouts


    conteudo = html.Div([
        dbc.Card([
            dbc.CardHeader(html.H3("Quantos dias (muito) quentes e chuvosos tivemos nos últimos 60 anos? (por estado)")),
            dbc.CardBody(
                html.Div(className='row',children=[
                    html.Div(className="col-lg-4",children=[
                        dcc.Dropdown(
                            options=[
                                    {'label':'Brasil','value':'BR'},
                                    {'label':'Acre','value':'AC'},
                                    {'label':'Alagoas','value':'AL'},
                                    {'label':'Amazonas','value':'AM'},
                                    {'label':'Amapá','value':'AP'},
                                    {'label':'Bahia','value':'BA'},
                                    {'label':'Ceará','value':'CE'},
                                    {'label':'Espírito Santo','value':'ES'},
                                    {'label':'Goiás','value':'GO'},
                                    {'label':'Maranhão','value':'MA'},
                                    {'label':'Minas Gerais','value':'MG'},
                                    {'label':'Mato Grosso do Sul','value':'MS'},
                                    {'label':'Mato Grosso','value':'MT'},
                                    {'label':'Pará','value':'PA'},
                                    {'label':'Paraíba','value':'PB'},
                                    {'label':'Pernambuco','value':'PE'},
                                    {'label':'Piauí','value':'PI'},
                                    {'label':'Paraná','value':'PR'},
                                    {'label':'Rio de Janeiro','value':'RJ'},
                                    {'label':'Rio Grande do Norte','value':'RN'},
                                    {'label':'Rondônia','value':'RO'},
                                    {'label':'Roraima','value':'RR'},
                                    {'label':'Rio Grande do Sul','value':'RS'},
                                    {'label':'Santa Catarina','value':'SC'},
                                    {'label':'Sergipe','value':'SE'},
                                    {'label':'São Paulo','value':'SP'},
                                    {'label':'Tocantins','value':'TO'},
                                    {'label':'Distrito Federal','value':'DF'},
                            ],
                            value='SP',
                            multi=False,
                            id='drop-estados'
                        ),
                        dcc.Loading(dcc.Graph(id='mapa',config=config))]),
                    html.Div(className="col-lg-8",children=[dcc.Loading(children=dcc.Graph(id='eventos',config=config))])
                ])
                ),
            dbc.CardFooter("""Escolha um estado (ou todo o país) e veja quantos dias, por ano, foram registradas temperaturas acima de 35°C ou precipitação acima de 50 mm/dia.
                            Você pode clicar em uma das barras e ver logo abaixo a distribuição de eventos de temperatura ou precipitação ao longo do ano correspondente."""),

            ],className="mb-5",
        ),
        html.Div(className='row',children=[
            html.Div(className='col-lg-5',children=[
                dbc.Card([
                    dbc.CardHeader(html.H3("Eventos ao longo de um ano")),
                    dbc.CardBody([
                        html.Div(className='row',children=[
                            html.Div(className='col-lg-12',children=dcc.Loading(dcc.Graph(id='calendario',config=config))),
                        ]),
                    ]),
                    dbc.CardFooter("""Neste gráfico você pode ver quantos eventos por dia, ao longo de um ano, foram vistos.
                            Selecione um dia para ver quais as estações que registraram T>35°C ou precipitação > 50mm/dia"""),
                ],className="mb-5"),
            ],),
            html.Div(className='col-lg-7',children=
                dbc.Card([
                    dbc.CardHeader(html.H3("Dia na estação",id='titulo-dia')),
                    dbc.CardBody([dcc.Dropdown(id='drop-estacoes'),
                        dcc.Loading(dcc.Graph(id='grafico-estacao',config=config)),
                    ]),
                    dbc.CardFooter("Escolha a estação e veja o registro ao longo do dia selecionado"),
                ],className="mb-5")
            ), dcc.Store(id='store-tipo')
    ])])
    return la.defineLayout(conteudo)
