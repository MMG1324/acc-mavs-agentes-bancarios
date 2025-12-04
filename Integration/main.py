from langgraph.graph import StateGraph, START, END
from settings.state import UserQueryState
from modelos.experto_faq.customer_agent import experto_faq
from modelos.routers.main_router import router_llm
from modelos.expertos_hipoteca.calculador_hipoteca import experto_calculador_hipotecas
from modelos.routers.router_hipotecas import router_hipotecas
from modelos.expertos_hipoteca.hipotecas_general import experto_hipotecario_general

g = StateGraph(UserQueryState)

g.add_node("router", router_llm)
g.add_node("faq", experto_faq)
g.add_node("hipotecas", router_hipotecas)
g.add_node("calculo_hip", experto_calculador_hipotecas)
g.add_node("general_hip", experto_hipotecario_general)

def decidir_experto(state: UserQueryState):
    return state["model"]

g.add_edge(START, "router")
g.add_conditional_edges("router", decidir_experto, ["faq", "hipotecas"])
g.add_edge("faq", END)
g.add_conditional_edges("hipotecas", decidir_experto, ["calculo_hip", "general_hip"])
g.add_edge("calculo_hip", END)
g.add_edge("general_hip", END)

app = g.compile()

if __name__ == "__main__":
    while(True):
        user_input = input("\nUser: ")
        ejemplo = {"input": user_input, "model": None, "output": None}
        res = app.invoke(ejemplo)

        print("\nModel: " + res['output'])

