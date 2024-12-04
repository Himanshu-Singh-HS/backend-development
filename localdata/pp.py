
# import json
# from typing import Any, Dict, List
# # python -m src.monolith.landscaping.testing1
# from monolith.config import MONOLITH_SOLR_CLASS_CODE_URL,MONOLITH_SOLR_COMPANIES_URL,MONOLITH_SOLR_ASSIGNEE_URL
# import requests

# solr_url = MONOLITH_SOLR_CLASS_CODE_URL

# query_params = { "q": "*:*", "rows": 2, "wt": "json"}


# # class_codes :list[str] =['A']
# # name: str = " OR ".join(class_codes)
# # query_params: Dict[str, Any] = {
# #     "q": f"class_code:({name})",
# #     "rows": 100000,
# #     # "start": start_row,
# #     "fq": "NOT (level:(UP07 OR UP05))",
# #     "indent": "true",
# #     "wt": "json",  # Response format
# # }


# response = requests.get(solr_url, params= query_params)
# if response.status_code == 200:
#     results = response.json()
#     print(results)
# else:
#     print(f"Error: {response.status_code}, {response.text}")

a={
  "status": "success",
  "comparisons": {
    "US-11544099-B2": {
      "similarity": []
    }
  }
}
print(a.get("comparisons"))