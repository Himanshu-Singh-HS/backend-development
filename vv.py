
# from pydantic import BaseModel
# from typing import List, Dict, Literal

# class PatentComparison(BaseModel):
#     similarity: List[str]
#     differences: List[str]

# class ComparisonResponse(BaseModel):
#     status: Literal["success", "error"]
#     comparisons: Dict[str, PatentComparison]={}  # Adjusted to Dict

# # Sample JSON response
# json_response = {
#   "status": "success",
#   "comparisons": {
#     "US9928522B2": {
#       "similarity": [
#         "Both patents involve the use of profile attributes to direct advertisements to electronic visitors...",
#         "Both patents describe systems that automatically authorize the display of advertisements...",
#         "Both patents emphasize the importance of managing audience segments based on behavioral data..."
#       ],
#       "differences": [
#         "US-8671139-B2 focuses on directing advertisements specifically to electronic visitors...",
#         "The method in US-8671139-B2 is centered around a direct authorization process..."
#       ]
#     }
#   }
# }

# # Parse the response into the model
# comparison_response = ComparisonResponse.model_validate(json_response)
# # Print the parsed model
# print("this is json response -> ",comparison_response)




# class PatentComparison(BaseModel):
#     similarity: List[str]
#     differences: List[str]

# class ComparisonItem(BaseModel):
#     identifier: str
#     comparison: PatentComparison

# class ComparisonResponse(BaseModel):
#     status: Literal["success", "error"]
#     comparisons: List[ComparisonItem]

def convert_to_batches(lst, batch_size):
    return [lst[i : i + batch_size] for i in range(0, len(lst), batch_size)]

