import random
def health_facts_of_the_day():
    li= [
        "Drinking water can help improve your metabolism.",
        "Regular exercise can boost your mood and energy levels.",
        "Getting enough sleep is crucial for overall health.",
        "Eating a balanced diet can help maintain a healthy weight.",
        "Taking breaks during work can improve productivity and reduce stress.",
        "Include more fruits and vegetables for vitamins and fiber.",
        "Choose whole grains over refined grains to increase fiber intake.",
        "Limit added sugars and sugary drinks to reduce empty calories.",
        "Prefer lean proteins like fish, poultry, beans, and legumes.",
        "Watch portion sizes to avoid overeating.",
        "Include healthy fats such as avocados, nuts, and olive oil in moderation.",
        "Plan meals and prep healthy snacks to avoid processed food choices.",
        "Read nutrition labels to make informed food choices.",
        "Practice mindful eating: slow down and savor your food.",
        "Stay consistent with regular meal times to help regulate appetite."
        "Favor whole-food snacks like nuts, seeds, and fresh fruit over packaged bars.",
        "Add legumes (lentils, chickpeas, black beans) to meals to boost protein and fiber.",
        "Try meatless meals a few times a week to diversify nutrients and reduce saturated fat.",
        "Choose healthy cooking oils (olive, avocado) and avoid trans fats.",
        "Include a variety of colorful vegetables to maximize vitamins and antioxidants.",
        "Consume fermented foods (yogurt, kefir, sauerkraut) to support gut health.",
        "Prioritize lean cuts of meat and remove visible fat when possible.",
        "Swap sugary dressings for vinegar-based or citrusy vinaigrettes.",
        "Replace sugary desserts with fresh fruit or yogurt parfaits.",
        "Limit high-sodium condiments and rinse canned foods to reduce salt intake.",
        "Use herbs and spices to enhance flavor instead of extra salt or sugar.",
        "Cook large batches and freeze portions to help maintain healthy choices on busy days."
    ]
    return random.choice(li)
#test
if __name__ == "__main__":
    print(health_facts_of_the_day())



def health_facts(bmi: float, category: str) -> list[str]:
    """Return short, evidence-based health facts related to the BMI category."""
    facts = {
        "Underweight": [
            "Low BMI is linked with lower muscle mass and potential nutrient deficiencies.",
            "Being underweight can weaken the immune system and reduce energy levels."
        ],
        "Normal weight": [
            "A healthy BMI correlates with lower risk of diabetes and heart disease.",
            "Maintaining this range is associated with better mobility and metabolism."
        ],
        "Overweight": [
            "Moderately high BMI increases the chance of developing hypertension.",
            "Extra body weight can gradually strain joints, especially knees."
        ],
        "Obesity class I": [
            "Higher BMI is linked with elevated blood pressure and cholesterol.",
            "Weight loss of even 5–10% significantly reduces long-term risks."
        ],
        "Obesity class II": [
            "This BMI range is strongly connected with type 2 diabetes risk.",
            "Cardiovascular strain increases significantly in this category."
        ],
        "Obesity class III": [
            "Very high BMI greatly elevates risk for heart disease and respiratory issues.",
            "Professional medical supervision is strongly recommended."
        ]
    }
    return facts.get(category, [])



def exercise_plan(category: str) -> list[str]:
    """Suggest beginner-friendly exercises depending on BMI category."""
    plans = {
        "Underweight": [
            "Light strength training to build muscle mass.",
            "Yoga or pilates for posture and flexibility."
        ],
        "Normal weight": [
            "30 minutes of brisk walking or jogging.",
            "Body-weight training 3–4 times per week."
        ],
        "Overweight": [
            "Low-impact cardio like cycling or swimming.",
            "Strength training with light weights to build metabolism."
        ],
        "Obesity class I": [
            "Walking 20–30 minutes daily at a comfortable pace.",
            "Chair exercises or light resistance band workouts."
        ],
        "Obesity class II": [
            "Short interval walks (5–10 minutes each).",
            "Water-based exercises to reduce joint strain."
        ],
        "Obesity class III": [
            "Supervised physiotherapy or guided low-impact routines.",
            "Focus on mobility and breathing exercises."
        ]
    }
    return plans.get(category, [])



def diet_suggestions(category: str) -> list[str]:
    """Simple dietary guidance, non-medical."""
    diets = {
        "Underweight": [
            "Add calorie-dense foods like nuts, peanut butter, and dairy.",
            "Increase protein intake to help muscle growth."
        ],
        "Normal weight": [
            "Balanced meals with vegetables, fruits, grains, and lean proteins.",
            "Keep hydrated and avoid excessive processed foods."
        ],
        "Overweight": [
            "Reduce sugary drinks and replace with water.",
            "Increase fiber intake using vegetables and whole grains."
        ],
        "Obesity class I": [
            "Portion control and reducing high-fat snacks help greatly.",
            "Add lean proteins and vegetables while reducing fried foods."
        ],
        "Obesity class II": [
            "Avoid high-calorie fast foods; choose home-cooked meals.",
            "Switch to whole grains instead of refined carbs."
        ],
        "Obesity class III": [
            "Professional dietary planning is strongly recommended.",
            "Focus on slow, sustainable changes instead of crash diets."
        ]
    }
    return diets.get(category, [])



def warnings(category: str) -> list[str]:
    """Optional warnings for risky categories."""
    danger_zones = {
        "Underweight": [
            "Severely low BMI may indicate nutritional deficiency.",
            "Consider consulting a doctor if fatigue or weakness persists."
        ],
        "Obesity class II": [
            "High risk of developing cardiac and metabolic issues.",
        ],
        "Obesity class III": [
            "Very high health risk. Medical guidance is important.",
        ]
    }
    return danger_zones.get(category, [])



def generate_suggestions(bmi: float, category: str) -> dict:
    """
    Combine all suggestions into one dictionary for easy use in GUI or CLI.
    Returns:
        {
            "health_facts": [...],
            "exercise_plan": [...],
            "diet": [...],
            "warnings": [...]
        }
    """
    return {
        "health_facts": health_facts(bmi, category),
        "exercise_plan": exercise_plan(category),
        "diet": diet_suggestions(category),
        "warnings": warnings(category)
    }
