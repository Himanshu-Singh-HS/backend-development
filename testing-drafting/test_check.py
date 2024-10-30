import asyncio
import json
import os
import pytest
import httpx
from monolith.drafting.models import DraftingSearchParameters, NoveltyRequest

# Load JSON data from file
def load_json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

data_file = os.path.join(os.path.dirname(__file__), 'sample.json')
json_data = load_json_data(data_file)

# Base URL endpoint
base_url = "https://betav2.patdelanalytics.ai/api"

# Main test function to process all JSON objects in parallel
@pytest.mark.asyncio
async def test_generate_drafting():
    async with httpx.AsyncClient(timeout=120.0) as client:
        
        # Function to process a single JSON object
        async def process_json_object(json_id, json_info):
            print(f"Processing JSON ID: {json_id} started...")  # Debug print

            # Generate novelty
            type = "DETECT"
            expected_status = 200
            expected_message = "Novelty detected."
            
            # Prepare the payload for novelty detection
            payload = NoveltyRequest(
                invention=json_info['invention_disclosure'],
                reference_novelty="Prior Art Reference XYZ",
                user_message="",
                is_regenerate=True,
            ).dict()

            print(f"Sending novelty request for JSON ID: {json_id}")  # Debug print
            response = await client.post(
                f"{base_url}/v1/drafting/novelty?type={type}", json=payload
            )
            assert response.status_code == expected_status
            response_json = response.json()
            assert response_json["status"] == "success"
            assert response_json["message"] == expected_message
            print(f"Novelty response received for JSON ID: {json_id}")  # Debug print

            # Generate Drafting Search Parameters
            search_payload = DraftingSearchParameters(
                drafting_type="DRAFTING",
                jurisdiction="US",
                project_title=json_info['project_title'],
                abstract="This invention relates to an advanced thermal management system designed to enhance the cooling efficiency of high-performance electronic devices.",
                novelty=response_json["data"]["novelty"],
                invention_disclosure=json_info['invention_disclosure'],
                problem_statement=json_info['problem_statement'],
                keyfeatures="1. Novel heat dissipation mechanism.\n2. Enhanced cooling efficiency.",
                uploaded_classes=["Thermal Management Systems", "Electronic Cooling Solutions"],
                uploaded_ucids=["US-7370044-B2"],
            ).dict()

            print(f"Sending create_draft request for JSON ID: {json_id}")  # Debug print
            search_response = await client.post(f"{base_url}/v1/drafting/create_draft", json=search_payload)
            assert search_response.status_code == 200
            search_response_json = search_response.json()
            search_id = search_response_json["search_id"]
            print(f"create_draft response received for JSON ID: {json_id}, search_id: {search_id}")  # Debug print

            # Function to generate drafting parts
            async def generate_drafting_part(part):
                url = f"{base_url}/v1/drafting/generate?part={part}&search_id={search_id}"
                print(f"Requesting {part} for JSON ID: {json_id}")  # Debug print
                response = await client.get(url)
                return response

            # Generate CLAIMS and FIGURES sequentially
            claims_response = await generate_drafting_part("CLAIMS")
            assert claims_response.status_code == 200
            print(f"Claims generated successfully for JSON ID: {json_id}.")

            figures_response = await generate_drafting_part("FIGURES")
            assert figures_response.status_code == 200
            print(f"Figures generated successfully for JSON ID: {json_id}.")

            # Generate other parts in parallel
            parts = ["FIGURE_LIST", "ABSTRACT", "SUMMARY", "DESCRIPTION", "TECHNICAL_FIELD"]
            tasks = [generate_drafting_part(part) for part in parts]
            print(f"Sending parallel requests for other parts for JSON ID: {json_id}")  # Debug print
            part_results = await asyncio.gather(*tasks)
            for result in part_results:
                assert result.status_code == 200, f"Error for part {result.url}: {result.status_code} - {result.text}"
            print(f"All parts received for JSON ID: {json_id}")  # Debug print

            # Generate TITLE and BACKGROUND sequentially
            title_response = await generate_drafting_part("TITLE")
            assert title_response.status_code == 200
            print(f"Title generated successfully for JSON ID: {json_id}")

            background_response = await generate_drafting_part("BACKGROUND")
            assert background_response.status_code == 200
            print(f"Background generated successfully for JSON ID: {json_id}")

            print(f"All parts processed successfully for JSON ID: {json_id}")
            print(f"=========================================")

        # Create a task for each JSON object
        tasks = [process_json_object(json_id, json_info) for json_id, json_info in json_data.items()]
        
          # Create a task for each JSON object
        # for json_id, json_info in json_data.items():  changes by himanshu 
        #     tasks.append(process_json_object(json_id, json_info))  we can check sequentially where is mistake or error 

        print(f"Starting parallel execution of {len(tasks)} JSON objects...")
        # Run all tasks in parallel
        await asyncio.gather(*tasks)
        print("Parallel execution completed.")

