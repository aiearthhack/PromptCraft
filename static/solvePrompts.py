prompts = {
    "prompt_instruction":"""
    As a solution proposal screener, your task is to assess the given solution proposal based on the criteria I provide in the following message.I will provide one main criterion or multiple main criteria, which may include sub-criteria for reference. However, your assessment should be based on the main criteria (criterion 1 - criterion 5) only. Carefully analyze the proposal step by step. Be aware of inconsistencies in the arguments, lack of supporting evidence or credible sources, and unreasonable or illogical arguments. Provide your final assessment with clear and concise reason for all given criterion. Provide your assessment in valid JSON format without any additional text or explanations:
        {
            "id": "",
            "assessment": {
                "criterion_n": {
                    "result": "'pass' or 'fail'",
                    "reason": "provide reasoning of your assessment."
                },...continue for all given criteria
            }
        }
        """,
    "prompt_train_criterion_instruction":"""
    As a solution proposal screener, you will be given a solution id, proposal, and advance decision. Your task is to carefully read through the complete solution.

    1. Based on the following criterion, assessing the solution step by step.
    2. Provide your assessment(pass/fail). 
    3. Compare your assessment to original advance decision (True: pass, False: fail).
    4. List down your reasoning of the assessment. Clearly explain why your assessment align or conflict with the original "Advance" decision.
    5. Provide your assessment in a valid JSON format:
        {
            "id": "",
            "assessment": {
                "criterion_n": {
                    "result": "'pass' or 'fail'",
                    "reason": "provide reasoning of your assessment. Clearly explain your steps of thought especially when you conflict with original advance decision."
                }
            }
        }
    """,
    "criterion_1":"""
    <criterion_1>
    Criterion 1
    Assess the proposal's completeness, intelligibility, and appropriateness.
    - Completeness:
        - Ensure the application is written in English.
        - Check if all required questions have been answered with sufficient detail. Applications with only a few words for required questions should be considered incomplete.
    - Intelligibility:
        - Carefully read the application and determine if you can clearly understand the proposed solution. If, after reviewing the application, you cannot comprehend the nature of the solution, it should be considered unintelligible.
    - Appropriateness:
        - Evaluate whether the application was created with a serious intent to participate in the Challenge.
        - If the application contains content that is clearly offensive, irrelevant, or disrespectful, it should be deemed inappropriate.
    </criterion_1>
    """,
    "criterion_2":"""
    <criterion_2>
    Criterion 2
    Assess whether the proposal meets prototype criterion. The proposal should clearly demonstrate that the venture or organization has reached the Prototype stage, which involves both actively building and testing its product, service, or business model. It has to be able to provide evidence of its target area and users/customers, as well as how it has tested its solution with them. Evaluate the consistency of the solution's stage description throughout the proposal. If there are contradictions between the claimed stage and the provided details, the proposal may be rejected. Assess the evidence and reasonableness of the claims to ensure the solution has genuinely reached at least the Prototype stage before advancing it to the next phase of evaluation.
    </criterion_2>
    """,
    "criterion_3":"""
    <criterion_3>
    Criterion 3
    Evaluate whether it meets all of the valid solution sub-criteria:
    - Directly addresses health challenges in contexts affected by conflict, displacement, natural disasters, or systemic inequities and vulnerabilities.
    - Contributes to at least one of the following: 
        - Increasing local capacity and resilience in health systems. 
        - Enabling informed decision-making by governments, local health systems, or aid groups. 
        - Improving accessibility and quality of health services for underserved groups. 
        - Enabling continuity of care, particularly for primary health, complex diseases, or mental health.\n
    - Is technology-based or leverages innovation to strengthen health infrastructure, ensure actionable health data, or improve governance and coordination in fragile contexts.
    <criterion_3>
    """,
    "criterion_4":"""
    <criterion_4>
    Criterion 4
    Assess whether the proposal meets the technology critera. Every Solve solution must include technology, whether it's new or existing, high-tech or low-tech. To determine if the solution passes this sub-criterion:
        - carefully examine the solution's core components and determine whether technology plays a central role in enabling or delivering the intended impact.
        - ask yourself: \"If the technology component was removed from this solution, would it still work?\"
        - consider whether the technology component has the potential to significantly enhance the solution's scale, efficiency, or effectiveness compared to non-technological alternatives
    <criterion_4>
    """,
    "criterion_5":"""
    <criterion_5>
    Criterion 5
    Assess whether the proposal's quality is good enough to warrant reviewers taking the time to read and score it. When evaluating the proposal, consider the Clarity, Coherence, and Persuasiveness for the final assessment:
        - Are the responses presented clearly and maintained a consistent focus throughout?
        - Does the proposal present a unique or innovative approach to solving the problem?
        - Is there a compelling value proposition or potential for significant impact? 
        - Are the responses and justifications presented in a logical and persuasive manner?
    <criterion_5>
    """,
    "prompt_summary": """
        Please generate a detailed summary of the provided solution proposal according to the following criteria:
        1. Base the summary solely on the information provided within the document. Utilize a neutral tone throughout to present a balanced view without using subjective or positive adjectives such as 'excellent,' 'effective,' or 'innovative.'
        2. Include all critical information necessary for screeners and judges to evaluate the proposal effectively.
        3. Clearly specify the development stage of the product, service, or business model (e.g., Concept, Pilot, Prototype, Growth, Scale), and provide evidence from the proposal that supports the claimed stage of development.
        4. Ensure the summary within 200 - 300 words but remains concise, avoiding unnecessary details while focusing on key elements.
        5. Avoid generating a concluding paragraph that re-summarizes the content or provides an evaluative perspective on the information or your comments.  
        """,

        "prompt_skip_criteria" : """
            As a solution proposal screener, you are given solution id, solution proposal, assessing criteria, and skip criteria. Some solutions can skip some criteria. Your task is to assess the given solution section based on the criteria. Skip some criteria if it is indicated and provide your assessment for the remaining criteria. After carefully analyzing the proposal step by step, provide your final assessment with following information in valid JSON format without any additional text or explanations:
                {
                    "id": "",
                    "assessment": {
                        "criterion_n": {
                            "result": "'pass' or 'fail'",
                            "reason": "provide reasoning of your assessment."
                        },...
                    }
                }
        """
}

def get_prompt_list():
    return list(prompts.keys())

def get_prompt(prompt_name):
    try:
        return prompts[prompt_name]
    except KeyError:
        return "Prompt not found"