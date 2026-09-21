
import sys
import os
sys.path.append(os.getcwd())

# Mock the input function to automatically select the subject
original_input = input
def mock_input(prompt=""):
    if "Enter your choice:" in prompt or "choice:" in prompt.lower():
        # Find the subject in the list and return its number
        attendance_folder = "attendance"
        if os.path.exists(attendance_folder):
            subjects = sorted([d for d in os.listdir(attendance_folder) 
                             if os.path.isdir(os.path.join(attendance_folder, d))])
            if "flat" in subjects:
                return str(subjects.index("flat") + 1)
        return "1"  # Default to creating new subject
    elif "Enter new subject name:" in prompt or "subject name:" in prompt.lower():
        return "flat"
    return original_input(prompt)

# Replace input function
__builtins__['input'] = mock_input

# Import and run the main script
exec(open('main.py').read())
