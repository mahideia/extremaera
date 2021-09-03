import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.graph_objs as go


from util import layout_app as la

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../dados").resolve()


#df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
#df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))


def create_layout(app):
    # Page layouts


    conteudo = html.Div(
        dbc.Card(
            dbc.CardBody(
                html.Div(className='row',children=[
                    dcc.Markdown("## Sobre quem fez"),
                    dcc.Markdown("Oi, eu sou a Marina M. M., e eu que fiz esse dashboard. Sou bacharela em Física pela Universidade de São Paulo, onde também fiz meu mestrado com física atmosférica. Hoje eu to emocionalmente envolvida com um doutorado na Unesp Sorocaba, no programa de Ciências Ambientais, ainda mexendo com nuvens e sensoriamento remoto."),
                    dcc.Markdown("Na vida eu sou um pouquinho física, um pouquinho (ex)professora, um pouquinho 'moça que faz gráficos', que é o que eu fiz aqui: uns gráficos. Esse dashboard foi um desses projetos pessoais que eu decidi por em ação depois de ter tido uma idéia e achar que ela era divertida o suficiente pra ocupar meu tempo livre. E foi isso, eu fiz no meu tempo livre. Por isso é possível que você esbarre com algumas coisinhas para consertar, tenham paciência, por favor."),
                    dcc.Markdown("Se você quiser entrar em contato pode enviar um email para ma.monteiro.m (no gmail), ou me seguir no [twitter](http://twitter.com/mahideia) onde eu reclamo muito e faço, às vezes, uns fios divertidos sobre física. Ah, se quiser ouvir minha voz (ou outras vozes muito melhores) dá uma olhadinha no podcast de divulgação científica que eu participo, o [Dragões de Garagem](http://dragoesdegaragem.com).")
                ])
            ),
            className="mb-5",
        ),
    )
    return la.defineLayout(conteudo)
