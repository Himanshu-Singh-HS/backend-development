class GetPatentdata: 
    def merge_bibliographys_and_summaries(self,bibliographys: List[Dict], summaries: List[Dict], response_comp:dict) -> List[Dict]:
        try:
            similarity_texts=[]
            count=0
            total_score=0
            bibliography_lookup = {b.patent_number: b for b in bibliographys}
            merged_data = []
            # for patent, comparison_data in response_comp['comparisons'].items():
            #         for similarity in comparison_data['similarity']:
            #             similarity_texts.append(similarity['text'])
            #             total_score += similarity['score']
            #             count += 1
            # average_score = total_score / count if count > 0 else 0
            
            for summary in summaries:
                each = {}
                ucid = summary.ucid
                if ucid in bibliography_lookup:
                    each.update(bibliography_lookup[ucid].dict())
                    each.update(summary.dict())
                     
                # each["average_score"] = average_score
                # each["similarities"]= similarity_texts
                # print("original response comparataor -->",response_comp)
                if response_comp:
                    print("yes th data is coming ",response_comp)
                    # ucid_no_hyphen = ucid.replace('-', '')  
                    if ucid in response_comp:
                        print("present ucids->",ucid)
                        comparison = response_comp[ucid]
                        # change this by using model
                        each['similarity'] = [data.get("text","") for data in comparison.get(ucid).get("similarity")] 
            merged_data.append(each)  
               
                                
                                        
        except Exception as e:
            print("error in merge_bibiliograpghy function",e)
        return merged_data
    
    #  if ucid in ml_response.comparisons:
    #                     comparison = ml_response.comparisons[ucid]
    #                     similarities = comparison.similarity

    #                     # Calculate total and average score
    #                     total_score = sum(s.score for s in similarities)
    #                     average_score = total_score / len(similarities) if similarities else 0

    #                     # Add similarity details to the merged data
    #                     each["similarities"] = [
    #                         {"text": s.text, "score": s.score} for s in similarities
    #                     ]
    #                     each["total_score"] = total_score
    #                     each["average_score"] = average_score

    #                 merged_data.append(each) 
    
    
    
    #   if ucid in ml_response.comparisons:
    #                     comparison = ml_response.comparisons[ucid]
    #                     similarities = comparison.similarity

    #                     # Calculate total and average scores
    #                     total_score = sum(sim.score for sim in similarities)
    #                     average_score = total_score / len(similarities) if similarities else 0

    #                     # Add similarity details to the merged data
    #                     each["similarities"] = [
    #                         {"text": sim.text, "score": sim.score} for sim in similarities
    #                     ]
    #                     each["total_score"] = total_score
    #                     each["average_score"] = average_score

    #                 merged_data.append(each)