import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


texto_p = """Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's
   standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."""

titulo_do_trabalho = "Eventos quentes e chuvosos por estado"

subtitulo_pagina  = ""#"""Veja quantos eventos de tempo (muito) quente ou (muito) chuvoso um estado registrou nos últimos 60 anos."""

nome_dash = "Extrema Era"

texto_cal = """
    """#\nUma descrição específica das ações no dia selecionado será apresentada logo abaixo."""



titulo_sobre = """ """


def defineLayout(conteudo):

    navbar = dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                children=[
                    #dbc.DropdownMenuItem("Mais", header=True),
                    #dbc.DropdownMenuItem("Sobre a pesquisa", href="/apps/pesquisa"),
                    dbc.DropdownMenuItem("Sobre o dashboard", href="/sobre"),
                    dbc.DropdownMenuItem("Quem fez", href="/sobre_ma"),
                ],
                nav=True,
                in_navbar=True,
                label="Mais",
            ),
        ],
        brand=nome_dash,
        brand_href="/home",
        color="dark",
        dark=True,
        className='navbar fixed-top'
    )



    rodape = dbc.NavbarSimple(
        children=[html.Div(dcc.Markdown("""Esse é um dash desenvolvido (às pressas) por [Marina M. Mendonça.](https://linktr.ee/mahideia)"""))],
        brand_href="#",
        color="dark",
        dark=True,
        className='navbar bottom'
    )

    titulo = html.Div([html.H2(titulo_do_trabalho,style={'padding-top':'100px','padding-bottom':'10px'}),
        #html.P(subtitulo_pagina,
        #   style={'padding-top':'0px','padding-bottom':'40px','padding-left':'25px','padding-right':'25px'}),
           dcc.Markdown(subtitulo_pagina + texto_cal,style={'padding-top':'0px','padding-bottom':'40px','padding-left':'25px','padding-right':'25px'})])

    layout = html.Div([navbar,
                      html.Div([
                            html.Div(titulo,className='container'),
                            html.Div(conteudo,className='container'),
                      ],className='container'),
                      rodape])
    return layout
