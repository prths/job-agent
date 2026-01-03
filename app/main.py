from app.graph.supervisor import build_graph

def run_pipeline(resume: str, job_description: str):
    graph = build_graph()

    state = {
        "resume": resume,
        "job_description": job_description,
        "match_score": 0.0,
        "verdict": "",
        "cover_letter": ""
    }

    return graph.invoke(state)
