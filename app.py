# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from util import graficos as gr
from dash.dependencies import Input, Output,State
from urllib.request import urlopen
import json
import pandas as pd

from pages import (
    home,
    sobre,
    sobre_ma
)


with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
    Brazil = json.load(response)
brasil_estados = {'Brasil':'BR','Acre':'AC','Alagoas':'AL','Amazonas':'AM','Amapá':'AP','Bahia':'BA','Ceará':'CE','Espírito Santo':'ES','Maranhão':'MA','Minas Gerais':'MG','Mato Grosso do Sul':'MS','Mato Grosso':'MT','Pará':'PA','Paraíba':'PB','Pernambuco':'PE','Piauí':'PI','Paraná':'PR','Rio de Janeiro':'RJ','Rio Grande do Norte':'RN','Rondônia':'RO','Roraima':'RR','Rio Grande do Sul':'RS','Santa Catarina':'SC','Sergipe':'SE','São Paulo':'SP','Tocantins':'TO','Distrito Federal':'DF'}
df_estados = gr.df_estados(Brazil)

app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.PULSE],suppress_callback_exceptions=True
)
app.title = "Extrema Era"
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/home":
        return home.create_layout(app)
    elif pathname == "/sobre":
        return sobre.create_layout(app)
    elif pathname == "/sobre_ma":
        return sobre_ma.create_layout(app)
    else:
        return home.create_layout(app)


@app.callback(Output('mapa','figure'),Input('drop-estados','value'))
def update_mapa(value):
    return gr.plota_estados(Brazil,df_estados,value)

@app.callback(Output('drop-estados','value'),Input('mapa','clickData'))
def update_drop(click):
    if click == None:
        return 'SP'
    else:
        print(click['points'][0]['location'])
        return brasil_estados[click['points'][0]['location']]

@app.callback(Output('eventos','figure'),Input('drop-estados','value'))
def update_eventos(estado):
    return gr.plot_barras_temperatura_precipitacao(estado)

@app.callback(Output('calendario','figure'),Output('store-tipo','children'),[Input('eventos','clickData'),Input('drop-estados','value')])
def update_calendario(click,estado):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id']=='drop-estados.value':
        ano = 2020
        estado = ctx.triggered[0]['value']
        evento = 'temperatura'
    else:
        if click['points'][0]['curveNumber']==0:
            evento = 'temperatura'
        else:
            evento = 'precipitacao'
        ano = click['points'][0]['x']
    return gr.plot_calendario(evento,ano,estado),evento

@app.callback(Output('drop-estacoes','options'),Output('titulo-dia','children'),[Input('calendario','clickData'),Input('drop-estados','value')],Input('store-tipo','children'))
def update_drop_estacoes(click,estado,tipo_evento):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id']!='store-tipo.children':
        if click is not None:
            data = click['points'][0]['text'][:10]
            est = gr.le_dados('estacoes',tipo_evento,estado,data=data)
            estacoes = pd.read_csv('dados/estacoes.csv')
            estacoes = estacoes[estacoes.codigo.isin(est)]
            estacoes['nome'] = estacoes['codigo'] + ' - ' +estacoes.estacao
            dd_estacoes = []
            for estacao in estacoes.nome:
                op = {'label':estacao,'value':estacao}
                dd_estacoes.append(op)

            return dd_estacoes,"Dia na estação ("+data+")"
        else:
            return [{'label':'Escolha um dia no calendário','value':0}],"Dia na estação "
    else:
        return [{'label':'Escolha um dia no calendário','value':0}],"Dia na estação "

@app.callback(Output('grafico-estacao','figure'),Input('drop-estacoes','value'),Input('titulo-dia','children'))
def update_grafico_estacao(estacao,titulo):
    ctx = dash.callback_context

    if estacao == 0 or estacao is None or ctx.triggered[0]['prop_id']=='titulo-dia.children':
        fig = gr.temp_prec_semdados()
    else:
        data = titulo[16:26]
        fig = gr.temp_prec(estacao,data)
    return fig

if __name__ == "__main__":
    app.run_server(debug=False)
