import sys

# Import functions from your existing modules
from bmi_core import input_values, bmi_report, save_profile, cms_to_meters, inches_to_meters, feet_inches_to_meters, lb_to_kg
from data_utils import load_profiles
from visualize import plot_bmi_comparison, plot_weight_vs_ideal, plot_bmi_range, plot_bmi_distribution

# Import suggestions
from suggestions import generate_suggestions as get_static_suggestions, health_facts_of_the_day as get_static_fact
# Import AI functions
from chatbot_ai import generate_bmi_suggestions, generate_bmi_faq_answer, generate_health_fact_of_the_day, is_ai_available, get_premade_faq_list, get_premade_faq_answer

def print_separator():
    print("\n" + "-" * 50 + "\n")


def view_history():
    """Displays saved user profiles in a simple table."""
    profiles = load_profiles()
    if not profiles:
        print("\n[!] No history found.")
        return

    print(f"\n{'Name':<15} {'Date':<20} {'BMI':<10} {'Category'}")
    print("-" * 60)
    for p in profiles[-10:]:  # Show last 10 entries
        date_str = p.get('saved_at', 'N/A')[:19] 
        print(f"{p.get('name', 'User'):<15} {date_str:<20} {p['bmi']:<10} {p['category']}")
    print("-" * 60)


def display_static_suggestions(bmi, category):
    """Helper function to print static suggestions (used for standard choice AND fallback)."""
    data = get_static_suggestions(bmi, category)
    print_separator()
    print(f"*** HEALTH FACTS FOR {category.upper()} (Standard) ***")
    for fact in data['health_facts']:
        print(f"- {fact}")
    
    print(f"\n*** EXERCISE PLAN ***")
    for ex in data['exercise_plan']:
        print(f"- {ex}")
        
    print(f"\n*** DIET TIPS ***")
    for tip in data['diet']:
        print(f"- {tip}")
        
    if data['warnings']:
        print(f"\n*** WARNINGS ***")
        for w in data['warnings']:
            print(f"[!] {w}")


def handle_suggestions(bmi, category, age, sex):
    """Handles the sub-menu for AI vs Static suggestions with Fallback."""
    print("\n[?] How would you like to get suggestions?")
    print("1. Standard (Instant, Rule-based)")
    print("2. AI Powered")
    
    choice = input(">>> Choice (1/2): ").strip()

    if choice == '1':
        display_static_suggestions(bmi, category)

    elif choice == '2':
        print("\n... Contacting AI (this may take a moment) ...")
        try:
            # Attempt AI generation
            ai_result = generate_bmi_suggestions(bmi, category, age, sex)
            
            # Check if API returned an error key instead of data
            if "error" in ai_result:
                raise ValueError(ai_result["error"])

            # Pretty print the JSON result
            print_separator()
            print("--- AI SUMMARY ---")
            print(ai_result.get("summary", "No summary provided."))
            
            recs = ai_result.get("recommendations", {})
            
            print("\n--- AI EXERCISES ---")
            for ex in recs.get("exercises", []):
                print(f"• {ex}")

            print("\n--- AI NUTRITION ---")
            for nut in recs.get("nutrition", []):
                print(f"• {nut}")
            
            print("\n--- LIFESTYLE ---")
            for life in recs.get("lifestyle", []):
                print(f"• {life}")
                
            if ai_result.get("caution"):
                print(f"\n[!] CAUTION: {ai_result['caution']}")

        except Exception as e:
            # FALLBACK LOGIC
            print(f"\n[!] AI Connection Failed: {e}")
            print("[*] Automatically switching to Standard Suggestions...\n")
            display_static_suggestions(bmi, category)
    else:
        print("[!] Invalid choice.")


def show_premade_faq_menu():
    """Display premade FAQ questions and let user choose."""
    print("\n=== PREMADE FAQ QUESTIONS ===")
    print("Select a question number to see the answer:\n")
    
    faq_list = get_premade_faq_list()
    for idx, question in faq_list:
        print(f"  {idx}. {question}")
    
    print(f"\n  0. Back to menu")
    
    while True:
        try:
            choice = input("\n>>> Enter question number: ").strip()
            if choice == '0' or choice.lower() in ['back', 'exit', 'quit']:
                return
            
            choice_num = int(choice)
            answer = get_premade_faq_answer(choice_num)
            
            if answer:
                print(f"\n{answer}")
                print("\n(Pre-written answer)")
                print("-" * 50)
            else:
                print("[!] Invalid question number. Please try again.")
        except ValueError:
            print("[!] Please enter a valid number.")


def handle_faq_chat():
    """Interactive loop for AI FAQ with premade fallback."""
    print_separator()
    print("=== HEALTH FAQ ===")

    # Check if AI is available
    if not is_ai_available():
        print("\n⚠️  AI features are unavailable.")
        print("Your API key may be missing, invalid, or not set.")
        print("To enable AI-powered answers, add a valid GEMINI_API_KEY to your src/.env file.\n")
        print("You can still browse premade FAQ questions!")
        show_premade_faq_menu()
        return

    print("Ask questions like:")
    print("- What is the difference between BMI and BMR?")
    print("- Is BMI accurate for athletes?")
    print("- How does age affect BMI?")
    print("- Any health/diet/fitness related questions")
    print("---Note that responses are generated by AI and may not be perfect and can contain errors.---")
    print("\n(Type 'exit' or 'back' to return, 'premade' for premade questions)")
    
    while True:
        question = input("\nAsk AI: ").strip()
        if question.lower() in ['exit', 'back', 'quit']:
            break
        
        if question.lower() == 'premade':
            show_premade_faq_menu()
            continue
        
        if not question:
            continue

        print("... Thinking ...")
        try:
            result = generate_bmi_faq_answer(question)
            
            if isinstance(result, dict):
                if result.get("ai_available"):
                    answer = result.get("answer", "No answer received.")
                    print(f"\n>> AI Answer:\n{answer}")
                else:
                    # AI unavailable
                    print("\n⚠️  AI is unavailable. Showing premade questions instead...")
                    show_premade_faq_menu()
                    break
            else:
                print(f"\n>> AI Answer:\n{result}")
                
        except Exception as e:
            print(f"\n[!] AI Error: {e}")
            print("[*] Switching to premade FAQ questions...\n")
            show_premade_faq_menu()
            break


def main():
    print("\n==========================================")
    print("       BMI HEALTH ANALYZER (CLI)          ")
    print("==========================================")

    # --- START UP: Health Fact of the Day ---
    print("\nLoading Health Fact of the Day...")
    try:
        fact = generate_health_fact_of_the_day()
        print(f"★ {fact}")
    except Exception:
        fact = get_static_fact()
        print(f"★ {fact}")
    print("==========================================\n")

    while True:
        print("=== MAIN MENU ===")
        print("1. Start BMI Calculator")
        print("2. General Health FAQ (AI Chat)")
        print("3. Exit")
        
        start_choice = input(">>> Select Option: ").strip()

        if start_choice == '2':
            handle_faq_chat()
            # After chat, loop continues (shows Main Menu again)
        elif start_choice == '3':
            print("Goodbye! Stay Healthy.")
            sys.exit()
        elif start_choice == '1':
            break # Break this loop to enter the Calculator App
        else:
            print("Invalid option.")

    while True:
        # --- STEP 1: INPUT ---
        print_separator()
        print("--- NEW CALCULATION ---")
        user_input = input_values()
        
        if user_input is None:
            retry = input("Input failed. Try again? (y/n): ")
            if retry.lower() == 'y':
                continue
            else:
                print("Goodbye!")
                sys.exit()

        name, weight, weight_unit_choice, height, height_unit_choice, age, sex = user_input
        
        # Map choices
        weight_units_map = {1: 'kg', 2: 'lb'}
        height_units_map = {1: 'm', 2: 'cm', 3: 'in', 4: 'ft_in'}
        w_unit_str = weight_units_map[weight_unit_choice]
        h_unit_str = height_units_map[height_unit_choice]

        # --- STEP 2: REPORT GENERATION ---
        report = bmi_report(weight, height, age, sex, w_unit_str, h_unit_str)

        if isinstance(report, str):
            print(f"\nError calculating BMI: {report}")
            continue

        # Unpack Report
        bmi, category, desc, bmr, healthy_rng, water, gain, lose = report

        # --- STEP 3: DISPLAY RESULTS ---
        print_separator()
        print(f"RESULT FOR: {name}")
        print(f"BMI:        {bmi}")
        print(f"Category:   {category}")
        print(f"BMR:        {bmr} kcal/day")
        print(f"Water:      {water} Liters/day")
        print(f"Target Wgt: {healthy_rng[0]} - {healthy_rng[1]} kg")
        
        if gain > 0: print(f"To Reach Healthy: Gain ~{gain} kg")
        if lose > 0: print(f"To Reach Healthy: Lose ~{lose} kg")

        # Save Profile
        profile_data = {
            "name": name, "age": age, "sex": sex,
            "weight": weight, "height": height,
            "bmi": bmi, "category": category,
            "bmr": bmr
        }
        save_profile(profile_data)
        print("\n(Result saved to history)")
        print_separator()

        while True:
            print(f"\n--- ACTIONS FOR {name.upper()} ---")
            print("1. Get Suggestions (Diet/Exercise)")
            print("2. Ask AI FAQ")
            print("3. Show Graphs")
            print("4. View History")
            print("5. Recalculate (New User)")
            print("6. Exit App")

            menu_choice = input("Select Option: ").strip()

            if menu_choice == '1':
                handle_suggestions(bmi, category, age, sex)
            
            elif menu_choice == '2':
                handle_faq_chat()

            elif menu_choice == '3':
                print("\n[Graphs]")
                print("a. Compare with World Averages")
                print("b. Weight vs Healthy Range")
                print("c. BMI Position")
                print("d. Global BMI Distribution")
                g_choice = input("Choose graph (a/b/c/d): ").strip().lower()
                try:
                    if g_choice == 'a':
                        plot_bmi_comparison(bmi)
                    elif g_choice == 'b':
                        # Convert to Metric for Visualize functions
                        h_m = 0
                        if h_unit_str == 'm': h_m = height
                        elif h_unit_str == 'cm': h_m = cms_to_meters(height)
                        elif h_unit_str == 'in': h_m = inches_to_meters(height)
                        elif h_unit_str == 'ft_in': h_m = feet_inches_to_meters(height[0], height[1])
                        
                        w_kg = weight if w_unit_str == 'kg' else lb_to_kg(weight)
                        plot_weight_vs_ideal(w_kg, h_m)
                    elif g_choice == 'c':
                        plot_bmi_range(bmi)
                    elif g_choice == 'd':
                        plot_bmi_distribution()
                    else:
                        print("Invalid graph choice.")
                except Exception as e:
                    print(f"Graph error: {e}")

            elif menu_choice == '4':
                view_history()

            elif menu_choice == '5':
                print("\nRestarting Calculator...")
                break 

            elif menu_choice == '6':
                print("Goodbye! Stay Healthy.")
                sys.exit()
            
            else:
                print("Invalid option.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting.")
        sys.exit()