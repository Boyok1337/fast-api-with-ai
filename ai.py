# import os
# from dotenv import load_dotenv
# import google.generativeai as genai  # Assuming this is a hypothetical import
#
# load_dotenv()
# genai.configure(api_key=os.environ["google_ai_api_key"])
# MODEL = genai.GenerativeModel('gemini-1.5-flash')
#
# test = "hello"
# response = MODEL.generate_content(test)
#
# # List of harmful content categories
# HARM_PROBABILITY = [
#     "MEDIUM",
#     "HIGH"
# ]
#
#
# # Convert response to string for easy search
# print(response)
# response_str = str(response)
#
# # Check if any harmful category exists in the response string
# contains_harmful_content = any(category in response_str for category in HARM_PROBABILITY)
#
# # Return false if harmful content is detected
# result = "false" if contains_harmful_content else "true"
#
# print(result)
