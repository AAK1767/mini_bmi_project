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
            height_inches = int(input("Enter height - inches: "))
            if (height_feet < 0 or height_inches < 0) or (height_feet == 0 and height_inches == 0):
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
    Parameters:
    pounds: Weight in pounds.

    Returns:
    Weight in kilograms
    """
    kg = pounds * 0.45359237
    return round(kg, 2)



def inches_to_meters(inches):
    """
    Convert inches to meters.
    Parameters:
    inches: Height in inches.

    Returns:
    Height in meters
    """
    meters = inches * 0.0254
    return round(meters, 4)



def feet_inches_to_meters(feet, inches):
    """
    Convert feet and inches to meters.
    Parameters:
    feet: Height in feet.
    inches: Additional height in inches.

    Returns:
    Height in meters
    """

    total_inches = (feet * 12) + inches
    meters = total_inches * 0.0254
    return round(meters, 4)



def cms_to_meters(cms):
    """
    Convert centimeters to meters.
    Parameters:
    cms: Height in centimeters.

    Returns:
    Height in meters
    """

    meters = cms / 100
    return round(meters, 4)



def calculate_bmi(weight, height):
    """
    Calculate Body Mass Index (BMI) given weight and height.

    Parameters:
    weight: Weight in kilograms.
    height: Height in meters.

    Returns:
    BMI value rounded to two decimal places.
    """
    if height == 0:
        return "Height cannot be zero."

    bmi = weight / (height ** 2)
    return round(bmi, 2)



def bmi_category(bmi):
    """
    Determine BMI category based on BMI value.

    Parameters:
    bmi: The BMI value.

    Returns:
    A string representing the BMI category.
    """

    if bmi < 18.5:
        return "Underweight","Below healthy range; consider nutritional guidance."
    elif 18.5 <= bmi < 25:
        return "Normal weight","Healthy range"
    elif 25 <= bmi < 30:
        return "Overweight","Above healthy range; lifestyle adjustments may help."
    elif 30 <= bmi < 35:
        return "Obesity class I","Moderately high; medical advice is recommended."
    elif 35 <= bmi < 40:
        return "Obesity class II","High; increased health risks."
    else:
        return "Obesity class III", "Very high; medical guidance is important."
    


def bmi_report(weight, height, weight_unit='kg', height_unit='m'):
    """
    Calculate BMI with automatic unit conversion.
    
    Parameters:
    weight: Weight value
    height: Height value (single value for m, cm, inches) or tuple (feet, inches)
    weight_unit: 'kg' or 'lb'
    height_unit: 'm', 'cm', 'in', or 'ft_in'
    
    Returns:
    Tuple of (BMI value, category, description)
    """
    # Convert weight to kg
    if weight_unit == 'lb':
        weight_kg = lb_to_kg(weight)
    elif weight_unit == 'kg':
        weight_kg = weight
    else:
        return "Unsupported weight unit."

    # Convert height to meters
    if height_unit == 'm':
        height_m = height
    elif height_unit == 'cm':
        height_m = cms_to_meters(height)
    elif height_unit == 'in':
        height_m = inches_to_meters(height)
    elif height_unit == 'ft_in':
        if isinstance(height, tuple) and len(height) == 2:
            feet, inches = height
            height_m = feet_inches_to_meters(feet, inches)
        else:
            return "Height must be a tuple (feet, inches) for 'ft_in' unit."
    else:
        return "Unsupported height unit."

    # Calculate BMI
    bmi_value = calculate_bmi(weight_kg, height_m)
    if isinstance(bmi_value, str):
        return bmi_value  # Return error message if any

    # Determine BMI category
    category, description = bmi_category(bmi_value)

    return bmi_value, category, description



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