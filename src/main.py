# Give choice to run either CLI or GUI

import sys

def main():
    """Main entry point - allows user to choose between CLI and GUI."""
    print("\n" + "=" * 50)
    print("       BMI HEALTH ANALYZER")
    print("=" * 50)
    print("\nChoose your interface:")
    print("1. Command Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")
    print("3. Exit")
    
    while True:
        choice = input("\n>>> Enter your choice (1/2/3): ").strip()
        
        if choice == '1':
            print("\nLaunching CLI...")
            from bmi_cli import main as cli_main
            cli_main()
            break
            
        elif choice == '2':
            print("\nLaunching GUI...")
            from bmi_gui2 import main as gui_main
            gui_main()
            break
            
        elif choice == '3':
            print("\nGoodbye! Stay Healthy.")
            sys.exit(0)
            
        else:
            print("[!] Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting.")
        sys.exit(0)