"""
questions.py  –  Banco de questões do Geomix
Estrutura: 5 unidades × 5 atividades × 5 questões = 125 questões
"""
import random
import math

UNITS_META = {
    1: {
        'title': 'Identificação das Figuras',
        'subtitle': 'Reconheça e nomeie as figuras planas',
        'color': '#2CA4BF',
        'intro_title': 'O que são figuras planas?',
        'intro_text': (
            'Figuras planas são formas geométricas que existem em apenas duas dimensões: '
            'largura e altura. Elas estão em todo lugar ao nosso redor! '
            'Uma pizza tem formato de círculo, um azulejo tem formato de quadrado, '
            'uma janela tem formato de retângulo. '
            'Nesta unidade você aprenderá a reconhecer 8 figuras planas fundamentais.'
        ),
        'intro_figures': ['square','rectangle','triangle','equilateral_triangle',
                          'trapezoid','rhombus','circle','hexagon'],
        'activities': [
            {'title': 'Identificação em imagens',    'type': 'multiple_choice',        'icon': '𖥑'},
            {'title': 'Nome para a figura',           'type': 'multiple_choice_figure', 'icon': '𖥑'},
            {'title': 'Arrastar nomes',               'type': 'drag_drop',              'icon': '𖥑'},
            {'title': 'Objetos do cotidiano',         'type': 'multiple_choice',        'icon': '𖥑'},
            {'title': 'Quiz cronometrado',            'type': 'timed_quiz',             'icon': '𖥑'},
        ],
    },
    2: {
        'title': 'Características das Figuras',
        'subtitle': 'Lados, vértices e propriedades',
        'color': '#F2A413',
        'intro_title': 'Lados, Vértices e Ângulos',
        'intro_text': (
            'Cada figura plana tem características únicas. '
            'O triângulo tem 3 lados e 3 vértices. O quadrado tem 4 lados iguais. '
            'O círculo não tem lados nem vértices – apenas raio e diâmetro. '
            'Conhecer essas características é fundamental para distinguir as figuras '
            'e aplicar as fórmulas corretas de área.'
        ),
        'intro_figures': ['square','triangle','rhombus','circle'],
        'activities': [
            {'title': 'Lados e vértices',            'type': 'fill_blank',  'icon': '𖥑'},
            {'title': 'Associar elementos',          'type': 'drag_drop',   'icon': '𖥑'},
            {'title': 'Classificar por lados',       'type': 'drag_drop',   'icon': '𖥑'},
            {'title': 'Comparar duas figuras',       'type': 'multiple_choice', 'icon': '𖥑'},
            {'title': 'Descrição correta',           'type': 'multiple_choice', 'icon': '𖥑'},
        ],
    },
    3: {
        'title': 'Fórmulas de Área',
        'subtitle': 'Aprenda as fórmulas de cada figura',
        'color': '#D9307F',
        'intro_title': 'Fórmulas de Área das Figuras Planas',
        'intro_text': (
            'A área mede a superfície de uma figura plana. '
            'Cada figura tem sua própria fórmula. O quadrado usa A = l² (lado ao quadrado). '
            'O círculo usa A = π × r² (π ≈ 3,14). O triângulo usa A = (base × altura) ÷ 2. '
            'Nesta unidade você vai conhecer, memorizar e aplicar todas essas fórmulas!'
        ),
        'intro_figures': ['square','circle','triangle','trapezoid'],
        'activities': [
            {'title': 'Completar fórmulas',          'type': 'fill_blank',     'icon': '𖥑'},
            {'title': 'Relacionar figura-fórmula',   'type': 'memory_match',   'icon': '𖥑'},
            {'title': 'Encontrar o erro',            'type': 'multiple_choice','icon': '𖥑'},
            {'title': 'Ordenar etapas',              'type': 'order_steps',    'icon': '𖥑'},
            {'title': 'Quiz conceitual',             'type': 'multiple_choice','icon': '𖥑'},
        ],
    },
    4: {
        'title': 'Cálculo de Áreas',
        'subtitle': 'Aplique as fórmulas e resolva exercícios',
        'color': '#1A7A8F',
        'intro_title': 'Hora de Calcular!',
        'intro_text': (
            'Chegou a hora de usar as fórmulas na prática! '
            'Para calcular a área você precisa: identificar a figura, lembrar a fórmula, '
            'substituir os valores e fazer o cálculo. '
            'Sempre inclua a unidade de medida no resultado (cm², m², etc.). '
            'Vamos começar com exemplos guiados e avançar até os desafios!'
        ),
        'intro_figures': ['square','rectangle','triangle','circle'],
        'activities': [
            {'title': 'Cálculo guiado (passo a passo)', 'type': 'fill_blank',  'icon': '𖥑'},
            {'title': 'Cálculo direto',                 'type': 'fill_blank',  'icon': '𖥑'},
            {'title': 'Problemas contextualizados',     'type': 'fill_blank',  'icon': '𖥑'},
            {'title': 'Problemas de múltiplas etapas',  'type': 'fill_blank',  'icon': '𖥑'},
            {'title': 'Desafio cronometrado',           'type': 'timed_quiz',  'icon': '𖥑'},
        ],
    },
    5: {
        'title': 'Desafios Integradores',
        'subtitle': 'Una todos os conhecimentos!',
        'color': '#F28F16',
        'intro_title': 'O Grande Desafio Final!',
        'intro_text': (
            'Parabéns por chegar até aqui! '
            'Nesta última unidade você vai unir tudo que aprendeu: '
            'identificar figuras, conhecer suas características, '
            'lembrar as fórmulas e calcular áreas em situações reais. '
            'Os desafios serão maiores, mas você está pronto!'
        ),
        'intro_figures': ['square','rectangle','triangle','trapezoid','rhombus','circle'],
        'activities': [
            {'title': 'Identificar + calcular',     'type': 'multiple_choice','icon': '𖥑'},
            {'title': 'Problemas do cotidiano',     'type': 'fill_blank',     'icon': '𖥑'},
            {'title': 'Figuras combinadas',         'type': 'fill_blank',     'icon': '𖥑'},
            {'title': 'Missão gamificada',          'type': 'multiple_choice','icon': '𖥑'},
            {'title': 'Avaliação final',            'type': 'mixed',          'icon': '𖥑'},
        ],
    },
}

# ─────────────────────────────────────────────────────────────────
#  UNIT 1 — IDENTIFICAÇÃO DAS FIGURAS
# ─────────────────────────────────────────────────────────────────

def q_1_1():
    """Atividade 1.1 – Ver a figura e nomear (MC)"""
    return [
        {'id':1,'type':'multiple_choice','question':'Qual é o nome desta figura geométrica?',
         'figure':'square','options':['Quadrado','Retângulo','Losango','Hexágono'],'correct':0,
         'explanation':'O Quadrado tem 4 lados iguais e 4 ângulos retos (90°).','xp':10},
        {'id':2,'type':'multiple_choice','question':'Qual é o nome desta figura geométrica?',
         'figure':'circle','options':['Hexágono','Oval','Círculo','Esfera'],'correct':2,
         'explanation':'O Círculo é uma figura plana redonda; todos os seus pontos estão à mesma distância do centro.','xp':10},
        {'id':3,'type':'multiple_choice','question':'Qual é o nome desta figura geométrica?',
         'figure':'triangle','options':['Pirâmide','Triângulo','Losango','Trapézio'],'correct':1,
         'explanation':'O Triângulo tem 3 lados e 3 vértices. É a figura com o menor número de lados.','xp':10},
        {'id':4,'type':'multiple_choice','question':'Qual é o nome desta figura geométrica?',
         'figure':'trapezoid','options':['Retângulo','Quadrado','Trapézio','Losango'],'correct':2,
         'explanation':'O Trapézio tem 4 lados, com exatamente um par de lados paralelos (base maior B e base menor b).','xp':10},
        {'id':5,'type':'multiple_choice','question':'Qual é o nome desta figura geométrica?',
         'figure':'hexagon','options':['Pentágono','Octógono','Hexágono Regular','Heptágono'],'correct':2,
         'explanation':'O Hexágono Regular tem 6 lados iguais e 6 ângulos iguais de 120°.','xp':10},
    ]


def q_1_2():
    """Atividade 1.2 – Ler o nome e identificar a figura correta (MC com figuras como opções)"""
    return [
        {'id':1,'type':'multiple_choice_figure','question':'Qual dessas figuras é um LOSANGO?',
         'options':['rhombus','square','rectangle','triangle'],'correct':0,
         'explanation':'O Losango tem 4 lados iguais, mas seus ângulos não são necessariamente retos.','xp':10},
        {'id':2,'type':'multiple_choice_figure','question':'Qual dessas figuras é um RETÂNGULO?',
         'options':['square','rectangle','trapezoid','rhombus'],'correct':1,
         'explanation':'O Retângulo tem 4 ângulos retos e lados opostos iguais (base ≠ altura).','xp':10},
        {'id':3,'type':'multiple_choice_figure','question':'Qual dessas figuras é um TRIÂNGULO EQUILÁTERO?',
         'options':['triangle','equilateral_triangle','rhombus','trapezoid'],'correct':1,
         'explanation':'O Triângulo Equilátero tem os 3 lados iguais e os 3 ângulos iguais a 60°.','xp':10},
        {'id':4,'type':'multiple_choice_figure','question':'Qual dessas figuras é um CÍRCULO?',
         'options':['hexagon','rhombus','circle','equilateral_triangle'],'correct':2,
         'explanation':'O Círculo é a única figura plana completamente arredondada, sem lados retos.','xp':10},
        {'id':5,'type':'multiple_choice_figure','question':'Qual dessas figuras é um HEXÁGONO REGULAR?',
         'options':['trapezoid','circle','square','hexagon'],'correct':3,
         'explanation':'O Hexágono Regular tem 6 lados iguais — é a forma das células de favo de mel!','xp':10},
    ]


def q_1_3():
    """Atividade 1.3 – Arrastar nomes para figuras (drag-drop)"""
    return [
        {'id':1,'type':'drag_drop',
         'question':'Arraste o nome correto para cada figura',
         'items':['Quadrado','Círculo','Triângulo'],
         'targets':[
             {'id':'sq','figure':'square','correct':'Quadrado'},
             {'id':'ci','figure':'circle','correct':'Círculo'},
             {'id':'tr','figure':'triangle','correct':'Triângulo'},
         ],'explanation':'Quadrado→4 lados iguais; Círculo→arredondado; Triângulo→3 lados.','xp':15},
        {'id':2,'type':'drag_drop',
         'question':'Arraste o nome correto para cada figura',
         'items':['Retângulo','Trapézio','Losango'],
         'targets':[
             {'id':'re','figure':'rectangle','correct':'Retângulo'},
             {'id':'tp','figure':'trapezoid','correct':'Trapézio'},
             {'id':'rh','figure':'rhombus','correct':'Losango'},
         ],'explanation':'Retângulo→4 ângulos retos; Trapézio→1 par paralelo; Losango→4 lados iguais.','xp':15},
        {'id':3,'type':'drag_drop',
         'question':'Arraste o nome correto para cada figura',
         'items':['Hexágono Regular','Triângulo Equilátero','Quadrado'],
         'targets':[
             {'id':'hx','figure':'hexagon','correct':'Hexágono Regular'},
             {'id':'et','figure':'equilateral_triangle','correct':'Triângulo Equilátero'},
             {'id':'sq','figure':'square','correct':'Quadrado'},
         ],'explanation':'Hexágono→6 lados; Triângulo Equilátero→3 lados iguais; Quadrado→4 lados iguais e ângulos retos.','xp':15},
        {'id':4,'type':'drag_drop',
         'question':'Arraste o nome correto para cada figura',
         'items':['Círculo','Losango','Trapézio'],
         'targets':[
             {'id':'ci','figure':'circle','correct':'Círculo'},
             {'id':'rh','figure':'rhombus','correct':'Losango'},
             {'id':'tp','figure':'trapezoid','correct':'Trapézio'},
         ],'explanation':'Cada figura tem características únicas que nos permitem identificá-la.','xp':15},
        {'id':5,'type':'drag_drop',
         'question':'Arraste o nome correto para cada figura',
         'items':['Triângulo','Hexágono Regular','Retângulo'],
         'targets':[
             {'id':'tr','figure':'triangle','correct':'Triângulo'},
             {'id':'hx','figure':'hexagon','correct':'Hexágono Regular'},
             {'id':'re','figure':'rectangle','correct':'Retângulo'},
         ],'explanation':'Triângulo→3 lados; Hexágono Regular→6 lados; Retângulo→4 lados com 2 pares iguais.','xp':15},
    ]


def q_1_4():
    """Atividade 1.4 – Identificar figuras em objetos do cotidiano (MC)"""
    return [
        {'id':1,'type':'multiple_choice','question':'Uma pizza inteira tem o formato de qual figura geométrica?',
         'figure':None,'options':['Quadrado','Triângulo','Círculo','Hexágono'],'correct':2,
         'explanation':'A pizza tem formato circular — é um Círculo! Todos os pontos da borda estão à mesma distância do centro.','xp':10},
        {'id':2,'type':'multiple_choice','question':'Um azulejo de banheiro com todos os lados iguais e cantos em ângulo reto tem formato de qual figura?',
         'figure':None,'options':['Losango','Quadrado','Retângulo','Trapézio'],'correct':1,
         'explanation':'O Quadrado tem 4 lados iguais e 4 ângulos retos — como um azulejo padrão!','xp':10},
        {'id':3,'type':'multiple_choice','question':'Uma porta de casa (mais alta do que larga) tem formato de qual figura geométrica?',
         'figure':None,'options':['Quadrado','Trapézio','Losango','Retângulo'],'correct':3,
         'explanation':'Uma porta é um Retângulo: 4 ângulos retos, mas base ≠ altura.','xp':10},
        {'id':4,'type':'multiple_choice','question':'As células de um favo de mel de abelha têm o formato de qual figura?',
         'figure':None,'options':['Triângulo','Quadrado','Hexágono Regular','Círculo'],'correct':2,
         'explanation':'Os favos de mel têm formato de Hexágono Regular — 6 lados iguais que encaixam perfeitamente sem deixar espaço!','xp':10},
        {'id':5,'type':'multiple_choice','question':'Uma placa de trânsito de "DÊ A PREFERÊNCIA" (triângulo invertido) tem o formato de qual figura?',
         'figure':None,'options':['Trapézio','Losango','Triângulo','Retângulo'],'correct':2,
         'explanation':'Placas de preferência têm formato de Triângulo — 3 lados e 3 vértices.','xp':10},
    ]


def q_1_5():
    """Atividade 1.5 – Quiz cronometrado (MC com timer)"""
    return [
        {'id':1,'type':'multiple_choice','question':'Identifique rapidamente: qual é esta figura?',
         'figure':'rhombus','options':['Retângulo','Losango','Trapézio','Quadrado'],'correct':1,
         'explanation':'Losango: 4 lados iguais mas ângulos não retos.','xp':15,'timed':True,'time_limit':15},
        {'id':2,'type':'multiple_choice','question':'Identifique rapidamente: qual é esta figura?',
         'figure':'equilateral_triangle','options':['Triângulo Equilátero','Trapézio','Losango','Triângulo'],'correct':0,
         'explanation':'Triângulo Equilátero: 3 lados e 3 ângulos iguais (60° cada).','xp':15,'timed':True,'time_limit':15},
        {'id':3,'type':'multiple_choice','question':'Identifique rapidamente: qual é esta figura?',
         'figure':'trapezoid','options':['Retângulo','Losango','Quadrado','Trapézio'],'correct':3,
         'explanation':'Trapézio: 4 lados, com exatamente 1 par de lados paralelos.','xp':15,'timed':True,'time_limit':15},
        {'id':4,'type':'multiple_choice','question':'Identifique rapidamente: qual é esta figura?',
         'figure':'rectangle','options':['Losango','Retângulo','Trapézio','Quadrado'],'correct':1,
         'explanation':'Retângulo: 4 ângulos retos, mas base ≠ altura (diferente do quadrado).','xp':15,'timed':True,'time_limit':15},
        {'id':5,'type':'multiple_choice','question':'Identifique rapidamente: qual é esta figura?',
         'figure':'hexagon','options':['Pentágono','Octógono','Hexágono Regular','Losango'],'correct':2,
         'explanation':'Hexágono Regular: 6 lados iguais, 6 ângulos de 120°.','xp':15,'timed':True,'time_limit':15},
    ]

# ─────────────────────────────────────────────────────────────────
#  UNIT 2 — CARACTERÍSTICAS DAS FIGURAS
# ─────────────────────────────────────────────────────────────────

def q_2_1():
    """Atividade 2.1 – Contar lados e vértices (fill-blank)"""
    return [
        {'id':1,'type':'fill_blank','question':'O Quadrado possui quantos lados?',
         'figure':'square','answer':'4','hint':'Conte as arestas do quadrado',
         'explanation':'O Quadrado tem exatamente 4 lados iguais e 4 vértices.','xp':10},
        {'id':2,'type':'fill_blank','question':'O Triângulo possui quantos vértices?',
         'figure':'triangle','answer':'3','hint':'Vértice = ponto de encontro de dois lados',
         'explanation':'O Triângulo tem 3 vértices — os três "cantos" da figura.','xp':10},
        {'id':3,'type':'fill_blank','question':'O Hexágono Regular possui quantos lados?',
         'figure':'hexagon','answer':'6','hint':'Hexa = seis em grego',
         'explanation':'Hexa significa seis: o Hexágono Regular tem 6 lados iguais.','xp':10},
        {'id':4,'type':'fill_blank','question':'O Círculo possui quantos lados retos?',
         'figure':'circle','answer':'0','hint':'O círculo é completamente arredondado',
         'explanation':'O Círculo não tem lados nem vértices — apenas raio, diâmetro e circunferência.','xp':10},
        {'id':5,'type':'fill_blank','question':'O Losango possui quantos vértices?',
         'figure':'rhombus','answer':'4','hint':'Vértice = ponto de encontro de dois lados',
         'explanation':'O Losango tem 4 vértices — os 4 "pontas" da figura.','xp':10},
    ]


def q_2_2():
    """Atividade 2.2 – Associar elementos à figura correta (drag-drop texto→texto)"""
    return [
        {'id':1,'type':'drag_drop',
         'question':'Associe cada elemento geométrico à sua definição',
         'items':['Base','Altura','Raio'],
         'targets':[
             {'id':'base','text':'Lado inferior de uma figura geométrica','correct':'Base'},
             {'id':'altura','text':'Distância perpendicular entre a base e o lado/vértice oposto','correct':'Altura'},
             {'id':'raio','text':'Distância do centro ao perímetro do círculo','correct':'Raio'},
         ],'explanation':'Base, altura e raio são elementos fundamentais para calcular áreas.','xp':15},
        {'id':2,'type':'drag_drop',
         'question':'Associe cada figura ao seu elemento característico',
         'items':['Círculo','Losango','Trapézio'],
         'targets':[
             {'id':'ci','text':'Possui raio (r) e diâmetro (d = 2r)','correct':'Círculo'},
             {'id':'rh','text':'Possui diagonal maior (D) e diagonal menor (d)','correct':'Losando'},
             {'id':'tp','text':'Possui base maior (B) e base menor (b)','correct':'Trapézio'},
         ],'explanation':'Losango→diagonais; Trapézio→duas bases; Círculo→raio.','xp':15},
        {'id':3,'type':'drag_drop',
         'question':'Associe cada definição ao elemento correto',
         'items':['Lado (l)','Diagonal maior (D)','Base maior (B)'],
         'targets':[
             {'id':'sq','text':'Medida de um dos lados iguais do quadrado','correct':'Lado (l)'},
             {'id':'rh','text':'A maior das duas diagonais do losango','correct':'Diagonal maior (D)'},
             {'id':'tp','text':'O lado mais longo e paralelo ao outro no trapézio','correct':'Base maior (B)'},
         ],'explanation':'Cada figura tem seus elementos nomeados de forma específica.','xp':15},
        {'id':4,'type':'drag_drop',
         'question':'Qual elemento pertence a cada figura?',
         'items':['Vértice','Ângulo reto (90°)','Lado igual ao oposto'],
         'targets':[
             {'id':'tr','text':'Ponto onde dois lados do triângulo se encontram','correct':'Vértice'},
             {'id':'re','text':'Característica de todos os ângulos do retângulo','correct':'Ângulo reto (90°)'},
             {'id':'rh','text':'Todos os 4 lados do losango possuem esta propriedade','correct':'Lado igual ao oposto'},
         ],'explanation':'Triângulo→vértices; Retângulo→4 ângulos retos; Losango→4 lados iguais.','xp':15},
        {'id':5,'type':'drag_drop',
         'question':'Associe o elemento ao número correto de lados da figura',
         'items':['Triângulo Equilátero','Hexágono Regular','Círculo'],
         'targets':[
             {'id':'t3','text':'3 lados iguais','correct':'Triângulo Equilátero'},
             {'id':'h6','text':'6 lados iguais','correct':'Hexágono Regular'},
             {'id':'c0','text':'0 lados (curva fechada)','correct':'Círculo'},
         ],'explanation':'Triângulo Equilátero→3 lados; Hexágono→6 lados; Círculo→0 lados.','xp':15},
    ]


def q_2_3():
    """Atividade 2.3 – Classificar figuras por número de lados (drag-drop)"""
    return [
        {'id':1,'type':'drag_drop',
         'question':'Arraste cada figura para a categoria com o número correto de lados',
         'items':['Triângulo','Quadrado','Círculo'],
         'targets':[
             {'id':'c3','text':'3 lados','correct':'Triângulo'},
             {'id':'c4','text':'4 lados','correct':'Quadrado'},
             {'id':'c0','text':'0 lados','correct':'Círculo'},
         ],'explanation':'Triângulo→3; Quadrado→4; Círculo→0 lados.','xp':15},
        {'id':2,'type':'drag_drop',
         'question':'Arraste cada figura para a categoria com o número correto de lados',
         'items':['Hexágono Regular','Retângulo','Triângulo Equilátero'],
         'targets':[
             {'id':'c6','text':'6 lados','correct':'Hexágono Regular'},
             {'id':'c4','text':'4 lados','correct':'Retângulo'},
             {'id':'c3','text':'3 lados','correct':'Triângulo Equilátero'},
         ],'explanation':'Hexágono→6; Retângulo→4; Triângulo Equilátero→3 lados.','xp':15},
        {'id':3,'type':'drag_drop',
         'question':'Arraste cada figura para a categoria com o número correto de lados',
         'items':['Trapézio','Círculo','Losango'],
         'targets':[
             {'id':'c4a','text':'4 lados','correct':'Trapézio'},
             {'id':'c0a','text':'0 lados','correct':'Círculo'},
             {'id':'c4b','text':'4 lados iguais','correct':'Losando'},
         ],'explanation':'Trapézio e Losango têm 4 lados; Círculo não tem lados.','xp':15},
        {'id':4,'type':'drag_drop',
         'question':'Quais figuras têm 4 lados? Arraste-as para a categoria correta',
         'items':['Quadrado','Triângulo','Trapézio'],
         'targets':[
             {'id':'c4c','text':'4 lados','correct':'Quadrado'},
             {'id':'c3a','text':'3 lados','correct':'Triângulo'},
             {'id':'c4d','text':'4 lados (um par paralelo)','correct':'Trapézio'},
         ],'explanation':'Quadrado e Trapézio têm 4 lados; Triângulo tem apenas 3.','xp':15},
        {'id':5,'type':'drag_drop',
         'question':'Classifique as figuras pela quantidade de lados',
         'items':['Hexágono Regular','Losango','Círculo'],
         'targets':[
             {'id':'c6a','text':'6 lados iguais','correct':'Hexágono Regular'},
             {'id':'c4e','text':'4 lados iguais','correct':'Losando'},
             {'id':'c0b','text':'Sem lados','correct':'Círculo'},
         ],'explanation':'Hexágono→6 lados; Losango→4 lados iguais; Círculo→sem lados.','xp':15},
    ]


def q_2_4():
    """Atividade 2.4 – Comparar duas figuras (MC)"""
    return [
        {'id':1,'type':'multiple_choice','question':'Qual é a principal diferença entre o QUADRADO e o RETÂNGULO?',
         'figure':None,
         'options':['O quadrado tem mais lados','No quadrado todos os lados são iguais; no retângulo apenas os lados opostos são iguais','O retângulo não tem ângulos retos','Não há diferença entre eles'],'correct':1,
         'explanation':'Ambos têm 4 ângulos retos, mas no Quadrado todos os 4 lados são iguais; no Retângulo só os lados opostos são iguais (base ≠ altura).','xp':10},
        {'id':2,'type':'multiple_choice','question':'O que o LOSANGO e o QUADRADO têm em COMUM?',
         'figure':None,
         'options':['Ambos têm ângulos retos','Ambos têm 4 lados iguais','Ambos têm diagonais iguais','Ambos têm 3 vértices'],'correct':1,
         'explanation':'Losango e Quadrado têm os 4 lados iguais. A diferença: o Quadrado tem 4 ângulos retos; o Losango tem ângulos oblíquos.','xp':10},
        {'id':3,'type':'multiple_choice','question':'Qual a diferença entre o TRIÂNGULO e o TRIÂNGULO EQUILÁTERO?',
         'figure':None,
         'options':['O triângulo equilátero tem 4 lados','No triângulo equilátero os 3 lados são iguais; no triângulo comum podem ser diferentes','O triângulo comum tem mais vértices','Não há diferença'],
         'correct':1,'explanation':'Todo triângulo tem 3 lados, mas no Equilátero todos os 3 lados são iguais e os 3 ângulos medem 60°.','xp':10},
        {'id':4,'type':'multiple_choice','question':'O TRAPÉZIO e o RETÂNGULO são diferentes porque:',
         'figure':None,
         'options':['O trapézio tem mais lados','O trapézio tem apenas 1 par de lados paralelos; o retângulo tem 2 pares e 4 ângulos retos','O retângulo não tem lados paralelos','O trapézio tem ângulos retos'],
         'correct':1,'explanation':'Retângulo tem 2 pares de lados paralelos e 4 ângulos retos. Trapézio tem apenas 1 par de lados paralelos.','xp':10},
        {'id':5,'type':'multiple_choice','question':'O que SOMENTE o CÍRCULO possui, que nenhuma outra figura plana tem?',
         'figure':None,
         'options':['Vértices','Diagonais','Raio e ausência de lados retos','Ângulos retos'],
         'correct':2,'explanation':'O Círculo é a única figura plana sem lados retos ou vértices. Ele possui raio, diâmetro e circunferência.','xp':10},
    ]


def q_2_5():
    """Atividade 2.5 – Selecionar a descrição correta da figura (MC)"""
    return [
        {'id':1,'type':'multiple_choice','question':'Qual das opções DESCREVE CORRETAMENTE o Losango?',
         'figure':'rhombus',
         'options':['4 lados iguais e 4 ângulos retos (90°)','4 lados iguais com ângulos opostos iguais (não necessariamente retos)','3 lados iguais e 3 ângulos de 60°','4 lados com apenas um par paralelo'],
         'correct':1,'explanation':'O Losango tem 4 lados iguais, mas os ângulos são oblíquos (não retos). Os ângulos opostos são iguais.','xp':10},
        {'id':2,'type':'multiple_choice','question':'Qual das opções DESCREVE CORRETAMENTE o Trapézio?',
         'figure':'trapezoid',
         'options':['4 lados iguais e 4 ângulos retos','3 lados e 3 vértices','4 lados com exatamente 1 par de lados paralelos (base maior B e base menor b)','6 lados iguais'],
         'correct':2,'explanation':'O Trapézio tem 4 lados, mas apenas 1 par de lados paralelos: a base maior (B) e a base menor (b).','xp':10},
        {'id':3,'type':'multiple_choice','question':'Qual das opções DESCREVE CORRETAMENTE o Triângulo Equilátero?',
         'figure':'equilateral_triangle',
         'options':['3 lados, todos de medidas diferentes','3 lados iguais e 3 ângulos de 60° cada','3 lados e 4 vértices','3 lados com um ângulo de 90°'],
         'correct':1,'explanation':'No Triângulo Equilátero, os 3 lados são iguais e os 3 ângulos medem 60°. A soma dos ângulos é 180°.','xp':10},
        {'id':4,'type':'multiple_choice','question':'Qual das opções DESCREVE CORRETAMENTE o Círculo?',
         'figure':'circle',
         'options':['Figura com 4 lados curvos','Figura plana fechada onde todos os pontos estão à mesma distância (raio) do centro','Figura com 6 lados arredondados','Figura com 3 vértices arredondados'],
         'correct':1,'explanation':'O Círculo é uma figura plana fechada. Todos os seus pontos estão à mesma distância do centro — essa distância é o raio (r).','xp':10},
        {'id':5,'type':'multiple_choice','question':'Qual das opções DESCREVE CORRETAMENTE o Hexágono Regular?',
         'figure':'hexagon',
         'options':['5 lados iguais e 5 ângulos de 108°','6 lados iguais e 6 ângulos de 120° cada','6 lados desiguais','4 lados com diagonais iguais'],
         'correct':1,'explanation':'O Hexágono Regular tem 6 lados iguais e 6 ângulos internos de 120°. A soma dos ângulos é 720°.','xp':10},
    ]

# ─────────────────────────────────────────────────────────────────
#  UNIT 3 — FÓRMULAS DE ÁREA
# ─────────────────────────────────────────────────────────────────

def q_3_1():
    """Atividade 3.1 – Completar fórmulas (fill-blank)"""
    return [
        {'id':1,'type':'fill_blank','question':'A fórmula da área do Quadrado é A = l___\n(onde l = lado)',
         'figure':'square','answer':'l^2','hint':'Lado vezes lado = l ao quadrado',
         'explanation':'A = l² significa que multiplicamos o lado por ele mesmo. Ex: l=5 → A = 5² = 25 cm².','xp':10},
        {'id':2,'type':'fill_blank','question':'A fórmula da área do Triângulo é A = (b × h) / ___\n(onde b = base, h = altura)',
         'figure':'triangle','answer':'2','hint':'A área do triângulo é metade do retângulo de mesma base e altura',
         'explanation':'A = (b × h) / 2. Dividimos por 2 porque o triângulo ocupa metade do retângulo de mesma base e altura.','xp':10},
        {'id':3,'type':'fill_blank','question':'A fórmula da área do Círculo é A = ___ × r²\n(onde r = raio)',
         'figure':'circle','answer':'pi','hint':'É uma constante que começa com a letra grega π (pi)',
         'explanation':'A = π × r². O valor de π ≈ 3,14159. Ele representa a relação entre a circunferência e o diâmetro.','xp':10},
        {'id':4,'type':'fill_blank','question':'A fórmula da área do Retângulo é A = b × ___\n(onde b = base)',
         'figure':'rectangle','answer':'h','hint':'O outro elemento além da base é a...',
         'explanation':'A = b × h (base vezes altura). No retângulo, base e altura são perpendiculares entre si.','xp':10},
        {'id':5,'type':'fill_blank','question':'A fórmula da área do Trapézio é A = ((B + b) × h) / ___\n(onde B = base maior, b = base menor, h = altura)',
         'figure':'trapezoid','answer':'2','hint':'A média das bases, vezes a altura',
         'explanation':'A = ((B + b) × h) / 2. Calculamos a média das duas bases e multiplicamos pela altura.','xp':10},
    ]


def q_3_2():
    """Atividade 3.2 – Relacionar figura à fórmula (memory-match)"""
    ALL_PAIRS = [
        {'left':{'kind':'figure','value':'square'},     'right':{'kind':'text','value':'A = l²'}},
        {'left':{'kind':'figure','value':'rectangle'},  'right':{'kind':'text','value':'A = b × h'}},
        {'left':{'kind':'figure','value':'triangle'},   'right':{'kind':'text','value':'A = (b × h) / 2'}},
        {'left':{'kind':'figure','value':'circle'},     'right':{'kind':'text','value':'A = π × r²'}},
        {'left':{'kind':'figure','value':'rhombus'},    'right':{'kind':'text','value':'A = (D × d) / 2'}},
        {'left':{'kind':'figure','value':'trapezoid'},  'right':{'kind':'text','value':'A = ((B+b) × h) / 2'}},
        {'left':{'kind':'figure','value':'hexagon'},    'right':{'kind':'text','value':'A = (3√3 × l²) / 2'}},
        {'left':{'kind':'figure','value':'equilateral_triangle'},'right':{'kind':'text','value':'A = (l² × √3) / 4'}},
    ]
    return [
        {'id':1,'type':'memory_match','question':'Conecte cada figura à sua fórmula de área',
         'pairs':ALL_PAIRS[0:3],'explanation':'Quadrado→l²; Retângulo→b×h; Triângulo→(b×h)/2','xp':15},
        {'id':2,'type':'memory_match','question':'Conecte cada figura à sua fórmula de área',
         'pairs':ALL_PAIRS[2:5],'explanation':'Triângulo→(b×h)/2; Círculo→π×r²; Losango→(D×d)/2','xp':15},
        {'id':3,'type':'memory_match','question':'Conecte cada figura à sua fórmula de área',
         'pairs':ALL_PAIRS[3:6],'explanation':'Círculo→π×r²; Losango→(D×d)/2; Trapézio→((B+b)×h)/2','xp':15},
        {'id':4,'type':'memory_match','question':'Conecte cada figura à sua fórmula de área',
         'pairs':ALL_PAIRS[0:4],'explanation':'Revise as 4 primeiras fórmulas.','xp':20},
        {'id':5,'type':'memory_match','question':'DESAFIO: Conecte todas as figuras às suas fórmulas!',
         'pairs':ALL_PAIRS[0:5],'explanation':'Parabéns! Você domina as fórmulas das 5 figuras principais.','xp':25},
    ]


def q_3_3():
    """Atividade 3.3 – Identificar erros em fórmulas (MC)"""
    return [
        {'id':1,'type':'multiple_choice','question':'Qual fórmula está ERRADA para a área do Quadrado (lado = l)?',
         'figure':'square','options':['A = l²','A = l × l','A = l³','A = lado²'],'correct':2,
         'explanation':'A = l³ está errada porque eleva o lado ao cubo (tridimensional). A área é sempre l², não l³.','xp':10},
        {'id':2,'type':'multiple_choice','question':'Qual fórmula está ERRADA para a área do Triângulo (base b, altura h)?',
         'figure':'triangle','options':['A = (b × h) / 2','A = b × h / 2','A = b + h','A = ½ × b × h'],'correct':2,
         'explanation':'A = b + h está errada! Área nunca é uma soma de lados. A fórmula correta é A = (b × h) / 2.','xp':10},
        {'id':3,'type':'multiple_choice','question':'Qual fórmula está ERRADA para a área do Círculo (raio r)?',
         'figure':'circle','options':['A = π × r²','A = 3,14 × r²','A = π × r','A = π × (r²)'],'correct':2,
         'explanation':'A = π × r está errada porque falta o quadrado do raio. A fórmula correta é A = π × r².','xp':10},
        {'id':4,'type':'multiple_choice','question':'Qual fórmula está ERRADA para a área do Losango (diagonais D e d)?',
         'figure':'rhombus','options':['A = (D × d) / 2','A = D × d / 2','A = D + d','A = (D × d) ÷ 2'],'correct':2,
         'explanation':'A = D + d está errada! Somamos as diagonais apenas no trapézio (bases). No losango, multiplicamos: A = (D × d) / 2.','xp':10},
        {'id':5,'type':'multiple_choice','question':'Qual fórmula está ERRADA para a área do Trapézio (bases B, b e altura h)?',
         'figure':'trapezoid','options':['A = ((B + b) × h) / 2','A = (B + b) / 2 × h','A = B × h','A = (B + b) × h ÷ 2'],'correct':2,
         'explanation':'A = B × h ignora a base menor (b) e não divide por 2. A fórmula correta usa ambas as bases: A = ((B + b) × h) / 2.','xp':10},
    ]


def q_3_4():
    """Atividade 3.4 – Ordenar etapas do cálculo de área (order-steps)"""
    return [
        {'id':1,'type':'order_steps','question':'Ordene as etapas para calcular a área do QUADRADO com lado = 7 cm',
         'figure':'square',
         'steps':['Escreva o resultado com a unidade: A = 49 cm²',
                  'Identifique a figura: é um Quadrado',
                  'Aplique a fórmula: A = l² = 7²',
                  'Lembre a fórmula: A = l²'],
         'correct_order':[1,3,2,0],
         'explanation':'Passo a passo: 1) Identificar a figura → 2) Lembrar a fórmula → 3) Aplicar os valores → 4) Escrever o resultado.','xp':15},
        {'id':2,'type':'order_steps','question':'Ordene as etapas para calcular a área do RETÂNGULO (b=8 cm, h=5 cm)',
         'figure':'rectangle',
         'steps':['Calcule: A = 8 × 5 = 40 cm²',
                  'Anote a fórmula: A = b × h',
                  'Identifique os valores: b = 8 cm, h = 5 cm',
                  'Identifique a figura: é um Retângulo'],
         'correct_order':[3,2,1,0],
         'explanation':'Sempre identifique a figura, os valores, a fórmula e calcule o resultado.','xp':15},
        {'id':3,'type':'order_steps','question':'Ordene as etapas para calcular a área do TRIÂNGULO (b=10 cm, h=6 cm)',
         'figure':'triangle',
         'steps':['Resultado: A = 30 cm²',
                  'Substitua: A = (10 × 6) / 2',
                  'Fórmula do triângulo: A = (b × h) / 2',
                  'Multiplique e divida: A = 60 / 2 = 30'],
         'correct_order':[2,1,3,0],
         'explanation':'Triângulo: fórmula → substituição → cálculo (multiplicar e dividir por 2) → resultado.','xp':15},
        {'id':4,'type':'order_steps','question':'Ordene as etapas para calcular a área do TRAPÉZIO (B=12, b=8, h=5 cm)',
         'figure':'trapezoid',
         'steps':['Calcule a soma das bases: B + b = 12 + 8 = 20',
                  'Fórmula: A = ((B + b) × h) / 2',
                  'Resultado final: A = 50 cm²',
                  'Multiplique pela altura e divida por 2: A = (20 × 5) / 2 = 50'],
         'correct_order':[1,0,3,2],
         'explanation':'Trapézio: fórmula → soma das bases → multiplica pela altura e divide por 2 → resultado.','xp':15},
        {'id':5,'type':'order_steps','question':'Ordene as etapas para calcular a área do CÍRCULO (r=4 cm)',
         'figure':'circle',
         'steps':['Use π ≈ 3,14 e calcule: A = 3,14 × 16 ≈ 50,24 cm²',
                  'Fórmula do círculo: A = π × r²',
                  'Calcule r²: 4² = 16',
                  'Identifique: é um círculo com raio r = 4 cm'],
         'correct_order':[3,1,2,0],
         'explanation':'Círculo: identificar → fórmula → calcular r² → multiplicar por π → resultado.','xp':15},
    ]


def q_3_5():
    """Atividade 3.5 – Quiz conceitual sobre fórmulas (MC)"""
    return [
        {'id':1,'type':'multiple_choice','question':'Na fórmula A = π × r², o que representa o "r"?',
         'figure':'circle','options':['Resultado da área','Raio do círculo','Retângulo','Razão entre as diagonais'],'correct':1,
         'explanation':'"r" representa o raio do círculo — a distância do centro à borda. O valor de π ≈ 3,14159.','xp':10},
        {'id':2,'type':'multiple_choice','question':'Na fórmula do Trapézio A = ((B + b) × h) / 2, o que são "B" e "b"?',
         'figure':'trapezoid','options':['Dois triângulos internos','Base e base — a maior (B) e a menor (b), que são paralelas','Diagonal maior e diagonal menor','Base e altura'],'correct':1,
         'explanation':'No trapézio, B é a base maior e b é a base menor. Ambas são paralelas entre si.','xp':10},
        {'id':3,'type':'multiple_choice','question':'Por que a fórmula do Triângulo tem "÷ 2"?',
         'figure':'triangle','options':['Porque tem 3 lados e dividimos por 3 menos 1','Porque o triângulo ocupa metade da área de um retângulo de mesma base e altura','Porque π divide por 2','Porque a unidade é quadrada'],
         'correct':1,'explanation':'Um retângulo com mesma base e altura do triângulo tem o dobro da área do triângulo. Por isso A = (b×h)/2.','xp':10},
        {'id':4,'type':'multiple_choice','question':'Na fórmula do Losango A = (D × d) / 2, o que são D e d?',
         'figure':'rhombus','options':['Diâmetro e distância','Diagonal maior e diagonal menor','Dois lados do losango','Dois ângulos opostos'],
         'correct':1,'explanation':'D é a diagonal maior e d é a diagonal menor do losango. As diagonais são as linhas que conectam os vértices opostos.','xp':10},
        {'id':5,'type':'multiple_choice','question':'Qual fórmula de área usa a RAIZ QUADRADA (√) em seu cálculo?',
         'figure':None,'options':['Quadrado: A = l²','Triângulo Equilátero: A = (l² × √3) / 4','Círculo: A = π × r²','Retângulo: A = b × h'],
         'correct':1,'explanation':'O Triângulo Equilátero usa √3 (raiz de 3 ≈ 1,732) na fórmula. Isso vem da geometria dos ângulos de 60°.','xp':10},
    ]

# ─────────────────────────────────────────────────────────────────
#  UNIT 4 — CÁLCULO DE ÁREAS
# ─────────────────────────────────────────────────────────────────

def q_4_1():
    """Atividade 4.1 – Cálculo guiado com dica (fill-blank)"""
    return [
        {'id':1,'type':'fill_blank',
         'question':'QUADRADO com lado = 6 cm\nFórmula: A = l² = 6² = ?\nQual é a área em cm²?',
         'figure':'square','answer':'36','hint':'6 × 6 = ?',
         'explanation':'A = l² = 6² = 6 × 6 = 36 cm²','xp':10},
        {'id':2,'type':'fill_blank',
         'question':'RETÂNGULO com base = 10 cm e altura = 4 cm\nFórmula: A = b × h = 10 × 4 = ?\nQual é a área em cm²?',
         'figure':'rectangle','answer':'40','hint':'10 × 4 = ?',
         'explanation':'A = b × h = 10 × 4 = 40 cm²','xp':10},
        {'id':3,'type':'fill_blank',
         'question':'TRIÂNGULO com base = 8 cm e altura = 5 cm\nFórmula: A = (b × h) / 2 = (8 × 5) / 2 = ?\nQual é a área em cm²?',
         'figure':'triangle','answer':'20','hint':'(8 × 5) = 40 → 40 ÷ 2 = ?',
         'explanation':'A = (b × h) / 2 = (8 × 5) / 2 = 40 / 2 = 20 cm²','xp':10},
        {'id':4,'type':'fill_blank',
         'question':'CÍRCULO com raio = 3 cm (use π ≈ 3,14)\nFórmula: A = π × r² = 3,14 × 3² = 3,14 × 9 = ?\nQual é a área em cm²?',
         'figure':'circle','answer':'28.26','hint':'3,14 × 9 = ?',
         'explanation':'A = π × r² = 3,14 × 3² = 3,14 × 9 = 28,26 cm²','xp':10},
        {'id':5,'type':'fill_blank',
         'question':'LOSANGO com diagonal maior D = 12 cm e diagonal menor d = 8 cm\nFórmula: A = (D × d) / 2 = (12 × 8) / 2 = ?\nQual é a área em cm²?',
         'figure':'rhombus','answer':'48','hint':'(12 × 8) = 96 → 96 ÷ 2 = ?',
         'explanation':'A = (D × d) / 2 = (12 × 8) / 2 = 96 / 2 = 48 cm²','xp':10},
    ]


def q_4_2():
    """Atividade 4.2 – Cálculo direto sem auxílio (fill-blank, valores aleatórios)"""
    def sq():
        l = random.randint(4,14)
        return {'id':1,'type':'fill_blank',
                'question':f'Calcule a área do QUADRADO com lado = {l} cm.',
                'figure':'square','answer':str(l*l),'hint':f'Fórmula: A = l² = {l}²',
                'explanation':f'A = l² = {l}² = {l*l} cm²','xp':12}
    def rect():
        b,h = random.randint(3,12),random.randint(2,10)
        return {'id':2,'type':'fill_blank',
                'question':f'Calcule a área do RETÂNGULO com base = {b} cm e altura = {h} cm.',
                'figure':'rectangle','answer':str(b*h),'hint':f'Fórmula: A = b × h',
                'explanation':f'A = b × h = {b} × {h} = {b*h} cm²','xp':12}
    def tri():
        b,h = random.randint(4,16),random.randint(3,12)
        a = b*h//2
        return {'id':3,'type':'fill_blank',
                'question':f'Calcule a área do TRIÂNGULO com base = {b} cm e altura = {h} cm.',
                'figure':'triangle','answer':str(a),'hint':'Fórmula: A = (b × h) / 2',
                'explanation':f'A = (b × h) / 2 = ({b} × {h}) / 2 = {b*h} / 2 = {a} cm²','xp':12}
    def trap():
        B,b,h = random.randint(8,16),random.randint(3,7),random.randint(4,10)
        a = (B+b)*h//2
        return {'id':4,'type':'fill_blank',
                'question':f'Calcule a área do TRAPÉZIO com B = {B} cm, b = {b} cm e h = {h} cm.',
                'figure':'trapezoid','answer':str(a),'hint':'Fórmula: A = ((B + b) × h) / 2',
                'explanation':f'A = (({B}+{b})×{h})/2 = ({B+b}×{h})/2 = {(B+b)*h}/2 = {a} cm²','xp':12}
    def rh():
        D,d = random.randint(6,18),random.randint(4,12)
        a = D*d//2
        return {'id':5,'type':'fill_blank',
                'question':f'Calcule a área do LOSANGO com D = {D} cm e d = {d} cm.',
                'figure':'rhombus','answer':str(a),'hint':'Fórmula: A = (D × d) / 2',
                'explanation':f'A = (D×d)/2 = ({D}×{d})/2 = {D*d}/2 = {a} cm²','xp':12}
    return [sq(), rect(), tri(), trap(), rh()]


def q_4_3():
    """Atividade 4.3 – Problemas contextualizados simples (fill-blank)"""
    return [
        {'id':1,'type':'fill_blank',
         'question':'Uma sala tem o piso em formato de RETÂNGULO com 7 m de base e 5 m de altura.\nQual é a área do piso em m²?',
         'figure':'rectangle','answer':'35','hint':'A = b × h',
         'explanation':'A = b × h = 7 × 5 = 35 m². Essa é a quantidade de material necessário para cobrir o piso.','xp':12},
        {'id':2,'type':'fill_blank',
         'question':'Um terreno QUADRADO tem lado de 9 m.\nQual é a área do terreno em m²?',
         'figure':'square','answer':'81','hint':'A = l²',
         'explanation':'A = l² = 9² = 81 m². Um terreno de 81 metros quadrados.','xp':12},
        {'id':3,'type':'fill_blank',
         'question':'Uma placa triangular de sinalização tem base = 60 cm e altura = 52 cm.\nQual é a área da placa em cm²?',
         'figure':'triangle','answer':'1560','hint':'A = (b × h) / 2',
         'explanation':'A = (b × h) / 2 = (60 × 52) / 2 = 3120 / 2 = 1560 cm²','xp':12},
        {'id':4,'type':'fill_blank',
         'question':'Um espelho circular tem raio = 25 cm. Use π ≈ 3,14.\nQual é a área do espelho em cm²?',
         'figure':'circle','answer':'1962.5','hint':'A = π × r²; 3,14 × 625 = ?',
         'explanation':'A = π × r² = 3,14 × 25² = 3,14 × 625 = 1962,5 cm²','xp':12},
        {'id':5,'type':'fill_blank',
         'question':'Uma pipa tem formato de LOSANGO com diagonal maior D = 80 cm e diagonal menor d = 50 cm.\nQual é a área da pipa em cm²?',
         'figure':'rhombus','answer':'2000','hint':'A = (D × d) / 2',
         'explanation':'A = (D × d) / 2 = (80 × 50) / 2 = 4000 / 2 = 2000 cm²','xp':12},
    ]


def q_4_4():
    """Atividade 4.4 – Problemas com múltiplas etapas (fill-blank)"""
    return [
        {'id':1,'type':'fill_blank',
         'question':'Uma sala RETANGULAR tem 6 m de base e 4 m de altura.\nO piso custa R$ 50,00/m².\nQual é o custo total do piso? (em R$)',
         'figure':'rectangle','answer':'1200','hint':'Passo 1: Área = 6 × 4. Passo 2: custo = Área × 50',
         'explanation':'Área = 6 × 4 = 24 m². Custo = 24 × R$50 = R$1200,00','xp':15},
        {'id':2,'type':'fill_blank',
         'question':'Um jardim TRIANGULAR tem base = 14 m e altura = 10 m.\nUm saco de adubo cobre 5 m².\nQuantos sacos são necessários?',
         'figure':'triangle','answer':'14','hint':'Passo 1: Área = (14 × 10) / 2. Passo 2: sacos = Área ÷ 5',
         'explanation':'Área = (14 × 10) / 2 = 70 m². Sacos = 70 ÷ 5 = 14 sacos','xp':15},
        {'id':3,'type':'fill_blank',
         'question':'Um QUADRADO tem perímetro de 32 cm.\nQual é a ÁREA desse quadrado em cm²?',
         'figure':'square','answer':'64','hint':'Passo 1: lado = perímetro ÷ 4. Passo 2: A = l²',
         'explanation':'Perímetro = 4 × lado → lado = 32 ÷ 4 = 8 cm. Área = 8² = 64 cm²','xp':15},
        {'id':4,'type':'fill_blank',
         'question':'Um TRAPÉZIO tem B = 15 m, b = 9 m e altura = 8 m.\nQual é a área em m²?',
         'figure':'trapezoid','answer':'96','hint':'A = ((B + b) × h) / 2',
         'explanation':'A = ((15 + 9) × 8) / 2 = (24 × 8) / 2 = 192 / 2 = 96 m²','xp':15},
        {'id':5,'type':'fill_blank',
         'question':'Uma janela CIRCULAR tem diâmetro = 1,2 m. Use π ≈ 3,14.\nQual é a área da janela em m²? (2 decimais)',
         'figure':'circle','answer':'1.13','hint':'Raio = diâmetro ÷ 2. A = π × r²',
         'explanation':'r = 1,2 ÷ 2 = 0,6 m. A = 3,14 × 0,6² = 3,14 × 0,36 ≈ 1,13 m²','xp':15},
    ]


def q_4_5():
    """Atividade 4.5 – Desafio cronometrado (MC com timer e valores aleatórios)"""
    def make_sq(qid):
        l = random.randint(3,12)
        correct = l*l
        wrong = [correct+l, correct-l, l*2]
        opts = sorted(set([correct]+wrong[:3]))
        random.shuffle(opts)
        return {'id':qid,'type':'multiple_choice',
                'question':f'Qual é a área do QUADRADO com lado = {l} cm?',
                'figure':'square','options':[str(v)+' cm²' for v in opts],
                'correct':opts.index(correct),
                'explanation':f'A = l² = {l}² = {correct} cm²','xp':15,'timed':True,'time_limit':20}
    def make_rect(qid):
        b,h = random.randint(4,12),random.randint(3,9)
        correct = b*h
        wrong = [b+h, b*h+b, b*h-h]
        opts = sorted(set([correct]+wrong[:3]))
        random.shuffle(opts)
        return {'id':qid,'type':'multiple_choice',
                'question':f'Qual é a área do RETÂNGULO com base = {b} cm e h = {h} cm?',
                'figure':'rectangle','options':[str(v)+' cm²' for v in opts],
                'correct':opts.index(correct),
                'explanation':f'A = b×h = {b}×{h} = {correct} cm²','xp':15,'timed':True,'time_limit':20}
    def make_tri(qid):
        b,h = random.randint(6,16),random.randint(4,12)
        correct = b*h//2
        wrong = [b*h, correct+b, correct-h//2]
        opts = sorted(set([correct]+wrong[:3]))
        random.shuffle(opts)
        return {'id':qid,'type':'multiple_choice',
                'question':f'Qual é a área do TRIÂNGULO com base = {b} cm e h = {h} cm?',
                'figure':'triangle','options':[str(v)+' cm²' for v in opts],
                'correct':opts.index(correct),
                'explanation':f'A = (b×h)/2 = ({b}×{h})/2 = {correct} cm²','xp':15,'timed':True,'time_limit':20}
    return [make_sq(1), make_rect(2), make_tri(3), make_sq(4), make_rect(5)]

# ─────────────────────────────────────────────────────────────────
#  UNIT 5 — DESAFIOS INTEGRADORES
# ─────────────────────────────────────────────────────────────────

def q_5_1():
    """Atividade 5.1 – Identificar figura + calcular área (MC)"""
    return [
        {'id':1,'type':'multiple_choice',
         'question':'Uma figura tem 4 lados iguais e 4 ângulos retos. Seu lado mede 11 cm.\nQual é a área dessa figura?',
         'figure':None,'options':['121 cm²','44 cm²','22 cm²','111 cm²'],'correct':0,
         'explanation':'A figura é um Quadrado (4 lados iguais + ângulos retos). A = l² = 11² = 121 cm²','xp':20},
        {'id':2,'type':'multiple_choice',
         'question':'Uma figura tem 0 lados e seu raio mede 5 cm. Use π ≈ 3,14.\nQual é a área dessa figura?',
         'figure':None,'options':['78,5 cm²','31,4 cm²','25 cm²','15,7 cm²'],'correct':0,
         'explanation':'A figura é um Círculo (0 lados, tem raio). A = π×r² = 3,14×5² = 3,14×25 = 78,5 cm²','xp':20},
        {'id':3,'type':'multiple_choice',
         'question':'Uma figura tem 3 lados iguais. Sua base mede 10 cm e altura mede 8,66 cm.\nQual é a área?',
         'figure':None,'options':['43,3 cm²','86,6 cm²','30 cm²','25 cm²'],'correct':0,
         'explanation':'A figura é um Triângulo Equilátero. A = (b×h)/2 = (10×8,66)/2 = 86,6/2 = 43,3 cm²','xp':20},
        {'id':4,'type':'multiple_choice',
         'question':'Uma figura tem 4 lados iguais e suas diagonais medem D = 20 cm e d = 14 cm.\nQual é a área?',
         'figure':None,'options':['140 cm²','280 cm²','68 cm²','70 cm²'],'correct':0,
         'explanation':'A figura é um Losango (4 lados iguais, identificado pelas diagonais). A = (D×d)/2 = (20×14)/2 = 280/2 = 140 cm²','xp':20},
        {'id':5,'type':'multiple_choice',
         'question':'Um campo de futebol RETANGULAR tem 105 m de comprimento e 68 m de largura.\nQual é a área do campo?',
         'figure':None,'options':['7140 m²','346 m²','3570 m²','14280 m²'],'correct':0,
         'explanation':'Campo retangular: A = b × h = 105 × 68 = 7140 m²','xp':20},
    ]


def q_5_2():
    """Atividade 5.2 – Problemas do cotidiano (fill-blank)"""
    return [
        {'id':1,'type':'fill_blank',
         'question':'Você quer cobrir o piso de uma cozinha QUADRADA com lado = 4,5 m com cerâmica.\nQual é a área do piso em m²?',
         'figure':'square','answer':'20.25','hint':'A = l²; 4,5² = 4,5 × 4,5',
         'explanation':'A = l² = 4,5² = 20,25 m². Você precisará de pelo menos 20,25 m² de cerâmica.','xp':20},
        {'id':2,'type':'fill_blank',
         'question':'Uma parede RETANGULAR de 3 m de altura e 5 m de largura será pintada.\nUma lata de tinta cobre 8 m².\nQuantas latas serão necessárias?',
         'figure':'rectangle','answer':'2','hint':'Passo 1: Área = 5 × 3 = 15 m². Passo 2: latas = ceil(15 ÷ 8)',
         'explanation':'Área = 5 × 3 = 15 m². 15 ÷ 8 = 1,875 → arredonda para cima = 2 latas.','xp':20},
        {'id':3,'type':'fill_blank',
         'question':'Uma piscina circular tem raio = 4 m. Use π ≈ 3,14.\nQual é a área da superfície da água em m²?',
         'figure':'circle','answer':'50.24','hint':'A = π × r² = 3,14 × 4² = 3,14 × 16',
         'explanation':'A = π × r² = 3,14 × 16 = 50,24 m²','xp':20},
        {'id':4,'type':'fill_blank',
         'question':'Um telhado tem formato TRIANGULAR com base = 12 m e altura = 5 m.\nQual é a área do telhado em m²?',
         'figure':'triangle','answer':'30','hint':'A = (b × h) / 2',
         'explanation':'A = (b × h) / 2 = (12 × 5) / 2 = 60 / 2 = 30 m²','xp':20},
        {'id':5,'type':'fill_blank',
         'question':'Uma calçada trapezoidal tem B = 8 m, b = 5 m e h = 3 m.\nQual é a área da calçada em m²?',
         'figure':'trapezoid','answer':'19.5','hint':'A = ((B + b) × h) / 2',
         'explanation':'A = ((8 + 5) × 3) / 2 = (13 × 3) / 2 = 39 / 2 = 19,5 m²','xp':20},
    ]


def q_5_3():
    """Atividade 5.3 – Figuras combinadas (fill-blank)"""
    return [
        {'id':1,'type':'fill_blank',
         'question':'Uma figura é formada por um RETÂNGULO (b=10, h=6 cm) com um TRIÂNGULO (b=10, h=4 cm) no topo.\nQual é a área total em cm²?',
         'figure':None,'answer':'80','hint':'Área total = Área retângulo + Área triângulo',
         'explanation':'Retângulo: 10×6 = 60 cm². Triângulo: (10×4)/2 = 20 cm². Total = 60 + 20 = 80 cm²','xp':25},
        {'id':2,'type':'fill_blank',
         'question':'Um terreno QUADRADO (l=20 m) tem uma piscina CIRCULAR (r=5 m) no centro. Use π ≈ 3,14.\nQual é a área do terreno FORA da piscina em m²?',
         'figure':None,'answer':'321.5','hint':'Área fora = Área quadrado − Área círculo',
         'explanation':'Quadrado: 20² = 400 m². Círculo: 3,14×5² = 78,5 m². Fora = 400 − 78,5 = 321,5 m²','xp':25},
        {'id':3,'type':'fill_blank',
         'question':'Duas figuras iguais: dois TRIÂNGULOS com base = 8 cm e altura = 6 cm.\nQual é a área TOTAL dos dois triângulos em cm²?',
         'figure':None,'answer':'48','hint':'Área de 1 triângulo × 2',
         'explanation':'1 triângulo: (8×6)/2 = 24 cm². 2 triângulos: 24 × 2 = 48 cm²','xp':25},
        {'id':4,'type':'fill_blank',
         'question':'Uma bandeira tem 60 cm × 40 cm (RETÂNGULO) e um LOSANGO central com D=20 cm, d=12 cm.\nQual é a área da bandeira FORA do losango em cm²?',
         'figure':None,'answer':'2280','hint':'Área fora = Área retângulo − Área losango',
         'explanation':'Retângulo: 60×40 = 2400 cm². Losango: (20×12)/2 = 120 cm². Fora = 2400 − 120 = 2280 cm²','xp':25},
        {'id':5,'type':'fill_blank',
         'question':'Um parque tem formato de TRAPÉZIO (B=50 m, b=30 m, h=20 m) e dentro há um QUADRADO (l=10 m).\nQual é a área verde (fora do quadrado) em m²?',
         'figure':None,'answer':'700','hint':'Área verde = Área trapézio − Área quadrado',
         'explanation':'Trapézio: ((50+30)×20)/2 = 800 m². Quadrado: 10² = 100 m². Verde = 800 − 100 = 700 m²','xp':25},
    ]


def q_5_4():
    """Atividade 5.4 – Missão gamificada (MC com narrativa)"""
    return [
        {'id':1,'type':'multiple_choice',
         'question':'🚀 MISSÃO 1: Você é arquiteto e precisa cobrir o piso de uma sala QUADRADA com l = 8 m.\nUm porcelanato cobre 0,64 m² (40 cm × 40 cm). Quantas peças você precisa?',
         'figure':None,'options':['100 peças','64 peças','128 peças','50 peças'],'correct':0,
         'explanation':'Área da sala: 8² = 64 m². 64 ÷ 0,64 = 100 peças.','xp':25},
        {'id':2,'type':'multiple_choice',
         'question':'🎨 MISSÃO 2: Você vai pintar uma parede TRIANGULAR com b = 6 m e h = 4 m.\nTinta cobre 3 m² por litro. Quantos litros você precisa?',
         'figure':None,'options':['4 litros','12 litros','3 litros','6 litros'],'correct':0,
         'explanation':'Área: (6×4)/2 = 12 m². 12 ÷ 3 = 4 litros.','xp':25},
        {'id':3,'type':'multiple_choice',
         'question':'🌊 MISSÃO 3: Uma piscina RETANGULAR tem 15 m × 6 m. Você vai colocar uma lona sobre ela.\nA lona custa R$ 12,00/m². Qual é o custo total?',
         'figure':None,'options':['R$ 1.080,00','R$ 540,00','R$ 252,00','R$ 216,00'],'correct':0,
         'explanation':'Área: 15 × 6 = 90 m². Custo: 90 × R$12 = R$1.080,00','xp':25},
        {'id':4,'type':'multiple_choice',
         'question':'🏟️ MISSÃO 4: Um estádio tem uma área circular de gramado com raio = 50 m. Use π ≈ 3,14.\nQual é a área do gramado em m²?',
         'figure':None,'options':['7850 m²','15700 m²','314 m²','2500 m²'],'correct':0,
         'explanation':'A = π × r² = 3,14 × 50² = 3,14 × 2500 = 7850 m²','xp':25},
        {'id':5,'type':'multiple_choice',
         'question':'🏆 MISSÃO FINAL: Um TRAPÉZIO tem B = 25 m, b = 15 m e h = 12 m.\nEsse é o formato de um telhado. Quantos m² de telha são necessários?',
         'figure':None,'options':['240 m²','480 m²','300 m²','120 m²'],'correct':0,
         'explanation':'A = ((25+15)×12)/2 = (40×12)/2 = 480/2 = 240 m²','xp':25},
    ]


def q_5_5():
    """Atividade 5.5 – Avaliação final com questões mistas (MC)"""
    return [
        {'id':1,'type':'multiple_choice',
         'question':'[AVALIAÇÃO] Qual é a fórmula CORRETA para a área do Losango?',
         'figure':'rhombus','options':['A = D + d','A = (D × d) / 2','A = D × d','A = D² / d'],'correct':1,
         'explanation':'A = (D × d) / 2, onde D é a diagonal maior e d é a diagonal menor.','xp':20},
        {'id':2,'type':'multiple_choice',
         'question':'[AVALIAÇÃO] Um hexágono regular tem 6 lados, cada um com 4 cm. Qual das opções descreve corretamente essa figura?',
         'figure':'hexagon','options':['4 lados iguais e 4 ângulos retos','6 lados iguais e 6 ângulos de 120°','3 lados iguais e 3 ângulos de 60°','5 lados iguais'],'correct':1,
         'explanation':'O Hexágono Regular tem 6 lados iguais e 6 ângulos internos de 120°.','xp':20},
        {'id':3,'type':'multiple_choice',
         'question':'[AVALIAÇÃO] Um quadrado tem área = 144 cm². Qual é o valor do seu lado?',
         'figure':'square','options':['14 cm','72 cm','12 cm','36 cm'],'correct':2,
         'explanation':'A = l² → 144 = l² → l = √144 = 12 cm. O lado do quadrado é 12 cm.','xp':20},
        {'id':4,'type':'multiple_choice',
         'question':'[AVALIAÇÃO] Qual figura tem a fórmula A = (b × h) / 2?',
         'figure':None,'options':['Retângulo','Círculo','Triângulo','Trapézio'],'correct':2,
         'explanation':'A = (b × h) / 2 é a fórmula do Triângulo — dividimos por 2 porque o triângulo é metade de um retângulo.','xp':20},
        {'id':5,'type':'multiple_choice',
         'question':'[AVALIAÇÃO] Um círculo tem diâmetro = 10 cm. Usando π ≈ 3,14, qual é sua área?',
         'figure':'circle','options':['31,4 cm²','78,5 cm²','314 cm²','15,7 cm²'],'correct':1,
         'explanation':'Diâmetro = 10 → raio = 5 cm. A = π × r² = 3,14 × 5² = 3,14 × 25 = 78,5 cm²','xp':20},
    ]

# ─────────────────────────────────────────────────────────────────
#  DISPATCHER
# ─────────────────────────────────────────────────────────────────

_REGISTRY = {
    (1,1): q_1_1, (1,2): q_1_2, (1,3): q_1_3, (1,4): q_1_4, (1,5): q_1_5,
    (2,1): q_2_1, (2,2): q_2_2, (2,3): q_2_3, (2,4): q_2_4, (2,5): q_2_5,
    (3,1): q_3_1, (3,2): q_3_2, (3,3): q_3_3, (3,4): q_3_4, (3,5): q_3_5,
    (4,1): q_4_1, (4,2): q_4_2, (4,3): q_4_3, (4,4): q_4_4, (4,5): q_4_5,
    (5,1): q_5_1, (5,2): q_5_2, (5,3): q_5_3, (5,4): q_5_4, (5,5): q_5_5,
}

def get_questions(unit_id: int, activity_id: int) -> list:
    """Retorna lista de 5 questões para a unidade/atividade solicitada."""
    fn = _REGISTRY.get((unit_id, activity_id))
    return fn() if fn else []
