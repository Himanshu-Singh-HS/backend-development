
# # from pydantic import BaseModel
# # from typing import List, Dict, Literal

# # class PatentComparison(BaseModel):
# #     similarity: List[str]
# #     differences: List[str]

# # class ComparisonResponse(BaseModel):
# #     status: Literal["success", "error"]
# #     comparisons: Dict[str, PatentComparison]={}  # Adjusted to Dict

# # # Sample JSON response
# # json_response = {
# #   "status": "success",
# #   "comparisons": {
# #     "US9928522B2": {
# #       "similarity": [
# #         "Both patents involve the use of profile attributes to direct advertisements to electronic visitors...",
# #         "Both patents describe systems that automatically authorize the display of advertisements...",
# #         "Both patents emphasize the importance of managing audience segments based on behavioral data..."
# #       ],
# #       "differences": [
# #         "US-8671139-B2 focuses on directing advertisements specifically to electronic visitors...",
# #         "The method in US-8671139-B2 is centered around a direct authorization process..."
# #       ]
# #     }
# #   }
# # }

# # # Parse the response into the model
# # comparison_response = ComparisonResponse.model_validate(json_response)
# # # Print the parsed model
# # print("this is json response -> ",comparison_response)




# # class PatentComparison(BaseModel):
# #     similarity: List[str]
# #     differences: List[str]

# # class ComparisonItem(BaseModel):
# #     identifier: str
# #     comparison: PatentComparison

# # class ComparisonResponse(BaseModel):
# #     status: Literal["success", "error"]
# #     comparisons: List[ComparisonItem]

# def convert_to_batches(lst, batch_size):
#     return [lst[i : i + batch_size] for i in range(0, len(lst), batch_size)]

# data=[ "WO-2024241761-A1",
#     "WO-2024241762-A1",
#     "WO-2024242306-A1",
#     "WO-2024242904-A1",
#     "WO-2024242970-A1"
    
# ]
# print(len(data))
# # a=[]
# # for item in data:
# #     x,y,z = item.split("-")
# #     print(x,y,z)
# #     a.append(x+y)
# # print(a)
# a="WO-2024241762-A1"
# x,y,z=a.split('-') 
# print(x,y,z)
# print(x+y)

 
# common_ucids = list(set(ucids1) & set(ucids2))

 
# unique_to_ucids1 = list(set(ucids1) - set(ucids2))
# unique_to_ucids2 = list(set(ucids2) - set(ucids1))

 
# all_unique_ucids = sorted(set(ucids1 + ucids2))

 
# print("Common UCIDs:", common_ucids)
# print("UCIDs unique to ucids1:", unique_to_ucids1)
# print("UCIDs unique to ucids2:", unique_to_ucids2)
# print("All unique UCIDs ranked lexicographically:", all_unique_ucids)


# print("Total UCIDs:", len(all_unique_ucids))








# #####=========
# # Common elements
# common_ucids = list(set(ucids1) & set(ucids2))

# # Unique elements in each list
# unique_to_ucids1 = list(set(ucids1) - set(ucids2))
# unique_to_ucids2 = list(set(ucids2) - set(ucids1))

# # Combined unique elements ranked lexicographically
# all_unique_ucids = sorted(set(ucids1 + ucids2))

# # Output the results
# print("Common UCIDs:", common_ucids)
# print("UCIDs unique to ucids1:", unique_to_ucids1)
# print("UCIDs unique to ucids2:", unique_to_ucids2)
# print("All unique UCIDs ranked lexicographically:", all_unique_ucids)

# # Total length of combined UCIDs
# print("Total UCIDs:", len(all_unique_ucids))


from uuid import UUID

# Example UUID1 (replace with your actual UUID1)
uuid_str = 'f47ac10b-58cc-4372-a567-d45763efe036'

# Extract the node (MAC address) from the UUID
uuid_obj = UUID(uuid_str)
node_mac = uuid_obj.node

# Format the extracted node as a MAC address
uuid_mac = ':'.join(f'{(node_mac >> i) & 0xff:02x}' for i in range(40, -1, -8))

# Your actual MAC address (replace with your MAC address)
device_mac = "d4:57:63:ef:e0:36"

# Compare the MAC addresses
if uuid_mac.lower() == device_mac.lower():
    print(f"The MAC address matches: {uuid_mac}")
else:
    print(f"The MAC address does not match.\nUUID MAC: {uuid_mac}\nYour MAC: {device_mac}")


import requests

mac_prefix = "d4:57:63"
response = requests.get(f"https://macvendors.com/query/{mac_prefix}")
if response.status_code == 200:
    print(f"Manufacturer: {response.text}")
else:
    print("Could not find manufacturer information.")





# if claim_list:
#     # Assign user_description_components to the last claim in the list
#     last_claim = claim_list[-1]
#     setattr(last_claim, 'user_description_components', final_user_description_component)



  # if claim_list:
    #     claim_list[-1].user_description_components =  user_description_components
    
#  data_features = [
#                   DataFeature(
#         figure=fig.figure,
#         description_type=fig.description_type,
#         text=fig.text,
#         features=fig.features
#     )
#     for fig in user_figure_features
# ]                