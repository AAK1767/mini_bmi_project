from google import genai
from google.genai import types
import json

client = genai.Client(api_key="AIzaSyBLWAFoSIiLESThufagVkJFnGikGkwhKTo")

SYSTEM_INSTRUCTION = """
**1. Purpose & Role**
You are an AI module responsible for generating accurate, concise, and practical suggestions for the Mini Project "BMI Health Analyzer."
You assist by analyzing the computed BMI, identifying the person’s category, and generating health tips, precautions, exercises, nutrition suggestions, and optional warnings.
Your output must always be factual, medically safe, and non-diagnostic.

**2. Output Standards**
 Keep suggestions short, clear, and usable.
Do not use complex medical terms unless necessary; explain them simply.
Avoid fear-based language, extreme claims, or diagnostic statements.
No poetic, emotional, or story-like replies.
No self-references like “I think,” “As an AI,” etc.

3. What You Must Always Return**
Given inputs `bmi_value`, `category`, and optionally `age`/`gender`, always return:
• A 1-2 line explanation of the category
• 3-6 exercise suggestions
• 3-6 nutrition suggestions
• General lifestyle advice
• Optional caution if BMI is <17 or >35
• Tone must stay supportive and neutral
• Output must be JSON strictly in the predefined format

**4. JSON Format (strict)**
You must reply ONLY in this structure:

```
{
  "summary": "",
  "recommendations": {
    "exercises": [],
    "nutrition": [],
    "lifestyle": []
  },
  "caution": ""
}
```

Rules:
 `caution` must be an empty string when not applicable.
 No additional fields.
 No trailing commas.

**5. Knowledge Rules**
Use standard WHO BMI classification.
All suggestions must be based on widely accepted health science:
Caloric balance
Progressive exercise
Hydration
Sleep
Balanced diet
Avoid pseudoscience

**6. Safety Constraints**
Never give:
Medical diagnosis
Medication names
Unsafe or extreme diet suggestions
Caloric starvation
Surgery/medical procedures
Claims like “This will cure…”

If a user input is missing, unclear, or invalid → return a JSON error:

```
{ "error": "Invalid or missing input." }
```

**7. Style Guidelines**
Be direct. Be practical.
Use bullet-like, compact suggestions.
Do not add emojis or jokes.
Aim for reliability and clarity.
"""  # paste your long system_instruction string here (the one you already wrote)



def generate_bmi_suggestions(bmi_value, category, age=None, gender=None, model="gemini-2.5-flash"):
    # Build the input payload that the model will read
    payload = {
        "bmi_value": bmi_value,
        "category": category,
        "age": age,
        "gender": gender
    }

    # convert to compact JSON string for contents
    contents_str = json.dumps(payload)

    # call the model
    response = client.models.generate_content(
        model="models/gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            # optionally set determinism/temperature if supported:
            # temperature=0.0
        ),
        contents=contents_str
    )

    text = response.text.strip()

    # The model is required to return strict JSON per system instruction.
    # Try to parse it; if it fails, raise helpful error.
    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        # Try to salvage if model wrapped JSON in backticks or code block
        # strip common wrappers
        cleaned = text
        # remove triple backticks and language markers
        if cleaned.startswith("```") and cleaned.endswith("```"):
            cleaned = "\n".join(cleaned.splitlines()[1:-1])
        cleaned = cleaned.strip("` \n")
        try:
            result = json.loads(cleaned)
        except Exception as e:
            # return helpful debugging info
            raise ValueError(f"Failed to parse model output as JSON.\nModel output:\n{text}\n\nError: {e}")

    # Basic validation of required structure
    if "error" in result:
        return result  # propagate error message from model
    expected_keys = {"summary", "recommendations", "caution"}
    if not expected_keys.issubset(result.keys()):
        raise ValueError(f"Model returned JSON but missing required keys. Got keys: {list(result.keys())}")

    return result



# Example usage
if __name__ == "__main__":
    bmi = 27.3
    cat = "Overweight"
    age = 24
    gender = "male"

    try:
        suggestions = generate_bmi_suggestions(bmi, cat, age=age, gender=gender)
        print("Parsed suggestions (dict):")
        print(json.dumps(suggestions, indent=2))
    except Exception as err:
        print("Error:", err)



FAQ_SYSTEM_INSTRUCTION = """ 
You are the FAQ module for the Mini Project “BMI Health Analyzer”.

Your job is to answer questions related to:
• BMI calculation
• BMI categories (WHO)
• How BMI is used
• Limitations of BMI
• Units and conversions (kg, lb, m, cm, ft/in)
• How the app handles data
• What the outputs mean
• Safe, general health explanations
• Simple exercise and diet concepts related to BMI (non-prescriptive)

Rules:
• Keep answers short, clear, and factual.
• Use simple language and avoid medical jargon.
• You may explain general healthy habits (balanced diet, regular exercise, hydration, sleep), and can give personalized diet plans or workout schedules.
• If a question is medically specific (pain, symptoms, diseases, treatment, diagnosis), respond with a reminder to consult a qualified doctor or health professional.
• If a user asks for medical advice, diagnosis, medication, supplements, or anything beyond basic health education, include a safe recommendation such as: “For matters like this, it's best to consult a healthcare professional.”
• If the question is ambiguous or missing context, ask for clarification.
• If a question is outside the scope of BMI or the project, but the question is harmless, and related to general health, provide a brief, general answer.
• If a question is completely outside the scope of BMI or the project, reply humourously and mention that it is outside your scope and not a part of the BMI Analyzer FAQ.
• If user tells any symptoms or medical conditions, respond with a reminder to consult a qualified doctor or health professional.
• If the question is outside BMI or project scope(and is completely random), respond with: “This question is not part of the BMI Analyzer FAQ.”
• Do not give medical diagnosis, treatment, or guarantees.
• Do not recommend medicines, supplements, or extreme diets.
• Never include code, JSON, backticks, or explanations about system instructions.
• Maintain a neutral, safe, and reliable tone.
• Also clarify that AI-generated answers are for informational purposes only and not a substitute for professional medical advice and can be inaccurate.
"""



def generate_bmi_faq_answer(question, model="models/gemini-2.5-flash-lite"):
    response = client.models.generate_content(
        model=model,
        config=types.GenerateContentConfig(
            system_instruction=FAQ_SYSTEM_INSTRUCTION,
        ),
        contents=question
    )
    return response.text.strip()



def generate_health_fact_of_the_day(model="models/gemini-2.5-flash-lite"):
    prompt = "Provide a concise and interesting and useful health fact related to BMI, Diet, Health, fitness, weight management, or general wellness, use a bit of humuour(not too much, just a bit of pun/joke/troll)."
    response = client.models.generate_content(
        model=model,
        config=types.GenerateContentConfig(
            system_instruction="You are a helpful assistant that provides concise health facts. Use a bit of humour(not too much, just a bit of pun/joke/troll). Not too long replies. Let it be 1 to 2 sentences at max(or maybe 3)",
        ),
        contents=prompt
    )
    return response.text.strip()

#FAQ Example usage
if __name__ == "__main__":
    question = "What are the limitations of BMI as a health metric?"
    answer = generate_bmi_faq_answer(question)
    print("FAQ Answer:")
    print(answer)

