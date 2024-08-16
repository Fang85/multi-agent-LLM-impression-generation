# Install required libraries
# !pip install nltk sacrebleu rouge-score rouge bert-score

import sacrebleu
from rouge_score import rouge_scorer
import bert_score
import pandas as pd

def metric_score(candidate,reference,measure_type):

    # Types =['presion','recall','fmeasure']

    # SacreBLEU Score
    bleu = sacrebleu.sentence_bleu(candidate, reference, lowercase=True,smooth_method='exp', smooth_value=None, use_effective_order=True)
    score_all = {"bleu": bleu.score}

    # ROUGE Score using rouge-score
    rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], 
                                        use_stemmer=True, split_summaries=True)
    rouge_score = rouge.score(candidate, reference[0])
    score_all['rouge1']= rouge_score['rouge1']
    score_all['rouge2']= rouge_score['rouge2']
    score_all['rougeL']= rouge_score['rougeL']

    # BERTScore
    all_preds, hash_code = bert_score.score([candidate], reference, model_type='bert-large-uncased', num_layers=18,
                                            verbose=False, idf=False, batch_size=64,
                                            nthreads=4, lang= 'en', return_hash=True,
                                            rescale_with_baseline=False)
    print(f"hash_code: {hash_code}")
    score_all['bert'] = {"precision": all_preds[0].cpu().item(), "recall": all_preds[1].cpu().item(), "fmeasure":
            all_preds[2].cpu().item()}
    
    score = {
        "bleu": score_all["bleu"],
        "rouge1": getattr(score_all["rouge1"], measure_type),
        "rouge2": getattr(score_all["rouge2"], measure_type),
        "rougeL": getattr(score_all["rougeL"], measure_type),
        "bert": score_all["bert"][measure_type]
    }
    
    return score


def extract_impression_content(text):
    """
    Extract the impression content from a given text.
    keep all content after the first "IMPRESSION:" and remove
    all content starting from the last "Note:". 
    """
    impression_start = text.find("IMPRESSION:")
    if impression_start != -1:
        # Extract content starting after "IMPRESSION:"
        impression_content = text[impression_start + len("IMPRESSION:"):]
    else:
        impression_content = text

    note_start = impression_content.rfind("Note:")
    if note_start != -1:
        # Remove content starting from the last "Note:"
        impression_content = impression_content[:note_start]

    return impression_content.strip()

# add 'ID' value for each metric result
def score_with_id(ID,candidate,reference,measure_type):
    score = metric_score(candidate,reference,measure_type)
    scores_with_id = {'ID': ID, **score}
    score_df = pd.DataFrame([scores_with_id])
    return score_df

    
def evaluation_three_models(data_df,measure_type,reference_name,model1_name,model2_name,model3_name):
    """
       Evaluate the performance of three models using the specified metric and reference data.
    
    In this context, the models are:
    - model1: Radiologist only
    - model2: Radiologist with retriever assistance
    - model3: Radiologist with retriever and reviewer assistance
    
    Note:
    - If no negative feedback is provided by the reviewer, the result for model3 will be null.
    - In such cases, model3_result will default to model2_result during metric score calculation.
    """

    ####### just keep the content after "IMPRESSION:"
    data_df[reference_name] = data_df[reference_name] .apply(extract_impression_content)
    data_df[model1_name] = data_df[model1_name] .apply(extract_impression_content)
    data_df[model2_name] = data_df[model2_name] .apply(extract_impression_content)
    data_df[model3_name] = data_df[model3_name].apply(lambda x: extract_impression_content(x) if  pd.notna(x) else x)
    
    model1_df  = pd.DataFrame()
    model2_df = pd.DataFrame()
    model3_df = pd.DataFrame()
    # get the score for all model
    for index, item in data_df.iterrows():
        print("\nindex:",index)
        reference = [item[reference_name]]  ###make it a list
        # reference = item['IMPRESSION_CLEAN']
        model1_df = pd.concat([model1_df, score_with_id(item['ID'],item[model1_name], reference, measure_type)], ignore_index=True)
        model2_df = pd.concat([model2_df, score_with_id(item['ID'],item[model2_name], reference, measure_type)], ignore_index=True)
        if pd.notna(item[model3_name]):  ##item[model3_name] is not None:
            model3_df = pd.concat([model3_df, score_with_id(item['ID'],item[model3_name], reference, measure_type)], ignore_index=True)
        else: 
            model3_df = pd.concat([model3_df, pd.DataFrame([model2_df.iloc[-1, :]])], ignore_index=True)
        
    model1_df.insert(1, "Model", model1_name)
    model2_df.insert(1, "Model", model2_name)
    model3_df.insert(1, "Model", model3_name)

    all_df = pd.concat([model1_df, model2_df,model3_df], ignore_index=True)
    all_sort_df = all_df.sort_values(by=['ID','Model'])
    mean_df = all_sort_df.iloc[:,1:].groupby('Model').mean()
    
    return mean_df,all_sort_df