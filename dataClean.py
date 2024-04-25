import pandas as pd
import re
from html import unescape
import anthropic
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


def clean_solution_response(solution_response):
    solution_response = str(solution_response)
    # Unescape HTML entities
    cleaned_response = unescape(solution_response)
    # Remove HTML tags
    cleaned_response = re.sub(r'<[^>]+>', '', cleaned_response)
    # Replace non-breaking spaces and other non-ASCII characters if necessary
    cleaned_response = cleaned_response.replace('\xa0', ' ').replace('Â', '').replace('_x000D_\n', '').replace('â€™', "'").replace('â€”', '—').replace('â€œ', '“').replace('â€', '”')
    return cleaned_response

def format_proposal(row, col_selected = True):
    if col_selected:
        selected = [1, 3, 4, 5, 6, 7, 8, 11, 12, 13, 20, 21, 25, 26, 28, 29]
    else:
        selected = range(0, 40)
    cleaned_responses = "<solution_section>\n" + "\n\n".join(
        [f"{row.index[col_index]}: {clean_solution_response(row.iloc[col_index])}" 
         for col_index in selected]
    ) + "\n</solution_section>"
    return cleaned_responses

def claude_inference(system_instructions, id, solution_proposal):
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4096,
        temperature=0,
        system=system_instructions,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f'ID: {id}\n Proposal: {solution_proposal} \n Only provide assessment in JSON format.'
                    }
                ]
            }
        ]
    )
    return message.content[0].text

def gpt_inference(system_instructions, id, solution_proposal):
    
    client = OpenAI(OPENAI_API_KEY = os.getenv("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
    model="gpt-4-0125-preview",
    messages=[
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": f'ID: {id}\n Proposal: {solution_proposal}'}
    ]
    )

    return(completion.choices[0].message.content)

def print_message(json_string, debug=False):
    try:
        # Attempt to directly parse the JSON string into a Python dictionary
        parsed_json = json.loads(json_string)
        if debug:
            print(f"1st attempt: {parsed_json}")
        return parsed_json
    except json.JSONDecodeError:
        # If parsing fails, attempt to extract and clean the JSON string
        # Find the start of the JSON string within the message
        start_index = json_string.find('{')
        end_index = json_string.rfind('}') + 1
        json_part = json_string[start_index:end_index]

        # Escaping newlines and other control characters within the JSON string part
        json_part = json_part.replace("\n", " ").replace("\r", "").replace("\t", "")

        try:
            parsed_json = json.loads(json_part)
            if debug:
                print(f"2nd attempt: {parsed_json}")
            return parsed_json
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON after extraction: {e}")
            return None



def check_all_criteria_pass(message):
    for i in range(1, 5):
        criteria = message['assessment'][f'criterion_{i}']
        if criteria['result'] == 'fail':
            return False
    return True

def write_to_df(parsed_json, df, model_name):
    if isinstance(df, pd.Series):
        # If df is a Series, convert it to a DataFrame
        df = df.to_frame().T  # Transpose to make it a single-row DataFrame
    column_names = [f'{model_name}_result', f'{model_name}_advance']
    for column_name in column_names:
        if column_name not in df.columns:
            df[column_name] = None

    indexes = df.index[df['Solution ID'] == int(parsed_json['id'])].tolist()
    for idx in indexes:
        criteria_json = json.dumps(parsed_json['assessment'])
        df.at[idx, f'{model_name}_result'] = criteria_json
        df.at[idx, f'{model_name}_advance'] = check_all_criteria_pass(parsed_json)

def check_all_criteria_pass(message):
    for i in range(1, 5):
        criteria = message['criteria_assessment'][f'criteria_{i}']
        if criteria['result'] == 'fail':
            return False
    return True

def normalize_keys(model_data):
    new_data = {}
    for key, value in model_data.items():
        normalized_key = key.replace('criteria_', 'criterion_')  # Standardize to 'criterion_n'
        new_data[normalized_key] = value
    return new_data

def remove_last_part(s):
    last_index = s.rfind('_')
    return s[:last_index] if last_index != -1 else s

from transformers import GPT2Tokenizer
def count_tokens(text):
    # Load the tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    # Tokenize the text and count the tokens
    tokens = tokenizer.tokenize(text)
    num_tokens = len(tokens)

    print("Tokens:", tokens)
    print("Number of tokens:", num_tokens)
    return num_tokens


def print_metrics(df, model):
    confusion_matrix = pd.crosstab(df['advance'], df[f'{model}_advance'], rownames=['Actual'], colnames=[model], margins=True)
    print(confusion_matrix, "\n")

    TP = confusion_matrix.loc[True, True]  # True Positives
    TN = confusion_matrix.loc[False, False]  # True Negatives
    FP = confusion_matrix.loc[False, True]  # False Positives
    FN = confusion_matrix.loc[True, False]  # False Negatives

    accuracy = (TP + TN) / confusion_matrix.loc['All', 'All']
    precision = TP / (TP + FP) if (TP + FP) != 0 else 0
    recall = TP / (TP + FN) if (TP + FN) != 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

    if model == 'gpt':
        model_name = 'gpt-4-0125-preview'
    elif model == 'claude':
        model_name = 'claude-3-opus-20240229'
    print(f"Model: {model_name}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1_score:.4f} \n" )

def print_difference_decision(df):
    diff_df = df.loc[(df['advance'] != df['claude_advance']),:]
    print(diff_df)
    return diff_df