from tqdm import tqdm
from server.data_loader import PatentLoader
import os
from from_monolith.download_patent import get_patent_document_by_ucids
# from nltk.tokenize import sent_tokenize
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForMaskedLM
# from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
from sklearn.cluster import AgglomerativeClustering
from server.openai_api import Openai_API
import numpy as np
from server.processing import Processing_steps
import concurrent.futures
from sentence_transformers import SentenceTransformer
import re
from .models import ComparisonResponse, PatentComparison
from typing import List, Dict
# from summarizer import Summarizer
# from summarizer2 import summarize

# class BertExtractiveSummarizer:
#     def __init__(self, content = []) -> None:
#         document_chunk = 20
#         # merged_paragraphs = self.merge_paragraphs(content)
#         # print(len(content), len(merged_paragraphs))
#         # self.doc_batches = [merged_paragraphs[i:i + document_chunk] for i in range(0, len(merged_paragraphs), document_chunk)]
#         self.doc_batches = content

    

#     def summarize_text(self, ratio = 0.3):
#         words_count, summary = 0, ""
#         for each_batch in self.doc_batches:
#             summary += "\n" +model(each_batch, ratio=ratio)
#             # words_count += len(summary.split())
#             # print(summary, type(each_batch))
#         # print(words_count)
#         return summary
    
class Comparator:
    def __init__(self):
        self.process = Processing_steps(chunk_size=250, chunk_overlap=50)
        self.openapi = Openai_API()
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # self.model_T5 = T5ForConditionalGeneration.from_pretrained("t5-base").to(self.device)
        # self.tokenizer_t5 = T5Tokenizer.from_pretrained("t5-base")
        # self.extractive_model = Summarizer()
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.comparison_response = ComparisonResponse(status="success")
        # self.summarizermodel = Summarizer()

    def define_request_features(self, input_key_features: list, ucids: list,subject_ucid: str):
        self.input_key_features = input_key_features
        self.ucids = ucids
        self.subject_ucid = subject_ucid
    
    
    def __reduce_key_feature(self, key_features:str) -> str:

        key_features = [each_feature for each_feature in key_features.splitlines() if each_feature.strip()]
        n_clusters = len(key_features)
        if n_clusters < 20:
            return key_features
        elif n_clusters <= 50:
            n_clusters = int(n_clusters - n_clusters * 0.15)
        elif n_clusters <= 100:
            n_clusters = int(n_clusters - n_clusters * 0.25)
        elif n_clusters <= 150:
            n_clusters = 60
        elif n_clusters <= 200:
            n_clusters = 75
        else:
            n_clusters = 80

        # Do embedding in batches
        embeddings = []
        for feature_index in range(0, len(key_features), 100):
            feature_batch = key_features[feature_index: feature_index+100]
            embeddings.extend(self.embed_model.encode(feature_batch))

        # embeddings = self.embed_model.encode(key_features)
        clustering_model = AgglomerativeClustering(n_clusters=n_clusters, metric='cosine', linkage='average', compute_full_tree='auto')
        cluster_labels = clustering_model.fit_predict(embeddings)

        clustered_features = {}
        for idx, label in enumerate(cluster_labels):
            if label not in clustered_features:
                clustered_features[label] = []
            clustered_features[label].append(key_features[idx])
        
        # text_batches = TextEncodings([abstract_summ], chunk_size=300).text_batching()

        final_key_features = []
        for label, features in clustered_features.items():
            if len(features) == 1:
                final_key_features.append(features[0])
            else:
                feature_lines = "\n".join(features)
                text_batches = self.process.text_batching(feature_lines)
                summary = text_batches[0]
                # for each_batch in text_batches:
                    # summary += "\n" + self.extractive_model(each_batch, ratio=0.7)

                final_key_features.append(summary.strip())



        final_key_feature = "\n".join(final_key_features)
        return final_key_feature
    

    def _comparison_prompts(self, prompt_key) -> str:
        
        comparison_prompts = { 
           "keyfeatures_prompt" :"""Extract the technical key features from the provided description. 
            Focus specifically on aspects that are unique, innovative, and distinct from existing technologies.

            List each technical point on a new line.
            Avoid including general or well-known features.
            Do not include information about figures, tables, or examples.
"""            
        }
        
        prompt =comparison_prompts.get(prompt_key)
        if prompt:
            """Cleaning the left side empty spaces from prompts"""
            prompt = "\n".join([line.lstrip() for line in prompt.split("\n")])
        return prompt
        
    
    def download_patents(self, ucids) -> str:
        pat_loder = PatentLoader()
        patent_directory = pat_loder.temp_download_dir()
        try:
            print("Downloading Patents - full documents ")
            for batch in range(0, len(ucids), 100):
                try:
                    full_documents = get_patent_document_by_ucids(ucids[batch:batch+100])
                    for each_doc in full_documents:
                        pat_loder.save_the_document(each_doc.patent_number.replace("-",""), each_doc, patent_directory)
                    
                except Exception as error:
                    print("Error in downloading:", error)
                    raise 
                
        except Exception  as e:
            print("erro during downalod patents  ", e)
            raise
        
        return patent_directory
    

    def generate_key_feature(self, description_text):
        prompt_key = "keyfeatures_prompt"
        keyfeature_prompt = self._comparison_prompts(prompt_key)

        if not keyfeature_prompt or keyfeature_prompt.strip() == "":
            return ComparisonResponse(status="error")
        
        description_text = self.process.string_stripper_tiktoken(text=description_text, token_limit=10000)
        messages = [
            {"role": "system", "content":keyfeature_prompt},
            {"role": "user", "content": description_text}
        ]
        key_features = self.openapi.generate_text(messages=messages, model="gpt-3.5-turbo-1106", max_tokens=1000, temperature=0.1)
        return key_features
    
    
    
    
    
    
    

    def generate_comparator(self, __patent_dir: str) -> ComparisonResponse:
        
        print("this is generate comparator data -> ",__patent_dir)
        all_files = os.listdir(__patent_dir)
        print(all_files)
        print("downloading done")
        pat_loder = PatentLoader()

        # key_features = [each_keyfeature.get("text", "") for tagged_claim in data.get("tagged_claims", []) for each_keyfeature in tagged_claim.get("key_features", [])]
        # key_features = [each_keyfeature for each_keyfeature in key_features if each_keyfeature.strip()]
        if not self.subject_ucid:
            self.subject_ucid = "Invention"
        print(f"{self.subject_ucid=}")
            
        sim_diff_results = []
        self.input_key_features = "\n".join(self.input_key_features)
        try:
            for each_file in tqdm(all_files):
                sim_diff = {}
                target_ucid = each_file.replace(".json", "")
                
                __file_path = os.path.join(__patent_dir, each_file)
                # Extract description and claims
                content = pat_loder.load_description_and_claims(__file_path, include_abstract=True)

                abstract = content.get("abstract", "")
                description = content.get("description", "")
                # claims = content.get("claims")

                all_description = description.splitlines()
                all_description = [abstract] + all_description
                
                
                # all_description = [each_line for each_line in all_description if len(each_line.split()) > 20]
                # all_description = [each_line for each_line in all_description if len(sent_tokenize(each_line)) > 2]

                # Prepare batches of 1500 tokens to generate key feature
                prepared_batches = []
                token_limit = 1500
                last_paragraph = ""
                print("tokens count",self.process.count_tokens("\n".join(all_description)), len(all_description))
                for i in range(len(all_description)):
                    last_paragraph += "\n\n"+all_description[i]
                    if self.process.count_tokens(last_paragraph) >= token_limit:
                        prepared_batches.append(last_paragraph)
                        last_paragraph = ""

                if last_paragraph:
                    prepared_batches.append(last_paragraph)

                # Run threads to generate features
                num_threads = 12
                all_results = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                    for i in range(0, len(prepared_batches), num_threads):
                        batch = prepared_batches[i:i + num_threads]
                        futures = [executor.submit(self.generate_key_feature, item) for item in batch]
                        for future in concurrent.futures.as_completed(futures):
                            all_results.append(future.result())  
                prepared_keyfeature = "\n".join(all_results)
                total = len(prepared_keyfeature.splitlines())
                
                prepared_keyfeature = self.__reduce_key_feature(prepared_keyfeature)
                # print(type(prepared_keyfeature))
                # prepared_keyfeature = self.generate_key_feature("\n".join(all_description))
                print(f"Reduced from {total} to {len(prepared_keyfeature.splitlines())}")
                
                comparator_prompt= f"""You are a Technical Analyst. Your task is to find the technical similarities and differences between the provided features of {self.subject_ucid} and the list of features of {target_ucid}.
                    Consider features of {self.subject_ucid} as the subject patent features and list of features of {target_ucid} is your target.
                    You need to focus on features of {self.subject_ucid} and use the provided features of {target_ucid} for comparison and provide the technical analysis along with a similarity score.
                    Provided technical analysis should justify the similarity score you have given based on their technical similarities.
                    As a technical analyst you are allowed to infer similarity between key elements of subject features, if their technical functions are similar with the target features of {target_ucid} patent.
                    Understand the below guidelines of similarities and differences, then compare the features.

                    Guidelines for similarities:
                    You need to focus on the features of {self.subject_ucid} for comparison and pick technically relevant and functionally similar features from target {target_ucid}'s features and provide technical analysis on their similarities.
                    Write contextual and technical similarities analysis, do not assume or write similar points if there is no similarities.
                    While writing for similarities, avoid generating any difference points in the sense of process, method, or component.
                    Must provide a similarity score ranging between 0-1 according to contextual and technical similarities in sense of their functional details.
                    # Examples for similarities (Learn how to write similarities):
                    {{'text': 'Both the patents calculate space usage costs for organizations and use machine learning to associate individuals with their space usage.', 'score': 0.75}}
                    {{'text': 'Both patents teaches a system for detecting malware in a suspected computer software using a pattern classification algorithm based upon features of the malware.', 'score': 0.8}}
                    {{'text': 'Both patents uses content filtering system which is formed by a content filtering training program model at the server end and a content filtering application at the client end (mobile phone).', 'score': 0.82}}

                    Guidelines for differences:
                    Differences should focus on the technical features of {self.subject_ucid} having no functional or technical similarity with the provided target features of {target_ucid}.
                    You need to pick most suitable and technically relevant features from {target_ucid} features and provide technical analysis on how they are technically different, focus should always on {self.subject_ucid} features.
                    Write only 1-2 difference points covering the most important differences; only if they are technically and functionally different.
                    If you have already mentioned a feature in similarities then avoid using or comparing the same feature in differences.
                    Must provide a similarity score ranging between 0-1 according to contextual and technical similarities in sense of their functional details.
                    # Examples for differences (Learn how to write differences):
                    {{"text": "The {self.subject_ucid} patent describes the use of Active Tag Identifiers (ATIs) to indicate which forwarding instruction tag is active, whereas {target_ucid} discloses a systematic approach for processing and matching labels within a forwarding base, which relates conceptually but lacks an explicit identifier for active tags.", "score": 0.6}}
                    Follow the output response structure.
                    """
                response_format= """
                    {
                        "similarities": [
                            {"text": "Similarity 1", "score": "{similarity_score}"},
                            {"text": "Similarity 2", "score": "{similarity_score}"},
                            {"text": "Similarity 3", "score": "{similarity_score}"} 
                        ],
                        "differences": [
                            {"text": "Difference 1", "score":"{similarity_score}"},
                            {"text": "Difference 2", "score": "{similarity_score}"},
                            {"text": "Difference 3", "score": "{similarity_score}"}
                        ]
                    }
                    """


                
                comparator_prompt += response_format
                
                messages = [
                    {"role": "system", "content": comparator_prompt},
                    {"role": "user", "content": f"Patent {self.subject_ucid}:\n{self.input_key_features}\n\nPatent {target_ucid}:\n{prepared_keyfeature}"}
                ]
                similarities_diff = self.openapi.generate_text(messages=messages, model="gpt-4o-mini", max_tokens=1500, temperature=0.05)# , response_format="json"
                print(f"{similarities_diff=}")
                # Regular expressions to extract "text" fields from "similarities" and "differences" sections
                similarities_pattern = r'"similarities":\s*\[(.*?)\],'
                differences_pattern = r'"differences":\s*\[(.*?)\]\s*}'

                # Find matches for similarities
                similarities_match = re.search(similarities_pattern, similarities_diff, re.DOTALL)
                if similarities_match:
                    similarities_str = similarities_match.group(1)
                    # Extract all "text" fields within similarities
                    similarities_texts = re.findall(r'"text":\s*"(.*?)"', similarities_str, re.DOTALL)
                else:
                    similarities_texts = []

                # Find matches for differences
                differences_match = re.search(differences_pattern, similarities_diff, re.DOTALL)
                if differences_match:
                    differences_str = differences_match.group(1)
                    # Extract all "text" fields within differences
                    differences_texts = re.findall(r'"text":\s*"(.*?)"', differences_str, re.DOTALL)
                else:
                    differences_texts = []
                    
                # Prepare the final output in the requested format
                comparison = PatentComparison(similarity=[text.strip() for text in similarities_texts], differences=[text.strip() for text in differences_texts])
                self.comparison_response.add_comparison(ucid=target_ucid, comparison=comparison)
                
        except Exception as e:
            print("error during genearting comaprator",e)
        return self.comparison_response
        
        
