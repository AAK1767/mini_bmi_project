from data_utils import save_profile
VALID_WEIGHT_UNITS = {'kg', 'lb'}
VALID_HEIGHT_UNITS = {'m', 'cm', 'in', 'ft_in'}

def log_execution(func):
    """Decorator that prints messages before and after function execution."""
    def wrapper(*args, **kwargs):
        print(f"\n[LOG] Starting calculation: {func.__name__}...")
        print(f"[LOG] Input values: {args}")
        result = func(*args, **kwargs)
        print(f"[LOG] Calculation complete!")
        print(f"[LOG] Result: {result}")
        return result
    return wrapper

def input_values():
    """
    Prompt user for weight, height, age, and sex.
    Returns:
        weight, weight_unit_choice, height (value or (feet, inches)), height_unit_choice, age, sex
    """
    try:
        #-------------------------
        #   Name Input
        #-------------------------
        name = input("Enter your name: ").strip()
        # -------------------------
        # Weight Input
        # -------------------------
        weight_units = {1: 'kg', 2: 'lb'}
        weight_unit_choice = int(input("Choose weight unit (1 for kg, 2 for lb): "))

        if weight_unit_choice not in [1, 2]:
            print("Invalid weight unit choice.")
            return None

        weight = float(input(f"Enter weight in {weight_units[weight_unit_choice]}: "))
        if weight <= 0:
            print("Weight must be positive.")
            return None

        # -------------------------
        # Height Input
        # -------------------------
        height_units = {1: 'm', 2: 'cm', 3: 'in', 4: 'ft/in'}
        height_unit_choice = int(input("Choose height unit (1 for m, 2 for cm, 3 for in, 4 for ft/in): "))

        if height_unit_choice not in [1, 2, 3, 4]:
            print("Invalid height unit choice.")
            return None

        if height_unit_choice == 4:
            feet = int(input("Enter height - feet: "))
            inches = float(input("Enter height - inches: "))

            if feet < 0 or inches < 0:
                print("Height values must be non-negative.")
                return None
            if inches >= 12:
                print("Inches must be less than 12.")
                return None
            if feet == 0 and inches == 0:
                print("Height cannot be zero.")
                return None

            height = (feet, inches)

        else:
            height = float(input(f"Enter height in {height_units[height_unit_choice]}: "))
            if height <= 0:
                print("Height must be positive.")
                return None

        # -------------------------
        # New: Age Input
        # -------------------------
        age = int(input("Enter age (years): "))
        if age <= 0:
            print("Age must be positive.")
            return None

        # -------------------------
        # New: Sex Input
        # -------------------------
        sex = input("Enter sex ('male' or 'female'): ").strip().lower()
        if sex not in ("male", "female"):
            print("Sex must be 'male' or 'female'.")
            return None

        # -------------------------
        # Return all collected values
        # -------------------------
        return name, weight, weight_unit_choice, height, height_unit_choice, age, sex

    except (ValueError, KeyError):
        print("Invalid input. Please enter numeric values.")
        return None

    


def lb_to_kg(pounds):
    """
    Convert pounds to kilograms.
    """
    kg = pounds * 0.45359237
    return kg



def inches_to_meters(inches):
    """
    Convert inches to meters.
    """
    meters = inches * 0.0254
    return meters



def feet_inches_to_meters(feet, inches):
    """
    Convert feet and inches to meters.
    """
    total_inches = (feet * 12) + inches
    meters = total_inches * 0.0254
    return meters



def cms_to_meters(cms):
    """
    Convert centimeters to meters.
    """

    meters = cms / 100
    return meters


@log_execution
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    Calculate BMI and return a float.
    Raises ValueError if height <= 0 or weight <= 0.
    """
    if height_m <= 0:
        raise ValueError("Height must be positive and non-zero.")
    if weight_kg <= 0:
        raise ValueError("Weight must be positive and non-zero.")
    return weight_kg / (height_m ** 2)



def healthy_weight_range_for_height(height_m: float, lower_bmi: float = 18.5, upper_bmi: float = 25.0):
    """
    Return (min_weight_kg, max_weight_kg) for healthy BMI range.
    """
    if height_m <= 0:
        raise ValueError("Height must be positive.")
    min_w = lower_bmi * (height_m ** 2)
    max_w = upper_bmi * (height_m ** 2)
    return round(min_w, 2), round(max_w, 2)



def calculate_bmr_mifflin(weight_kg: float, height_cm: float, age: int, sex: str) -> float:
    """
    sex: 'male' or 'female'
    Returns BMR in kcal/day using Mifflin-St Jeor formula, i.e required minimum calories per day to survive.
    """
    sex = sex.lower()
    if sex not in ("male", "female"):
        raise ValueError("sex must be 'male' or 'female'.")

    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age
    bmr += 5 if sex == "male" else -161
    return round(bmr, 2)



def recommended_water_liters_per_day(weight_kg: float) -> float:
    """
    Simple formula: liters/day = weight_kg * 0.033
    """
    if weight_kg <= 0:
        raise ValueError("Weight must be positive.")
    return round(weight_kg * 0.033, 2)



def kg_diff_to_reach_healthy(weight_kg: float, min_w: float, max_w: float):
    """
    Returns (kg_to_gain, kg_to_lose)
    Values will be 0 if not needed.
    """
    gain = round(max(0, min_w - weight_kg), 2)
    lose = round(max(0, weight_kg - max_w), 2)
    return gain, lose



def bmi_category(bmi: float) -> tuple[str, str]:
    """
    Return (category, description).
    Uses standard WHO ranges.
    """
    # thresholds: (upper_bound, category, description)
    # upper_bound is exclusive except the last one.
    thresholds = [
        (18.5, "Underweight", "Below healthy range; consider nutritional guidance."),
        (25.0, "Normal weight", "Healthy range"),
        (30.0, "Overweight", "Above healthy range; lifestyle adjustments may help."),
        (35.0, "Obesity class I", "Moderately high; medical advice is recommended."),
        (40.0, "Obesity class II", "High; increased health risks."),
        (float("inf"), "Obesity class III", "Very high; medical guidance is important.")
    ]
    for boundary, category, description in thresholds:
        if bmi < boundary:
            return category, description
    # fallback (shouldn't happen)
    return "Unknown", "No description available."

    

def bmi_report(weight, height, age, sex, weight_unit='kg', height_unit='m'):
    # Validate units using sets
    if weight_unit not in VALID_WEIGHT_UNITS:
        return "Unsupported weight unit."
    if height_unit not in VALID_HEIGHT_UNITS:
        return "Unsupported height unit."
    
    # Convert weight
    if weight_unit == 'lb':
        weight_kg = lb_to_kg(weight)
    else:  # kg
        weight_kg = float(weight)

    # Convert height
    if height_unit == 'm':
        height_m = float(height)
    elif height_unit == 'cm':
        height_m = cms_to_meters(float(height))
    elif height_unit == 'in':
        height_m = inches_to_meters(float(height))
    elif height_unit == 'ft_in':
        if isinstance(height, tuple) and len(height) == 2:
            feet, inches = height
            height_m = feet_inches_to_meters(float(feet), float(inches))
        else:
            return "Height must be a tuple (feet, inches) for 'ft_in' unit."
    else:
        return "Unsupported height unit."

    try:
        bmi_value = calculate_bmi(weight_kg, height_m)
    except ValueError as e:
        return str(e)

    # round for display only
    bmi_value_rounded = round(bmi_value, 2)
    category, description = bmi_category(bmi_value)
    bmr_value = calculate_bmr_mifflin(weight_kg, height_m * 100, age, sex)
    healthy_weight_values = healthy_weight_range_for_height(height_m)
    water_intake = recommended_water_liters_per_day(weight_kg)
    kg_to_gain, kg_to_lose = kg_diff_to_reach_healthy(weight_kg, healthy_weight_values[0], healthy_weight_values[1])

    return bmi_value_rounded, category, description, bmr_value, healthy_weight_values, water_intake, kg_to_gain, kg_to_lose



def main():
    """Main function to run the BMI calculator."""
    print("=== BMI Calculator ===\n")
    
    result = input_values()
    if result is None:
        print("\nFailed to get valid input. Please try again.")
        return
    
    name, weight, weight_unit_choice, height, height_unit_choice, age, sex = result
    
    # Map choices to unit strings
    weight_units = {1: 'kg', 2: 'lb'}
    height_units = {1: 'm', 2: 'cm', 3: 'in', 4: 'ft_in'}
    
    bmi_result = bmi_report(weight, height, age, sex, weight_units[weight_unit_choice], height_units[height_unit_choice])
    if isinstance(bmi_result, tuple):
        bmi, category, description, bmr_value, healthy_weight_values, water_intake, kg_to_gain, kg_to_lose = bmi_result
        print(f"\n=== Results ===")
        print(f"BMI: {bmi}")
        print(f"Category: {category}")
        print(f"Description: {description}")
        print(f"BMR(required minimum calories per day): {bmr_value}")
        print(f"Healthy Weight Range (kg): {healthy_weight_values}")
        print(f"Recommended Water Intake (liters/day): {water_intake}")
        print(f"Kg to Gain: {kg_to_gain}")
        print(f"Kg to Lose: {kg_to_lose}")
        profile = {
        "name": name,
        "age": age,
        "weight": weight,
        "height": height,
        "bmi": bmi,
        "category": category,
        "sex": sex,
        "bmr": bmr_value,
        "healthy_weight_range": healthy_weight_values,
        "recommended_water_intake": water_intake,
        "kg_to_gain": kg_to_gain,
        "kg_to_lose": kg_to_lose
        }
        save_profile(profile)   
    else:
        print(f"\nError: {bmi_result}")




if __name__ == "__main__":
    main()