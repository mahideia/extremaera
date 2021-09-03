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
                    dcc.Markdown("## Sobre a idéia"),html.P(
                    """Esse dashboard foi construído como uma iniciativa de divulgação científica para aumentar a conscientização acerca de eventos extremos e sua frequência em crescimento em um mundo sob mudanças climáticas."""
                    ),dcc.Markdown("""Com a publicação do sexto relatório do primeiro grupo de trabalho do IPCC, alguns resultados reunidos ao longo dos últimos anos receberam maior atenção. Um desses resultados diz respeito à frequencia e intensidade, que devem aumentar, de eventos extremos. Extremos de temperatura, seja com mais ondas de calor ou frios intensos, vão se intensificar e acontecer mais vezes. Extremos de precipitação também poderão ser vistos com maior frequência em diversas regiões. Secas serão mais preocupantes em outras regiões."""),
                    dcc.Markdown("""Todos esses resultados são bastante alarmantes e para evitá-los precisamos tomar ações definitivas, urgentes e bem informadas."""),
                    dcc.Markdown("""Foi pensando nisso que esse dashboard foi construído. Ser uma ferramenta para a disseminação de informações públicas e dar autonomia para que as pessoas conhecam melhor suas regiões e avaliem riscos que podemos estar correndo"""),
                    dcc.Markdown("""Ainda que ações individuais pareçam ter pouco impacto, estar bem informado, conhecer a realidade que se aproxima e entender que nossa participação política (seja no processo eleitoral, seja no dia-a-dia) tem impacto faz parte de começar a construir um futuro melhor para todos. """),
                    html.Br(),
                    dcc.Markdown("## Sobre o conteúdo"),
                    dcc.Markdown("""Definir um evento extremo não é algo realmente fácil. A literatura é vasta e muito, muito diversificada. Para identificar eventos extremos de precipitação alguns trabalhos utilizam o Índice de Precipitação Normalizado, outros consideram um valores a partir de um percentil da distribuição de volume de chuvas diários, outros consideram um valor limite, como 50 mm de precipitação por dia, já poderia configurar um evento extremo.  """),
                    dcc.Markdown("""Nesse trabalho fiz uma escolha pensando em simplicidade e praticidade. Como uma análise mais aprofundada de dados e uma identificação mais precisa de eventos extremos demandaria mais tempo dois limites foram escolhidos para filtrar os dados obtidos. Dentro dessa escolha bastante simplificada optei por chamar de **dias (muito) quentes** e **dias (muito) chuvosos** deixando, assim, a discussão sobre definição de eventos extremos/severos em aberto e podendo abranger um estudo mais aprofundado no futuro."""),
                    dcc.Markdown("""Os **dias (muito) quentes** são aqueles que possuem ao menos um registro de temperatura máxima na estação acima de 35°C. Os **dias (muito) chuvosos** contam com registro de precipitação da estação acima de 50 mm, no dia todo."""),
                    dcc.Markdown("""Os dados utilizados nesse dashboard foram adquiridos através do site do INMET e são dados de temperatura e precipitação registrados por estações meteorológicas convencionais ou automáticas (pedidos feitos para todas as estações disponíveis) no período de 01/01/1960 a 31/12/2020. Nenhum pré-processamento foi feito nesses dados. Esse dashboard se dispõe a ser uma visualização direta dos dados registrados pelas estações e disponibilizados pelo INMET. Uma análise posterior pode ser interessante para aumentar a qualidade do trabalho, mas por ora é importante ter em mente que todos os gráficos apresentados são demonstrações fieis dos registros. """)
                ])
            ),
            className="mb-5",
        ),
    )
    return la.defineLayout(conteudo)
