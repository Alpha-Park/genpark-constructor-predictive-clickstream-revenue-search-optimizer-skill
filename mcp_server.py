#!/usr/bin/env python3
import json
import sys
from client import ConstructorPredictiveClickstreamSearchOptimizer

from typing import Any, Dict, List, Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:
    raise SystemExit("MCP requires the mcp package. Run: python -m pip install -r requirements.txt") from exc

mcp = FastMCP('genpark-constructor-predictive-clickstream-revenue-search-optimizer-skill')

@mcp.tool()
def optimize_search_results(query: str = "", candidates: Optional[List[Dict[str, Any]]] = None, user_clickstream: Optional[Dict[str, Any]] = None) -> str:
    """Rank supplied product candidates using clickstream and revenue signals."""
    return json.dumps(ConstructorPredictiveClickstreamSearchOptimizer().optimize_search_results(query, candidates if candidates is not None else [], user_clickstream if user_clickstream is not None else {}))

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        optimizer = ConstructorPredictiveClickstreamSearchOptimizer()
        items = [
            {"id": "c1", "title": "Wireless Noise Cancelling Headphones", "category": "Electronics", "brand": "Sony", "price": 349.0, "historical_cvr": 0.05},
            {"id": "c2", "title": "Over-Ear Studio Headphones", "category": "Audio", "brand": "AudioTechnica", "price": 149.0, "historical_cvr": 0.08},
            {"id": "c3", "title": "Budget Bluetooth Earbuds", "category": "Electronics", "brand": "Generic", "price": 29.0, "historical_cvr": 0.12}
        ]
        clickstream = {"viewed_categories": ["Electronics"], "viewed_brands": ["Sony"], "preferred_price_range": [200, 500]}
        res = optimizer.optimize_search_results("headphones", items, clickstream)
        assert len(res["ranked_results"]) == 3
        assert res["ranked_results"][0]["id"] == "c1"
        print(f"[TEST PASS] Constructor.io Optimizer Passed! Top: {res['top_rpv_product']}")
        sys.exit(0)

    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
