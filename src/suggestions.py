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
        "Stay consistent with regular meal times to help regulate appetite.",
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



def health_facts(bmi: float, category: str) -> list[str]:
    """Return short, evidence-based health facts related to the BMI category."""
    facts = {
        "Underweight": [
            "Low BMI is linked with lower muscle mass and potential nutrient deficiencies.",
            "Being underweight can weaken the immune system and reduce energy levels.",
            "Inadequate body weight may affect bone density and increase fracture risk.",
            "Low BMI can impact hormonal balance and reproductive health.",
            "Underweight individuals may experience difficulty maintaining body temperature."
        ],
        "Normal weight": [
            "A healthy BMI correlates with lower risk of diabetes and heart disease.",
            "Maintaining this range is associated with better mobility and metabolism.",
            "Normal weight range supports optimal hormone production and balance.",
            "People in this range typically have better sleep quality and energy levels.",
            "This BMI range is associated with improved longevity and quality of life."
        ],
        "Overweight": [
            "Moderately high BMI increases the chance of developing hypertension.",
            "Extra body weight can gradually strain joints, especially knees.",
            "Overweight status may lead to sleep apnea and breathing difficulties.",
            "Even modest weight loss can significantly improve cholesterol levels.",
            "Carrying extra weight can increase inflammation throughout the body."
        ],
        "Obesity class I": [
            "Higher BMI is linked with elevated blood pressure and cholesterol.",
            "Weight loss of even 5–10% significantly reduces long-term risks.",
            "This BMI range increases risk of developing fatty liver disease.",
            "Joint problems and arthritis become more common at this weight range.",
            "Risk of certain cancers increases with higher BMI levels."
        ],
        "Obesity class II": [
            "This BMI range is strongly connected with type 2 diabetes risk.",
            "Cardiovascular strain increases significantly in this category.",
            "Breathing difficulties and reduced lung capacity are common concerns.",
            "Risk of stroke and heart attack is notably elevated.",
            "Mobility and physical function can be significantly impacted."
        ],
        "Obesity class III": [
            "Very high BMI greatly elevates risk for heart disease and respiratory issues.",
            "Professional medical supervision is strongly recommended.",
            "This category carries highest risk for metabolic syndrome.",
            "Life expectancy can be significantly reduced without intervention.",
            "Multiple organ systems may be affected, requiring comprehensive care."
        ]
    }
    return facts.get(category, [])



def exercise_plan(category: str) -> list[str]:
    """Suggest beginner-friendly exercises depending on BMI category."""
    plans = {
        "Underweight": [
            "light strength training to build muscle mass.",
            "yoga or pilates for posture and flexibility.",
            "resistance band exercises 3 times per week.",
            "progressive weight training with proper nutrition support.",
            "balance and stability exercises like tai chi."
        ],
        "Normal weight": [
            "30 minutes of brisk walking or jogging.",
            "body-weight training 3-4 times per week.",
            "mix of cardio and strength training for overall fitness.",
            "try sports activities like tennis, basketball, or swimming.",
            "high-intensity interval training (HIIT) 2-3 times weekly.",
            "incorporate flexibility exercises and stretching routines."
        ],
        "Overweight": [
            "low-impact cardio like cycling or swimming.",
            "strength training with light weights to build metabolism.",
            "brisk walking for 30-45 minutes daily.",
            "water aerobics to reduce joint stress.",
            "elliptical training for cardiovascular fitness.",
            "gradual progression to include light jogging intervals."
        ],
        "Obesity class I": [
            "walking 20-30 minutes daily at a comfortable pace.",
            "chair exercises or light resistance band workouts.",
            "swimming or pool exercises for full-body workout.",
            "stationary cycling starting with short sessions.",
            "gentle stretching and range-of-motion exercises.",
            "seated strength training to build muscle safely."
        ],
        "Obesity class II": [
            "short interval walks (5-10 minutes each).",
            "water-based exercises to reduce joint strain.",
            "chair yoga and seated exercises.",
            "arm exercises with very light weights or resistance bands.",
            "breathing exercises and gentle stretching.",
            "gradual increase in daily movement and activity."
        ],
        "Obesity class III": [
            "supervised physiotherapy or guided low-impact routines.",
            "focus on mobility and breathing exercises.",
            "assisted standing and sitting exercises.",
            "pool therapy under professional guidance.",
            "gentle range-of-motion exercises to maintain flexibility.",
            "focus on building daily activity tolerance gradually."
        ]
    }
    return plans.get(category, [])



def diet_suggestions(category: str) -> list[str]:
    """Simple dietary guidance, non-medical."""
    diets = {
        "Underweight": [
            "Add calorie-dense foods like nuts, peanut butter, and dairy.",
            "Eat"
            "Increase protein intake to help muscle growth.",
            "Eat more frequent, smaller meals throughout the day.",
            "Include healthy fats from avocados, olive oil, and fatty fish.",
            "Add protein shakes or smoothies with fruits and nut butters.",
            "Choose nutrient-dense carbohydrates like sweet potatoes and oats."
        ],
        "Normal weight": [
            "Balanced meals with vegetables, fruits, grains, and lean proteins.",
            "Perfect"
            "Keep hydrated and avoid excessive processed foods.",
            "Practice portion control to maintain current weight.",
            "Include variety in your diet for all essential nutrients.",
            "Limit alcohol and sugary beverages.",
            "Plan meals ahead to avoid unhealthy impulse choices."
        ],
        "Overweight": [
            "Reduce sugary drinks and replace with water.",
            "Eat less"
            "Increase fiber intake using vegetables and whole grains.",
            "Control portion sizes using smaller plates.",
            "Eat more vegetables and fruits, aim for 5-7 servings daily.",
            "Choose lean proteins like chicken, fish, and legumes.",
            "Reduce consumption of fried and high-fat foods.",
            "Keep healthy snacks available to avoid junk food."
        ],
        "Obesity class I": [
            "Portion control and reducing high-fat snacks help greatly.",
            "Add lean proteins and vegetables while reducing fried foods.",
            "Don't eat"
            "Track daily calorie intake to increase awareness.",
            "Eliminate sugary sodas and juice drinks.",
            "Increase water intake to 8-10 glasses daily.",
            "Plan meals with half the plate being vegetables.",
            "Reduce eating out and prepare more meals at home."
        ],
        "Obesity class II": [
            "Avoid high-calorie fast foods; choose home-cooked meals.",
            "Switch to whole grains instead of refined carbs.",
            "No eating"
            "Work with a nutritionist for personalized meal planning.",
            "Focus on vegetables, lean proteins, and controlled portions.",
            "Eliminate late-night snacking and emotional eating.",
            "Keep a food diary to identify problem areas.",
            "Choose baked, grilled, or steamed foods over fried options."
        ],
        "Obesity class III": [
            "Professional dietary planning is strongly recommended.",
            "Focus on slow, sustainable changes instead of crash diets.",
            "Work with medical team for structured weight loss program.",
            "No eating at all"
            "Start with small achievable goals like reducing one unhealthy food.",
            "Consider medically supervised meal replacement programs.",
            "Address emotional eating with professional support.",
            "Focus on whole, unprocessed foods in controlled portions."
        ]
    }
    return diets.get(category, [])



def warnings(category: str) -> list[str]:
    """Optional warnings for risky categories."""
    danger_zones = {
        "Underweight": [
            "Severely low BMI may indicate nutritional deficiency.",
            "Consider consulting a doctor if fatigue or weakness persists.",
            "Prolonged underweight status can affect bone health.",
            "May indicate underlying medical conditions requiring evaluation."
        ],
        "Overweight": [
            "Monitor blood pressure and cholesterol levels regularly.",
            "Early intervention can prevent progression to obesity."
        ],
        "Obesity class I": [
            "Regular health screenings are recommended.",
            "Consider medical consultation for weight management strategies."
        ],
        "Obesity class II": [
            "High risk of developing cardiac and metabolic issues.",
            "Medical supervision recommended for safe weight loss.",
            "Regular monitoring of blood sugar and blood pressure essential."
        ],
        "Obesity class III": [
            "Very high health risk. Medical guidance is important.",
            "Immediate medical consultation strongly advised.",
            "May require comprehensive medical evaluation and treatment plan.",
            "Consider discussing surgical weight loss options with physician."
        ]
    }
    return danger_zones.get(category, [])



def generate_suggestions(bmi: float, category: str) -> dict:
    """
    Combine all suggestions into one dictionary for easy use in GUI or CLI.
    Demonstrates: list comprehension, map, and filter.
    Returns:
        {
            "health_facts": [...],
            "exercise_plan": [...],
            "diet": [...],
            "warnings": [...]
        }
    """
    raw_facts = health_facts(bmi, category)
    raw_exercises = exercise_plan(category)
    raw_diet = diet_suggestions(category)
    raw_warnings = warnings(category)
    
    # LIST COMPREHENSION: Add bullet formatting to facts
    formatted_facts = [f"• {fact}" for fact in raw_facts]
    
    # MAP: Capitalize first letter of each exercise suggestion
    formatted_exercises = list(map(lambda x: x.strip().capitalize(), raw_exercises))
    
    # FILTER: Only include diet tips longer than 20 characters (more detailed tips)
    detailed_diet = list(filter(lambda tip: len(tip) > 20, raw_diet))
    
    return {
        "health_facts": formatted_facts,
        "exercise_plan": formatted_exercises,
        "diet": detailed_diet if detailed_diet else raw_diet,  # fallback if all filtered out
        "warnings": raw_warnings
    }

# Example usage:
if __name__ == "__main__":
    # Health Facts of the Day
    print(health_facts_of_the_day())
    bmi_value = 32.5
    category = "Obesity class I"
    suggestions = generate_suggestions(bmi_value, category)
    print("Health Facts:")
    for fact in suggestions["health_facts"]:
        print(fact)
    print("\nExercise Plan:")
    for exercise in suggestions["exercise_plan"]:
        print(f"- {exercise}")
    print("\nDiet Suggestions:")
    for diet_tip in suggestions["diet"]:
        print(f"- {diet_tip}")
    if suggestions["warnings"]:
        print("\nWarnings:")
        for warning in suggestions["warnings"]:
            print(f"⚠️ {warning}")