def input_values():
    """
    Prompt user for weight and height inputs.
    Returns:
    weight: Weight in pounds.
    height_feet: Height in feet.
    height_inches: Additional height in inches.
    """
    try:
        weight_units={1: 'kg', 2: 'lb'}
        weight_unit_choice = int(input("Choose weight unit (1 for kg, 2 for lb): "))

        if weight_unit_choice not in [1, 2]:
            print("Invalid weight unit choice.")
            return None

        weight = float(input(f"Enter weight in {weight_units[weight_unit_choice]}: "))
        if weight <= 0:
            print("Weight must be a positive number.")
            return None
        height_units={1: 'm', 2: 'cm', 3: 'in', 4: 'ft/in'}
        height_unit_choice = int(input("Choose height unit (1 for m, 2 for cm, 3 for in, 4 for ft_in): "))
        if height_unit_choice not in [1, 2, 3, 4]:
            print("Invalid height unit choice.")
            return None
        
        if height_unit_choice == 4:
            height_feet = int(input("Enter height - feet: "))
            height_inches = float(input("Enter height - inches: "))
            if (height_feet < 0 or height_inches < 0) or (height_feet == 0 and height_inches == 0) and height_inches < 12:
                print("Height values must be non-negative.")
                return None
        else:
            height = float(input(f"Enter height in {height_units[height_unit_choice]}: "))
            if height <= 0:
                print("Height must be a positive number.")
                return None
        if height_unit_choice != 4:
            return weight, weight_unit_choice, height, height_unit_choice
        else:
            return weight, weight_unit_choice, (height_feet, height_inches), height_unit_choice
    except (ValueError, KeyError):
        print("Invalid input. Please enter numeric values")
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

    

def bmi_report(weight, height, weight_unit='kg', height_unit='m'):
    # Convert weight
    if weight_unit == 'lb':
        weight_kg = lb_to_kg(weight)
    elif weight_unit == 'kg':
        weight_kg = float(weight)
    else:
        return "Unsupported weight unit."

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
    category, description = bmi_category(bmi_value_rounded)

    return bmi_value_rounded, category, description



def main():
    """Main function to run the BMI calculator."""
    print("=== BMI Calculator ===\n")
    
    result = input_values()
    if result is None:
        print("\nFailed to get valid input. Please try again.")
        return
    
    weight, weight_unit_choice, height, height_unit_choice = result
    
    # Map choices to unit strings
    weight_units = {1: 'kg', 2: 'lb'}
    height_units = {1: 'm', 2: 'cm', 3: 'in', 4: 'ft_in'}
    
    bmi_result = bmi_report(weight, height, weight_units[weight_unit_choice], height_units[height_unit_choice])
    
    if isinstance(bmi_result, tuple):
        bmi, category, description = bmi_result
        print(f"\n=== Results ===")
        print(f"BMI: {bmi}")
        print(f"Category: {category}")
        print(f"Description: {description}")
    else:
        print(f"\nError: {bmi_result}")



if __name__ == "__main__":
    main()