from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.agents.resume_agent import parse_resume
from app.agents.matcher_agent import match_resume
from app.agents.cover_agent import generate_cover
from app.utils.decision import decide
from app.utils.logger import get_logger

logger = get_logger("Supervisor")


def resume_node(state: AgentState):
    logger.info("Running Resume Agent")
    state["resume"] = parse_resume(state["resume"])
    return state


def match_node(state: AgentState):
    logger.info("Running Matcher Agent")

    raw = match_resume(state["resume"], state["job_description"])
    decision = decide(raw.raw_score, raw.missing_skills)

    state["match_score"] = decision.match_score
    state["verdict"] = decision.verdict
    state["missing_skills"] = decision.missing_skills

    return state


def cover_node(state: AgentState):
    logger.info("Running Cover Letter Agent")
    state["cover_letter"] = generate_cover(
        state["resume"], state["job_description"]
    )
    return state


def decision_router(state: AgentState):
    return "cover" if state["verdict"] == "apply" else END


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("resume", resume_node)
    graph.add_node("match", match_node)
    graph.add_node("cover", cover_node)

    graph.set_entry_point("resume")
    graph.add_edge("resume", "match")

    graph.add_conditional_edges(
        "match",
        decision_router,
        {"cover": "cover", END: END}
    )

    graph.add_edge("cover", END)

    return graph.compile()
