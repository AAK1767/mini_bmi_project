'''
This module provides utility functions for loading and saving user profile data.
'''


import json
import os
from datetime import datetime

PROFILE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_profiles.json")


def load_profiles():
    """Load all saved user profiles."""
    if not os.path.exists(PROFILE_FILE):
        return []
    with open(PROFILE_FILE, "r") as f:
        return json.load(f)


def save_profile(profile):
    """
    Save a single user profile to the JSON file.
    profile should be a dict with any fields you decide.
    """
    profiles = load_profiles()
    profile["saved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    profiles.append(profile)

    with open(PROFILE_FILE, "w") as f:
        json.dump(profiles, f, indent=4)