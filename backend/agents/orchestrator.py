import time
from typing import Dict, Any
from .requirement_agent import RequirementUnderstandingAgent
from .filter_agent import CatalogSearchFilterAgent
from .comparison_agent import ProductComparisonAgent

class MultiAgentOrchestrator:
    def __init__(self):
        self.req_agent = RequirementUnderstandingAgent()
        self.filter_agent = CatalogSearchFilterAgent()
        self.comp_agent = ProductComparisonAgent()

    def run_pipeline(self, raw_requirement: str) -> Dict[str, Any]:
        start_time = time.time()
        pipeline_traces = []

        # Step 1: Analyze Requirements
        step1_res = self.req_agent.process(raw_requirement)
        pipeline_traces.append({
            "step": 1,
            "agent": step1_res["agent_name"],
            "role": step1_res["role"],
            "output_summary": f"Extracted category: {step1_res['parsed_constraints']['category']}, max_price: ${step1_res['parsed_constraints']['max_price'] or 'N/A'}",
            "thought_trace": step1_res["thought_trace"]
        })

        # Step 2: Search & Filter Catalog
        constraints = step1_res["parsed_constraints"]
        step2_res = self.filter_agent.process(constraints)
        pipeline_traces.append({
            "step": 2,
            "agent": step2_res["agent_name"],
            "role": step2_res["role"],
            "output_summary": f"Found {step2_res['candidate_count']} matching candidate product(s).",
            "thought_trace": step2_res["thought_trace"]
        })

        # Step 3: Compare & Recommend
        candidates = step2_res["candidates"]
        step3_res = self.comp_agent.process(candidates, raw_requirement, constraints)
        pipeline_traces.append({
            "step": 3,
            "agent": step3_res["agent_name"],
            "role": step3_res["role"],
            "output_summary": f"Top winner selected: {step3_res.get('winner_overall', {}).get('name', 'None')}",
            "thought_trace": step3_res["thought_trace"]
        })

        elapsed_time = round(time.time() - start_time, 2)

        return {
            "status": "success",
            "user_query": raw_requirement,
            "elapsed_seconds": elapsed_time,
            "parsed_constraints": constraints,
            "candidates": candidates,
            "comparison": step3_res,
            "pipeline_traces": pipeline_traces
        }
