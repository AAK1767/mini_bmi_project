'''
This module provides visualization functions for BMI-related data.
'''


import matplotlib.pyplot as plt

def plot_bmi_comparison(user_bmi: float):
    """
    Plot a simple bar graph comparing the user's BMI with
    approximate global/region average BMI values.
    Values used are static reference estimates (not real-time data).
    """

    # Sample reference values (approximate global averages)
    labels = ["You", "World Avg", "Asia Avg", "Europe Avg"]
    bmi_values = [
        user_bmi,
        24.5,   # Global average BMI (approx WHO estimate)
        23.0,   # Asia-Pacific typical average
        26.5    # Europe typical average
    ]

    # Create bar chart
    plt.figure(figsize=(7, 5))
    bars = plt.bar(labels, bmi_values)

    # Highlight user's bar
    bars[0].set_color('orange')

    # Labeling
    plt.title("BMI Comparison with World Averages")
    plt.xlabel("Category")
    plt.ylabel("BMI Value")

    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.1f}",
            ha='center',
            va='bottom'
        )

    plt.tight_layout()
    plt.show()



def plot_bmi_distribution():
    """
    A simple pie chart showing global BMI category distribution (approx values).
    """
    categories = ["Underweight", "Normal", "Overweight", "Obese"]
    values = [8, 45, 30, 17]  # Approx WHO estimates

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Approx Global BMI Category Distribution")
    plt.show()



def plot_weight_vs_ideal(user_weight_kg: float, height_m: float):
    """
    Show user's weight vs ideal weight range (derived from BMI healthy range).
    """
    bmi_min, bmi_max = 18.5, 24.9
    w_min = bmi_min * (height_m ** 2)
    w_max = bmi_max * (height_m ** 2)

    labels = ["Your Weight", "Min Healthy", "Max Healthy"]
    values = [user_weight_kg, w_min, w_max]

    plt.figure(figsize=(7, 5))
    bars = plt.bar(labels, values)

    bars[0].set_color("orange")

    for bar in bars:
        ht = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, ht, f"{ht:.1f}", ha='center', va='bottom')

    plt.ylabel("Weight (kg)")
    plt.title("Your Weight vs Healthy Weight Range")

    plt.show()



def plot_bmi_range(user_bmi: float):
    """
    Plot user's BMI against the healthy range using a horizontal band.
    """

    plt.figure(figsize=(8, 2.5))
    
    # Healthy range band - convert BMI values to axis fraction (xlim is 10-40, so range is 30)
    xmin_frac = (18.5 - 10) / (40 - 10)  # = 8.5/30
    xmax_frac = (24.9 - 10) / (40 - 10)  # = 14.9/30
    plt.axhspan(0, 1, xmin=xmin_frac, xmax=xmax_frac, color='lightgreen', alpha=0.6)

    # Vertical line for user's BMI
    plt.axvline(user_bmi, color='red', linewidth=3)
    
    plt.xlim(10, 40)
    plt.yticks([])
    plt.xlabel("BMI Value")
    plt.title("Your BMI Compared to Healthy Range (18.5 - 24.9)")

    plt.text(user_bmi, 0.5, f"{user_bmi:.1f}", fontsize=12, ha='center', va='center')

    plt.tight_layout()
    plt.show()

# Example usage:
if __name__ == "__main__":
    sample_weight = float(input("Enter your weight in kg for visualization: "))
    sample_height = float(input("Enter your height in meters for visualization: "))
    sample_bmi = sample_weight / (sample_height ** 2)
    choices = {
        '1': plot_bmi_comparison,
        '2': plot_bmi_distribution,
        '3': plot_weight_vs_ideal,
        '4': plot_bmi_range
    }
    print("Choose a visualization to display:")
    print("1. BMI Comparison with World Averages")
    print("2. Global BMI Category Distribution")
    print("3. Your Weight vs Healthy Weight Range")
    print("4. Your BMI Compared to Healthy Range")
    print("5. Exit")
    choice = ''
    while choice != '5':
        choice = input("Enter choice (1-5): ").strip()
        if choice in choices:
            if choice == '1':
                choices[choice](sample_bmi)
            elif choice == '2':
                choices[choice]()
            elif choice == '3':
                choices[choice](sample_weight, sample_height)
            elif choice == '4':
                choices[choice](sample_bmi)