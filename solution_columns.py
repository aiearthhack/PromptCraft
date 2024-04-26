challenge_2023 = {
    0: "Solution ID",
    1: "Challenge Name",
    2: "Solution Status",
    3: "Provide a one-line summary of your solution.",
    4: "What specific problem are you solving?",
    5: "What is your solution?",
    6: "Who does your solution serve, and in what ways will the solution impact their lives?",
    7: "How are you and your team well-positioned to deliver this solution?",
    8: "Which dimension of the Challenge does your solution most closely address?",
    9: "In what city, town, or region is your solution team headquartered?",
    10: "In what country is your solution team headquartered?",
    11: "What is your solution's stage of development?",
    12: "Please share details about what makes your solution a Prototype rather than a Concept.",
    13: "How many people does your solution currently serve?",
    14: "Why are you applying to Solve?",
    15: "In which of the following areas do you most need partners or support?",
    16: "Is your solution an active or past participant in another entrepreneurship network?",
    17: "Please share the names of the other entrepreneurship networks.",
    18: "How did you first hear about Solve?",
    19: "Tell us more about how you found out about Solve’s 2023 Global Challenges.",
    20: "What makes your solution innovative?",
    21: "What are your impact goals for the next year and the next five years, and how will you achieve them?",
    22: "Which of the UN Sustainable Development Goals does your solution address?",
    23: "How are you measuring your progress toward your impact goals?",
    24: "What is your theory of change?",
    25: "Describe the core technology that powers your solution.",
    26: "Which of the following categories best describes your solution?",
    27: "How do you know that this technology works?",
    28: "Please select the technologies currently used in your solution:",
    29: "In which countries do you currently operate?",
    30: "In which countries will you be operating within the next year?",
    31: "What type of organization is your solution team?",
    32: "If you selected Other, please explain here.",
    33: "How many people work on your solution team?",
    34: "How long have you been working on your solution?",
    35: "What is your approach to incorporating diversity, equity, and inclusivity into your work?",
    36: "What is your business model?",
    37: "Do you primarily provide products or services directly to individuals, to other organizations, or to the government?",
    38: "What is your plan for becoming financially sustainable?",
    39: "Share some examples of how your plan to achieve financial sustainability has been successful so far."
}

challenge_2024 = {
    0: "Solution ID",
    1: "Challenge Name",
    2: "Provide a one-line summary of your solution.",
    3: "In what city, town, or region is your solution team headquartered?",
    4: "In what country is your solution team headquartered?",
    5: "What type of organization is your solution team?",
    6: "If you selected Other, please explain here.",
    7: "What specific problem are you solving?",
    8: "What is your solution?",
    9: "Who does your solution serve, and in what ways will the solution impact their lives?",
    10: "How are you and your team well-positioned to deliver this solution?",
    11: "Which dimension of the Challenge does your solution most closely address?",
    12: "Which of the UN Sustainable Development Goals does your solution address?",
    13: "What is your solution’s stage of development?",
    14: "Please share details about why you selected the stage above.",
    15: "Why are you applying to Solve?",
    16: "In which of the following areas do you most need partners or support?",
    17: "Who is the Team Lead for your solution?",
    18: "Is the Team Lead a resident of the United States?",
    19: "Have you or someone else from your organization ever been selected as a Solver for an MIT Solve Global Challenge or for the Indigenous Communities Fellowship?",
    20: "Explain what makes your solution different from when you or your organization was previously selected.",
    21: "Is your solution an active or past participant in another entrepreneurship network?",
    22: "Please share the names of the other entrepreneurship networks.",
    23: "Did you take the MITx course “Business and Impact Planning for Social Enterprises?”",
    24: "How did you first hear about Solve?",
    25: "Tell us more about how you found out about Solve’s 2024 Global Challenges.",
    26: "What makes your solution innovative?",
    27: "Describe in simple terms how and why you expect your solution to have an impact on the problem.",
    28: "What are your impact goals for your solution and how are you measuring your progress towards them?",
    29: "Describe the core technology that powers your solution.",
    30: "Which of the following categories best describes your solution?",
    31: "How do you know that this technology works?",
    32: "Please select the technologies currently used in your solution:",
    33: "If your solution has a website, app, or social media handle, provide the link(s) here:",
    34: "In which countries do you currently operate?",
    35: "Which, if any, additional countries will you be operating in within the next year?",
    36: "How many people work on your solution team?",
    37: "How long have you been working on your solution?",
    38: "Tell us about how you ensure that your team is diverse, minimizes barriers to opportunity for staff, and provides a welcoming and inclusive environment for all team members.",
    39: "What is your business model?",
    40: "Do you primarily provide products or services directly to individuals, to other organizations, or to the government?",
    41: "What is your plan for becoming financially sustainable, and what evidence can you provide that this plan has been successful so far?"
}

def get_solution_col(solution_col_dict, col_names):
    result = ""
    for key, value in solution_col_dict.items():
        if key in col_names:
            result += f'{key}. {value}\n'
    return result