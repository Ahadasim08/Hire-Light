from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    # The raw strings we extracted
    resume_markdown: str
    jd_markdown: str
    
    # Structured data populated by agents
    candidate_profile: dict  # Agent A fills this
    job_profile: dict        # Agent B fills this
    
    # The running log of thoughts/critiques
    # 'Annotated' with 'operator.add' tells LangGraph to APPEND new items 
    # to this list instead of overwriting it.
    evaluation_log: Annotated[List[str], operator.add]
    
    # Final decision summary
    decision_brief: str