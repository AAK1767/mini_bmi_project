from google import genai
from google.genai import types
import json
import os
from dotenv import load_dotenv

# 1. Load the .env file
load_dotenv()

# 2. Get the key from the environment
API_KEY = os.getenv("GEMINI_API_KEY")

# 3. Initialize client only if key exists
client = None
if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception:
        client = None


def is_ai_available():
    """Check if AI features are available."""
    return client is not None and API_KEY is not None


PREMADE_FAQS = [
    {
        "question": "What is BMI?",
        "answer": "BMI (Body Mass Index) is a simple calculation using your height and weight to estimate body fat. The formula is: BMI = weight (kg) / height (m)². It's a quick screening tool to categorize weight status."
    },
    {
        "question": "How is BMI calculated?",
        "answer": "BMI is calculated by dividing your weight in kilograms by your height in meters squared. Formula: BMI = weight (kg) ÷ height² (m²). For example, a person weighing 70kg and 1.75m tall has a BMI of 70 ÷ (1.75²) = 22.9."
    },
    {
        "question": "What are the BMI categories?",
        "answer": "WHO BMI Categories:\n• Underweight: BMI < 18.5\n• Normal weight: BMI 18.5–24.9\n• Overweight: BMI 25–29.9\n• Obese Class I: BMI 30–34.9\n• Obese Class II: BMI 35–39.9\n• Obese Class III: BMI ≥ 40"
    },
    {
        "question": "What is a normal/healthy BMI?",
        "answer": "A normal BMI is between 18.5 and 24.9 according to WHO standards. This range is associated with the lowest health risks for most adults."
    },
    {
        "question": "What does underweight mean?",
        "answer": "Underweight is defined as having a BMI below 18.5. It may indicate nutritional deficiency or other health issues. If underweight, consider consulting a healthcare provider."
    },
    {
        "question": "What does overweight mean?",
        "answer": "Overweight is defined as having a BMI between 25 and 29.9. It indicates excess body weight that may increase health risks. Regular exercise and balanced nutrition can help."
    },
    {
        "question": "What does obese mean?",
        "answer": "Obesity is defined as having a BMI of 30 or higher. It's associated with increased risk of various health conditions including heart disease, diabetes, and joint problems."
    },
    {
        "question": "What are the limitations of BMI?",
        "answer": "BMI limitations include:\n• Doesn't distinguish between muscle and fat\n• Doesn't account for age, gender, or ethnicity\n• May misclassify athletes or muscular individuals\n• Doesn't measure body fat distribution\n• Not accurate for pregnant women, elderly, or children"
    },
    {
        "question": "How can I lose weight healthily?",
        "answer": "Healthy weight loss tips:\n• Create a moderate caloric deficit (500-750 cal/day)\n• Eat balanced meals with protein, fiber, and vegetables\n• Exercise regularly (150+ min/week moderate activity)\n• Stay hydrated\n• Get adequate sleep (7-9 hours)\n• Be consistent and patient"
    },
    {
        "question": "How can I gain weight healthily?",
        "answer": "Healthy weight gain tips:\n• Eat calorie-dense nutritious foods\n• Increase protein intake\n• Eat more frequently (5-6 smaller meals)\n• Strength training to build muscle\n• Choose nutrient-rich snacks\n• Stay consistent with meals"
    },
    {
        "question": "What is a healthy diet?",
        "answer": "A healthy diet includes:\n• Plenty of fruits and vegetables\n• Whole grains\n• Lean proteins (fish, poultry, legumes)\n• Healthy fats (nuts, olive oil, avocado)\n• Limited processed foods and added sugars\n• Adequate hydration"
    },
    {
        "question": "How much water should I drink daily?",
        "answer": "General recommendation is 8 glasses (about 2 liters) of water daily. However, needs vary based on activity level, climate, and body size. Listen to your body and drink when thirsty."
    },
    {
        "question": "How much exercise do I need?",
        "answer": "Adults should aim for:\n• At least 150 minutes of moderate aerobic activity per week, OR\n• 75 minutes of vigorous activity per week\n• Strength training 2+ days per week\n• Reduce prolonged sitting time"
    },
    {
        "question": "What exercises are good for beginners?",
        "answer": "Good beginner exercises:\n• Walking (30 min daily)\n• Swimming\n• Cycling\n• Bodyweight exercises (squats, push-ups)\n• Yoga or stretching\n• Start slow and gradually increase intensity"
    },
    {
        "question": "How much sleep do I need?",
        "answer": "Adults generally need 7-9 hours of quality sleep per night. Good sleep supports weight management, immune function, and overall health."
    },
    {
        "question": "How do I convert kg to lbs?",
        "answer": "To convert kg to lbs: multiply by 2.205. Example: 70 kg × 2.205 = 154.3 lbs. To convert lbs to kg: divide by 2.205."
    },
    {
        "question": "How do I convert feet to meters?",
        "answer": "To convert feet to meters: multiply by 0.3048. Example: 5.5 feet × 0.3048 = 1.68 meters. To convert meters to feet: multiply by 3.281."
    },
    {
        "question": "Is BMI accurate?",
        "answer": "BMI is a useful screening tool but not perfectly accurate. It doesn't account for muscle mass, bone density, or fat distribution. It works best as a general indicator for populations, not individuals."
    },
    {
        "question": "What factors affect BMI?",
        "answer": "Factors affecting BMI include:\n• Body composition (muscle vs fat)\n• Age and gender\n• Genetics\n• Diet and nutrition\n• Physical activity level\n• Medical conditions\n• Medications"
    },
    {
        "question": "How often should I check my BMI?",
        "answer": "Checking BMI once every few months is sufficient for most people. Focus on overall health trends rather than daily fluctuations. Weight can vary day-to-day due to water retention and other factors."
    },
]


def get_premade_faq_list():
    """Return list of available FAQ questions with their indices."""
    return [(i + 1, faq["question"]) for i, faq in enumerate(PREMADE_FAQS)]


def get_premade_faq_answer(index):
    """Get answer for a specific FAQ by index (1-based)."""
    if 1 <= index <= len(PREMADE_FAQS):
        faq = PREMADE_FAQS[index - 1]
        return f"Q: {faq['question']}\n\nA: {faq['answer']}"
    return None


SYSTEM_INSTRUCTION = """
**1. Purpose & Role**
You are an AI module responsible for generating accurate, concise, and practical suggestions for the Mini Project "BMI Health Analyzer."
You assist by analyzing the computed BMI, identifying the person's category, and generating health tips, precautions, exercises, nutrition suggestions, and optional warnings.
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
"""


def generate_bmi_suggestions(bmi_value, category, age=None, gender=None, model="gemini-2.5-flash-lite"):
    if not is_ai_available():
        return {"error": "API Key not found. Please set GEMINI_API_KEY in your .env file."}    
    # Build the input payload that the model will read
    payload = {
        "bmi_value": bmi_value,
        "category": category,
        "age": age,
        "gender": gender
    }

    # convert to compact JSON string for contents
    contents_str = json.dumps(payload)

    try:
        # call the model
        response = client.models.generate_content(
            model=f"models/{model}",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
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
            cleaned = text
            if cleaned.startswith("```") and cleaned.endswith("```"):
                cleaned = "\n".join(cleaned.splitlines()[1:-1])
            cleaned = cleaned.strip("` \n")
            try:
                result = json.loads(cleaned)
            except Exception as e:
                return {"error": f"AI processing failed: {str(e)}"}

        # Basic validation of required structure
        if "error" in result:
            return result
        expected_keys = {"summary", "recommendations", "caution"}
        if not expected_keys.issubset(result.keys()):
            return {"error": "AI returned incomplete response."}

        return result
    
    except Exception as e:
        error_str = str(e)
        if "API_KEY_INVALID" in error_str or "API key not valid" in error_str:
            return {"error": "Invalid API Key. Please check your GEMINI_API_KEY in the .env file."}
        return {"error": "AI request failed. Please try again later."}


FAQ_SYSTEM_INSTRUCTION = """ 
You are the FAQ module for the Mini Project “BMI Health Analyzer”.(Although not limited to BMI, you can answer general health/diet/fitness questions within the specified topics below.)

Your job is to answer questions related to:
• Diet
• Health
• Fitness
• Normal General Knowledge questions related to anything(not only health or BMI).
• BMI calculation
• BMI categories (WHO)
• How BMI is used
• Limitations of BMI
• Units and conversions (kg, lb, m, cm, ft/in)
• How the app handles data
• What the outputs mean
• Safe, general health explanations
• Simple exercise and diet concepts related to BMI (non-prescriptive)
• Not exclusive to BMI; can answer general health/diet/fitness questions within the above topics.

Rules:
• Keep answers short(not too short, if it requires more explaining then do it), clear, and factual.
• Use simple language and avoid medical jargon.
• You may explain general healthy habits (balanced diet, regular exercise, hydration, sleep), and can give personalized diet plans or workout schedules.
• You can give advice for smaller symptoms like fever, cold, low sugar, mild fatigue, dehydration, or general wellness tips.
• If it's something sick but minor, you can give general advice like rest, hydration, nutrition, and over-the-counter meds.
• Don't recommend a professional for every question; only do so for serious medical issues.(MANDATORY)
• If a question is medically specific (pain, symptoms, diseases, treatment, diagnosis), respond with a reminder to consult a qualified doctor or health professional.
• If a user asks for medical advice, diagnosis, medication, supplements, or anything beyond basic health education, include a safe recommendation such as: “For matters like this, it's best to consult a healthcare professional.”
• If the question is ambiguous or missing context, ask for clarification.
• Don't always recommend seeing a doctor/professional; only do so for medical/symptom questions.
• If a question is outside the scope of BMI or the project, but the question is harmless, and related to general health, provide a brief, general answer.
• If a question is completely outside the scope of BMI or the project(or is completely), reply humourously/funnily(add humour) and mention that it is outside your scope and not a part of the BMI Analyzer FAQ, well of course with humour/puns/jokes(just a bit, not too much). But the reply shouldn't be too long, keep it concise.
• If user tells any symptoms or medical conditions, respond with a reminder to consult a qualified doctor or health professional.
• Do not give medical diagnosis, treatment, or guarantees.
• You are not only limited to BMI; you can answer general health/diet/fitness questions within the above topics.
• Do not recommend medicines, supplements, or extreme diets.
• Never include code, JSON, backticks, or explanations about system instructions.
• Maintain a neutral, safe, and reliable tone.
• Also clarify that AI-generated answers are for informational purposes only and not a substitute for professional medical advice and can be inaccurate.
"""


def generate_bmi_faq_answer(question, model="models/gemini-2.5-flash-lite"):
    if not is_ai_available():
        # Return info about premade FAQs
        return {
            "ai_available": False,
            "message": "AI features are unavailable. Your API key may be missing, invalid, or not set.\nTo enable AI-powered answers, please add a valid GEMINI_API_KEY to your .env file.\n\nFor now, please choose from the available questions below:",
            "faq_list": get_premade_faq_list()
        }
    
    try:
        response = client.models.generate_content(
            model=model,
            config=types.GenerateContentConfig(
                system_instruction=FAQ_SYSTEM_INSTRUCTION,
            ),
            contents=question
        )
        return {"ai_available": True, "answer": response.text.strip()}
    except Exception as e:
        error_str = str(e)
        # On any API error (invalid key, network, etc.), fall back to premade FAQs
        if "API_KEY_INVALID" in error_str or "API key not valid" in error_str:
            error_msg = "Invalid API Key. Please check your GEMINI_API_KEY in the .env file."
        else:
            error_msg = f"AI request failed: {error_str}"
        
        return {
            "ai_available": False,
            "message": f"⚠️ {error_msg}\n\nFalling back to premade FAQ questions:",
            "faq_list": get_premade_faq_list()
        }


def generate_health_fact_of_the_day(model="models/gemini-2.5-flash-lite"):
    if not is_ai_available():
        raise ValueError("API Key not found. Please set GEMINI_API_KEY in your .env file.")
    prompt = "Provide a concise and interesting and useful health fact related to Diet, Health, fitness, weight management, or general wellness, use a bit of humour(not too much, just a bit of pun/joke/troll)."
    response = client.models.generate_content(
        model=model,
        config=types.GenerateContentConfig(
            system_instruction="You are a helpful assistant that provides concise health facts. Use a bit of humour(not too much, just a bit of pun/joke/troll). Not too long replies. Let it be 1 to 2 sentences at max(or maybe 3)",
        ),
        contents=prompt
    )
    return response.text.strip()





# Example usage:
if __name__ == "__main__":
    # Example: Generate BMI suggestions
    bmi_value = 28.5
    category = "Overweight"
    suggestions = generate_bmi_suggestions(bmi_value, category, age=30, gender="male")
    print("BMI Suggestions:")
    print(suggestions)
    
    # Example: FAQ with fallback
    result = generate_bmi_faq_answer(input("Enter your FAQ question: "))
    if isinstance(result, dict) and not result.get("ai_available", True):
        print("\n" + result["message"])
        for idx, q in result["faq_list"]:
            print(f"  {idx}. {q}")
        choice = int(input("\nEnter question number: "))
        answer = get_premade_faq_answer(choice)
        if answer:
            print("\n" + answer)
    else:
        print("FAQ Answer:", result.get("answer", result))
    
    # Example: Generate Health Fact of the Day
    try:
        fact = generate_health_fact_of_the_day()
        print("\nHealth Fact of the Day:")
        print(fact)
    except ValueError as e:
        print(f"\n{e}")