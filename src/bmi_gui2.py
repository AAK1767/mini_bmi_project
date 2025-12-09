import wx
import os
import threading

# Import functions from existing modules
from bmi_core import (
    bmi_report, save_profile, cms_to_meters, 
    inches_to_meters, feet_inches_to_meters, lb_to_kg
)
from data_utils import load_profiles
from visualize import plot_bmi_comparison, plot_weight_vs_ideal, plot_bmi_range, plot_bmi_distribution
from suggestions import (
    generate_suggestions as get_static_suggestions,
    health_facts_of_the_day as get_static_fact
)
from chatbot_ai import (
    generate_bmi_suggestions, 
    generate_bmi_faq_answer, 
    generate_health_fact_of_the_day,
    is_ai_available
)


class BMICalculatorApp(wx.Frame):
    """Main application window for BMI Health Analyzer."""
    
    def __init__(self):
        super().__init__(parent=None, title="BMI Health Analyzer", size=(800, 700))
        
        # Store current calculation results
        self.current_result = None
        self.current_input = None
        
        # Create main panel with simple background color
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.Colour(230, 240, 250))
        
        # Create notebook for tabs
        self.notebook = wx.Notebook(self.panel)
        self.notebook.SetBackgroundColour(wx.Colour(245, 248, 252))
        
        # Create tabs with semi-transparent backgrounds
        self.calculator_tab = CalculatorTab(self.notebook, self)
        self.suggestions_tab = SuggestionsTab(self.notebook, self)
        self.faq_tab = FAQTab(self.notebook, self)
        self.history_tab = HistoryTab(self.notebook, self)
        self.graphs_tab = GraphsTab(self.notebook, self)
        
        # Set tab background colors for visual consistency with background
        tab_bg_color = wx.Colour(245, 248, 252, 240)  # Light, slightly transparent
        self.calculator_tab.SetBackgroundColour(tab_bg_color)
        self.suggestions_tab.SetBackgroundColour(tab_bg_color)
        self.faq_tab.SetBackgroundColour(tab_bg_color)
        self.history_tab.SetBackgroundColour(tab_bg_color)
        self.graphs_tab.SetBackgroundColour(tab_bg_color)
        
        # Add tabs to notebook
        self.notebook.AddPage(self.calculator_tab, "Calculator")
        self.notebook.AddPage(self.suggestions_tab, "Suggestions")
        self.notebook.AddPage(self.faq_tab, "AI FAQ")
        self.notebook.AddPage(self.history_tab, "History")
        self.notebook.AddPage(self.graphs_tab, "Graphs")
        
        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Health Fact of the Day at top with styled background
        fact_panel = wx.Panel(self.panel)
        fact_panel.SetBackgroundColour(wx.Colour(255, 255, 255, 200))
        fact_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fact_text = wx.StaticText(fact_panel, label="Loading Health Fact...")
        self.fact_text.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        self.fact_text.SetForegroundColour(wx.Colour(50, 50, 100))
        fact_sizer.Add(self.fact_text, 1, wx.ALL | wx.EXPAND, 5)
        fact_panel.SetSizer(fact_sizer)
        
        sizer.Add(fact_panel, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(self.notebook, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        self.panel.SetSizer(sizer)
        
        # Load health fact in background
        self.load_health_fact()
        
        # Center and show
        self.Centre()
        self.Show()
    
    def load_health_fact(self):
        """Load health fact of the day (try AI first, fallback to static)."""
        def fetch_fact():
            try:
                fact = generate_health_fact_of_the_day()
            except Exception:
                fact = get_static_fact()
            wx.CallAfter(self.fact_text.SetLabel, f"★ {fact}")
        
        thread = threading.Thread(target=fetch_fact, daemon=True)
        thread.start()
    
    def set_result(self, result, user_input):
        """Store calculation result and enable other tabs."""
        self.current_result = result
        self.current_input = user_input
        
        # Enable suggestions and graphs tabs
        self.suggestions_tab.enable_controls(True)
        self.graphs_tab.enable_controls(True)


class CalculatorTab(wx.Panel):
    """Tab for BMI calculation input and results."""
    
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.setup_ui()
    
    def setup_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title
        title = wx.StaticText(self, label="BMI Calculator")
        title.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        # Input section
        input_box = wx.StaticBox(self, label="Enter Your Details")
        input_sizer = wx.StaticBoxSizer(input_box, wx.VERTICAL)
        grid = wx.FlexGridSizer(rows=7, cols=2, hgap=10, vgap=10)
        
        # Name
        grid.Add(wx.StaticText(self, label="Name:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.name_input = wx.TextCtrl(self)
        grid.Add(self.name_input, 1, wx.EXPAND)
        
        # Weight
        grid.Add(wx.StaticText(self, label="Weight:"), 0, wx.ALIGN_CENTER_VERTICAL)
        weight_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.weight_input = wx.TextCtrl(self, size=(100, -1))
        self.weight_unit = wx.Choice(self, choices=["kg", "lb"])
        self.weight_unit.SetSelection(0)
        weight_sizer.Add(self.weight_input, 1, wx.EXPAND)
        weight_sizer.Add(self.weight_unit, 0, wx.LEFT, 5)
        grid.Add(weight_sizer, 1, wx.EXPAND)
        
        # Height
        grid.Add(wx.StaticText(self, label="Height:"), 0, wx.ALIGN_CENTER_VERTICAL)
        height_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.height_input = wx.TextCtrl(self, size=(60, -1))
        self.height_input2 = wx.TextCtrl(self, size=(60, -1))  # For feet/inches
        self.height_input2.Hide()
        self.height_label2 = wx.StaticText(self, label="in:")
        self.height_label2.Hide()
        self.height_unit = wx.Choice(self, choices=["m", "cm", "in", "ft/in"])
        self.height_unit.SetSelection(0)
        self.height_unit.Bind(wx.EVT_CHOICE, self.on_height_unit_change)
        height_sizer.Add(self.height_input, 1, wx.EXPAND)
        height_sizer.Add(self.height_label2, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        height_sizer.Add(self.height_input2, 0, wx.LEFT, 5)
        height_sizer.Add(self.height_unit, 0, wx.LEFT, 5)
        grid.Add(height_sizer, 1, wx.EXPAND)
        
        # Age
        grid.Add(wx.StaticText(self, label="Age:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.age_input = wx.SpinCtrl(self, min=1, max=120, initial=25)
        grid.Add(self.age_input, 1, wx.EXPAND)
        
        # Sex
        grid.Add(wx.StaticText(self, label="Sex:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.sex_input = wx.Choice(self, choices=["male", "female"])
        self.sex_input.SetSelection(0)
        grid.Add(self.sex_input, 1, wx.EXPAND)
        
        grid.AddGrowableCol(1, 1)
        input_sizer.Add(grid, 1, wx.EXPAND | wx.ALL, 10)
        
        # Calculate button
        self.calc_btn = wx.Button(self, label="Calculate BMI")
        self.calc_btn.Bind(wx.EVT_BUTTON, self.on_calculate)
        input_sizer.Add(self.calc_btn, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        main_sizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Results section
        result_box = wx.StaticBox(self, label="Results")
        result_sizer = wx.StaticBoxSizer(result_box, wx.VERTICAL)
        
        self.result_text = wx.TextCtrl(
            self, 
            style=wx.TE_MULTILINE | wx.TE_READONLY,
            size=(-1, 200)
        )
        self.result_text.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        result_sizer.Add(self.result_text, 1, wx.EXPAND | wx.ALL, 10)
        
        main_sizer.Add(result_sizer, 1, wx.EXPAND | wx.ALL, 10)
        
        self.SetSizer(main_sizer)
    
    def on_height_unit_change(self, event):
        """Show/hide second height input for feet/inches."""
        if self.height_unit.GetStringSelection() == "ft/in":
            self.height_label2.Show()
            self.height_input2.Show()
            self.height_input.SetHint("ft")
            self.height_input2.SetHint("in")
        else:
            self.height_label2.Hide()
            self.height_input2.Hide()
            self.height_input.SetHint("")
        self.Layout()
    
    def on_calculate(self, event):
        """Handle BMI calculation."""
        try:
            # Get inputs
            name = self.name_input.GetValue().strip() or "User"
            weight = float(self.weight_input.GetValue())
            age = self.age_input.GetValue()
            sex = self.sex_input.GetStringSelection()
            
            # Weight unit
            w_unit = self.weight_unit.GetStringSelection()
            
            # Height unit and value
            h_unit_str = self.height_unit.GetStringSelection()
            
            if h_unit_str == "ft/in":
                feet = int(self.height_input.GetValue())
                inches = float(self.height_input2.GetValue())
                height = (feet, inches)
                h_unit = "ft_in"
            else:
                height = float(self.height_input.GetValue())
                h_unit = h_unit_str
            
            # Calculate BMI
            report = bmi_report(weight, height, age, sex, w_unit, h_unit)
            
            if isinstance(report, str):
                wx.MessageBox(f"Error: {report}", "Calculation Error", wx.OK | wx.ICON_ERROR)
                return
            
            # Unpack results
            bmi, category, desc, bmr, healthy_rng, water, gain, lose = report
            
            # Display results
            result = f"RESULTS FOR: {name}\n"
            result += "=" * 40 + "\n\n"
            result += f"BMI:           {bmi}\n"
            result += f"Category:      {category}\n"
            result += f"Description:   {desc}\n\n"
            result += f"BMR:           {bmr} kcal/day\n"
            result += f"Water Intake:  {water} Liters/day\n"
            result += f"Healthy Range: {healthy_rng[0]} - {healthy_rng[1]} kg\n\n"
            
            if gain > 0:
                result += f"To Reach Healthy: Gain ~{gain} kg\n"
            if lose > 0:
                result += f"To Reach Healthy: Lose ~{lose} kg\n"
            
            result += "\n(Result saved to history)"
            
            self.result_text.SetValue(result)
            
            # Save profile
            profile_data = {
                "name": name, "age": age, "sex": sex,
                "weight": weight, "height": height,
                "bmi": bmi, "category": category, "bmr": bmr
            }
            save_profile(profile_data)
            
            # Store result in main frame
            user_input = {
                "name": name, "weight": weight, "height": height,
                "age": age, "sex": sex, "w_unit": w_unit, "h_unit": h_unit
            }
            self.main_frame.set_result(report, user_input)
            
            # Refresh history tab
            self.main_frame.history_tab.refresh_history()
            
        except ValueError as e:
            wx.MessageBox(f"Invalid input: {e}", "Input Error", wx.OK | wx.ICON_ERROR)


class SuggestionsTab(wx.Panel):
    """Tab for health suggestions (Standard and AI-powered)."""
    
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.setup_ui()
    
    def setup_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title
        title = wx.StaticText(self, label="Health Suggestions")
        title.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        # Info text
        self.info_label = wx.StaticText(self, label="Calculate BMI first to get personalized suggestions.")
        main_sizer.Add(self.info_label, 0, wx.ALL, 10)
        
        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.standard_btn = wx.Button(self, label="Standard Suggestions")
        self.standard_btn.Bind(wx.EVT_BUTTON, self.on_standard)
        self.ai_btn = wx.Button(self, label="AI-Powered Suggestions")
        self.ai_btn.Bind(wx.EVT_BUTTON, self.on_ai)
        
        btn_sizer.Add(self.standard_btn, 0, wx.ALL, 5)
        btn_sizer.Add(self.ai_btn, 0, wx.ALL, 5)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER)
        
        # Results area
        self.suggestions_text = wx.TextCtrl(
            self,
            style=wx.TE_MULTILINE | wx.TE_READONLY,
            size=(-1, 400)
        )
        self.suggestions_text.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        main_sizer.Add(self.suggestions_text, 1, wx.EXPAND | wx.ALL, 10)
        
        self.SetSizer(main_sizer)
        self.enable_controls(False)
    
    def enable_controls(self, enabled):
        """Enable or disable suggestion buttons."""
        self.standard_btn.Enable(enabled)
        self.ai_btn.Enable(enabled)
        if enabled:
            self.info_label.SetLabel("Click a button to get suggestions based on your BMI.")
        else:
            self.info_label.SetLabel("Calculate BMI first to get personalized suggestions.")
    
    def on_standard(self, event):
        """Display standard rule-based suggestions."""
        if not self.main_frame.current_result:
            return
        
        bmi, category, *_ = self.main_frame.current_result
        data = get_static_suggestions(bmi, category)
        
        text = f"=== STANDARD SUGGESTIONS FOR {category.upper()} ===\n\n"
        
        text += "*** HEALTH FACTS ***\n"
        for fact in data['health_facts']:
            text += f"• {fact}\n"
        
        text += "\n*** EXERCISE PLAN ***\n"
        for ex in data['exercise_plan']:
            text += f"• {ex}\n"
        
        text += "\n*** DIET TIPS ***\n"
        for tip in data['diet']:
            text += f"• {tip}\n"
        
        if data['warnings']:
            text += "\n*** WARNINGS ***\n"
            for w in data['warnings']:
                text += f"⚠ {w}\n"
        
        self.suggestions_text.SetValue(text)
    
    def on_ai(self, event):
        """Get AI-powered suggestions."""
        if not self.main_frame.current_result:
            return
        
        bmi, category, *_ = self.main_frame.current_result
        age = self.main_frame.current_input['age']
        sex = self.main_frame.current_input['sex']
        
        self.suggestions_text.SetValue("Contacting AI... Please wait...")
        self.ai_btn.Disable()
        
        def fetch_ai():
            try:
                ai_result = generate_bmi_suggestions(bmi, category, age, sex)
                
                if "error" in ai_result:
                    raise ValueError(ai_result["error"])
                
                text = "=== AI-POWERED SUGGESTIONS ===\n\n"
                text += "--- SUMMARY ---\n"
                text += ai_result.get("summary", "No summary provided.") + "\n\n"
                
                recs = ai_result.get("recommendations", {})
                
                text += "--- EXERCISES ---\n"
                for ex in recs.get("exercises", []):
                    text += f"• {ex}\n"
                
                text += "\n--- NUTRITION ---\n"
                for nut in recs.get("nutrition", []):
                    text += f"• {nut}\n"
                
                text += "\n--- LIFESTYLE ---\n"
                for life in recs.get("lifestyle", []):
                    text += f"• {life}\n"
                
                if ai_result.get("caution"):
                    text += f"\n⚠ CAUTION: {ai_result['caution']}\n"
                
                wx.CallAfter(self.suggestions_text.SetValue, text)
                
            except Exception as e:
                # Fallback to standard
                wx.CallAfter(self.show_fallback, str(e))
            
            wx.CallAfter(self.ai_btn.Enable)
        
        thread = threading.Thread(target=fetch_ai, daemon=True)
        thread.start()
    
    def show_fallback(self, error):
        """Show standard suggestions as fallback when AI fails."""
        bmi, category, *_ = self.main_frame.current_result
        data = get_static_suggestions(bmi, category)
        
        text = f"⚠ AI Connection Failed: {error}\n"
        text += "Showing Standard Suggestions instead...\n\n"
        text += "=" * 40 + "\n\n"
        
        text += "*** HEALTH FACTS ***\n"
        for fact in data['health_facts']:
            text += f"• {fact}\n"
        
        text += "\n*** EXERCISE PLAN ***\n"
        for ex in data['exercise_plan']:
            text += f"• {ex}\n"
        
        text += "\n*** DIET TIPS ***\n"
        for tip in data['diet']:
            text += f"• {tip}\n"
        
        self.suggestions_text.SetValue(text)


class FAQTab(wx.Panel):
    """Tab for AI-powered FAQ chat."""
    
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.setup_ui()
    
    def setup_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title
        title = wx.StaticText(self, label="AI Health FAQ")
        title.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        # Info
        info = wx.StaticText(self, label="Ask questions about BMI, diet, exercise, health, and more!")
        main_sizer.Add(info, 0, wx.ALL, 5)
        
        # Example questions
        examples = wx.StaticText(self, label="Examples: 'Is pasta healthy?', 'Health tips for BMI 36?', 'What is BMR?', 'How does age affect BMI?'")
        examples.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        main_sizer.Add(examples, 0, wx.ALL, 5)
        
        # Chat history
        self.chat_history = wx.TextCtrl(
            self,
            style=wx.TE_MULTILINE | wx.TE_READONLY,
            size=(-1, 350)
        )
        self.chat_history.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        main_sizer.Add(self.chat_history, 1, wx.EXPAND | wx.ALL, 10)
        
        # Input area
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.question_input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.question_input.Bind(wx.EVT_TEXT_ENTER, self.on_ask)
        self.ask_btn = wx.Button(self, label="Ask")
        self.ask_btn.Bind(wx.EVT_BUTTON, self.on_ask)
        
        input_sizer.Add(self.question_input, 1, wx.EXPAND | wx.RIGHT, 5)
        input_sizer.Add(self.ask_btn, 0)
        main_sizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Disclaimer
        disclaimer = wx.StaticText(self, label="Note: AI responses are for informational purposes only and may contain errors.")
        disclaimer.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        main_sizer.Add(disclaimer, 0, wx.ALL, 5)
        
        self.SetSizer(main_sizer)

        # Check if AI is available and show warning
        if not is_ai_available():
            self.chat_history.SetValue(
                "⚠️ WARNING: API Key not found or invalid.\n"
                "Please set GEMINI_API_KEY in your src/.env file to use AI features.\n\n"
                "AI FAQ is currently unavailable.\n" +
                "-" * 50
            )
            self.ask_btn.Disable()
            self.question_input.Disable()
    
    def on_ask(self, event):
        """Handle FAQ question."""
        question = self.question_input.GetValue().strip()
        if not question:
            return
        
        # Add question to chat
        self.chat_history.AppendText(f"\nYou: {question}\n")
        self.question_input.Clear()
        self.ask_btn.Disable()
        
        def fetch_answer():
            try:
                answer = generate_bmi_faq_answer(question)
                wx.CallAfter(self.chat_history.AppendText, f"\nAI: {answer}\n")
                wx.CallAfter(self.chat_history.AppendText, "-" * 50 + "\n")
            except Exception as e:
                wx.CallAfter(self.chat_history.AppendText, f"\n[Error]: {e}\n")
            
            wx.CallAfter(self.ask_btn.Enable)
        
        thread = threading.Thread(target=fetch_answer, daemon=True)
        thread.start()


class HistoryTab(wx.Panel):
    """Tab for viewing saved BMI history."""
    
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.setup_ui()
        self.refresh_history()
    
    def setup_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title
        title = wx.StaticText(self, label="BMI History")
        title.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        # Refresh button
        self.refresh_btn = wx.Button(self, label="Refresh")
        self.refresh_btn.Bind(wx.EVT_BUTTON, lambda e: self.refresh_history())
        main_sizer.Add(self.refresh_btn, 0, wx.ALL, 5)
        
        # History list
        self.history_list = wx.ListCtrl(
            self,
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL
        )
        self.history_list.InsertColumn(0, "Name", width=100)
        self.history_list.InsertColumn(1, "Date", width=150)
        self.history_list.InsertColumn(2, "BMI", width=80)
        self.history_list.InsertColumn(3, "Category", width=150)
        self.history_list.InsertColumn(4, "Age", width=50)
        self.history_list.InsertColumn(5, "Sex", width=70)
        
        main_sizer.Add(self.history_list, 1, wx.EXPAND | wx.ALL, 10)
        
        self.SetSizer(main_sizer)
    
    def refresh_history(self):
        """Reload and display history from file."""
        self.history_list.DeleteAllItems()
        profiles = load_profiles()
        
        # Show last 20 entries (most recent first)
        for p in reversed(profiles[-20:]):
            index = self.history_list.InsertItem(self.history_list.GetItemCount(), p.get('name', 'User'))
            date_str = p.get('saved_at', 'N/A')[:19]
            self.history_list.SetItem(index, 1, date_str)
            self.history_list.SetItem(index, 2, str(p.get('bmi', 'N/A')))
            self.history_list.SetItem(index, 3, p.get('category', 'N/A'))
            self.history_list.SetItem(index, 4, str(p.get('age', 'N/A')))
            self.history_list.SetItem(index, 5, p.get('sex', 'N/A'))


class GraphsTab(wx.Panel):
    """Tab for BMI visualization graphs."""
    
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.setup_ui()
    
    def setup_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title
        title = wx.StaticText(self, label="BMI Visualizations")
        title.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        # Info
        self.info_label = wx.StaticText(self, label="Calculate BMI first to view graphs.")
        main_sizer.Add(self.info_label, 0, wx.ALL, 10)
        
        # Graph buttons
        btn_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.compare_btn = wx.Button(self, label="Compare with World Averages", size=(250, 40))
        self.compare_btn.Bind(wx.EVT_BUTTON, self.on_compare)
        btn_sizer.Add(self.compare_btn, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        self.weight_btn = wx.Button(self, label="Weight vs Healthy Range", size=(250, 40))
        self.weight_btn.Bind(wx.EVT_BUTTON, self.on_weight_vs_ideal)
        btn_sizer.Add(self.weight_btn, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        self.position_btn = wx.Button(self, label="BMI Position on Scale", size=(250, 40))
        self.position_btn.Bind(wx.EVT_BUTTON, self.on_bmi_position)
        btn_sizer.Add(self.position_btn, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        self.distribution_btn = wx.Button(self, label="BMI Distribution Chart", size=(250, 40))
        self.distribution_btn.Bind(wx.EVT_BUTTON, self.on_bmi_distribution)
        btn_sizer.Add(self.distribution_btn, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        main_sizer.Add(btn_sizer, 1, wx.ALIGN_CENTER)
        
        self.SetSizer(main_sizer)
        self.enable_controls(False)
    
    def enable_controls(self, enabled):
        """Enable or disable graph buttons."""
        self.compare_btn.Enable(enabled)
        self.weight_btn.Enable(enabled)
        self.position_btn.Enable(enabled)
        self.distribution_btn.Enable(enabled)
        if enabled:
            self.info_label.SetLabel("Click a button to view the graph.")
        else:
            self.info_label.SetLabel("Calculate BMI first to view graphs.")
    
    def on_compare(self, event):
        """Show BMI comparison with world averages."""
        if self.main_frame.current_result:
            bmi = self.main_frame.current_result[0]
            try:
                plot_bmi_comparison(bmi)
            except Exception as e:
                wx.MessageBox(f"Graph error: {e}", "Error", wx.OK | wx.ICON_ERROR)
    
    def on_weight_vs_ideal(self, event):
        """Show weight vs healthy range graph."""
        if self.main_frame.current_result and self.main_frame.current_input:
            inp = self.main_frame.current_input
            height = inp['height']
            h_unit = inp['h_unit']
            weight = inp['weight']
            w_unit = inp['w_unit']
            
            # Convert to metric
            if h_unit == 'm':
                h_m = height
            elif h_unit == 'cm':
                h_m = cms_to_meters(height)
            elif h_unit == 'in':
                h_m = inches_to_meters(height)
            elif h_unit == 'ft_in':
                h_m = feet_inches_to_meters(height[0], height[1])
            else:
                h_m = height
            
            w_kg = weight if w_unit == 'kg' else lb_to_kg(weight)
            
            try:
                plot_weight_vs_ideal(w_kg, h_m)
            except Exception as e:
                wx.MessageBox(f"Graph error: {e}", "Error", wx.OK | wx.ICON_ERROR)
    
    def on_bmi_position(self, event):
        """Show BMI position on scale."""
        if self.main_frame.current_result:
            bmi = self.main_frame.current_result[0]
            try:
                plot_bmi_range(bmi)
            except Exception as e:
                wx.MessageBox(f"Graph error: {e}", "Error", wx.OK | wx.ICON_ERROR)
    
    def on_bmi_distribution(self, event):
        """Show BMI distribution chart."""
        if self.main_frame.current_result:
            bmi = self.main_frame.current_result[0]
            try:
                plot_bmi_distribution()
            except Exception as e:
                wx.MessageBox(f"Graph error: {e}", "Error", wx.OK | wx.ICON_ERROR)


def main():
    """Main entry point for the GUI application."""
    app = wx.App()
    frame = BMICalculatorApp()
    app.MainLoop()


if __name__ == "__main__":
    main()