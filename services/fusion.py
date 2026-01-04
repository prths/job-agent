def fuse_scores(embedding_score: float, llm_score: float,
                w_embed=0.65, w_llm=0.35):
    """
    embedding_score: 0–1
    llm_score: 0–100
    """
    embed_100 = embedding_score * 100
    final = (w_embed * embed_100) + (w_llm * llm_score)
    return round(final, 2)

