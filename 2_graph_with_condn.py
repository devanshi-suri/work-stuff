from typing import TypedDict, Literal
class PortfolioState(TypedDict):
    amount_usd: float
    total_usd: float
    target_curr: Literal['INR','EUR']
    total: float
def calc_total(state: PortfolioState) -> PortfolioState:
    state['total_usd'] = state['amount_usd'] * 1.08
    return state

def convert_to_inr(state: PortfolioState) -> PortfolioState:
    state['total'] = state['total_usd'] * 85.0
    return state
def convert_to_eur(state: PortfolioState) -> PortfolioState:
    state['total'] = state['total_usd'] * 0.9
    return state

def choose_conversion(state: PortfolioState) -> str:
    return state['target_curr']

from langgraph.graph import StateGraph, START, END
builder = StateGraph(PortfolioState)

builder.add_node('calc_total_node',calc_total)
builder.add_node('convert_to_inr_node',convert_to_inr)
builder.add_node('convert_to_eur_node',convert_to_eur)

builder.add_edge(START, 'calc_total_node')
builder.add_conditional_edges(
    "calc_total_node",
    choose_conversion,
    {'INR': 'convert_to_inr_node',
        'EUR': 'convert_to_eur_node'}
)
builder.add_edge(['convert_to_inr_node','convert_to_eur_node'],END)
graph = builder.compile()

from IPython.display import display,Image
display(Image(graph.get_graph().draw_mermaid_png()))

res = graph.invoke({'amount_usd':50, 'target_curr': "EUR"})
print(res)