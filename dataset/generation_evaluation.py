import nltk
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
import json
nltk.download('wordnet', download_dir='E:\\nltk_data')
import os


result_file_path = "human_test_gpt_4o_full.json"
# result_file_path = "human_test.json"


def property_classify_by_question(question: str):
    if "cell" in question:
        return "cellular_locations"
    elif "bio-specimen" in question:
        return "biospecimen_locations"
    elif "tissue" in question:
        return "tissue_locations"
    elif "disorders" in question:
        return "diseases"
    elif "value" in question:
        return "chromatographic"
    elif "information" in question:
        return "description"
    else:
        return "else"


def preprocess_text(text):
    """
    Preprocess the input text by splitting on spaces and handling special cases.
    """
    # Replace special characters with spaces for simplicity (if needed)
    cleaned_text = text.replace("-", " ").replace(",", " ").replace(".", " ").strip()
    tokens = cleaned_text.split()  # Tokenize into words
    return tokens


def calculate_metrics(content: str, reference: str):
    """
    Calculate BLEU-1, BLEU-2, BLEU-3, BLEU-4, and METEOR scores.

    Parameters:
        content (str): The generated text.
        reference (str): The reference text.

    Returns:
        list: A list containing BLEU-1, BLEU-2, BLEU-3, BLEU-4, and METEOR scores.
    """
    # Preprocess and tokenize the input strings
    content_tokens = word_tokenize(content)
    reference_tokens = word_tokenize(reference)

    # BLEU scores
    smoothing_function = SmoothingFunction().method1
    bleu1 = sentence_bleu([reference_tokens], content_tokens, weights=(1, 0, 0, 0),
                          smoothing_function=smoothing_function)
    bleu2 = sentence_bleu([reference_tokens], content_tokens, weights=(0, 1, 0, 0),
                          smoothing_function=smoothing_function)
    bleu3 = sentence_bleu([reference_tokens], content_tokens, weights=(0, 0, 1, 0),
                          smoothing_function=smoothing_function)
    bleu4 = sentence_bleu([reference_tokens], content_tokens, weights=(0, 0, 0, 1),
                          smoothing_function=smoothing_function)

    # METEOR score (hypothesis and reference must be tokenized lists)
    meteor = meteor_score([reference_tokens], content_tokens)
    # meteor = 0

    return [bleu1, bleu2, bleu3, bleu4, meteor]


if __name__ == "__main__":
    results = [0 for i in range(5)]
    count = 0
    save_folder = "eval_results"
    save_name = "gpt_meteor.txt"
    result_array = []
    bleu_1 = []
    with open(result_file_path, "r", encoding="utf-8") as r:
        generation_data = json.load(r)
    for smiles in generation_data.keys():
        data = generation_data[smiles]
        for qa_pair in data:
            question = qa_pair[0]
            if property_classify_by_question(question) == "description":
                reference = qa_pair[1]
                content = qa_pair[2]
                values = calculate_metrics(content, reference)
                for i, value in enumerate(values):
                    results[i] += value
                count += 1
                result_array.append(values[4])
    results = [result / count for result in results]
    print(results)
    print(count)
    with open(os.path.join(save_folder, save_name), "w") as w:
        result_array = [str(item) + '\n' for item in result_array]
        w.writelines(result_array)
    '''
    [0.46479440405863215, 0.4129157173565165, 0.387879936949493, 0.3701619543040308, 0.500227208218955]
    33459
    '''
    "[0.23806721646248963, 0.11305325497635466, 0.06518762752011517, 0.040934345230472846, 0.24326343714915505]"
    "[0.12105175501125459, 0.02359441358626221, 0.005066040334797128, 0.0015601871993585223, 0.22050777488406914]"