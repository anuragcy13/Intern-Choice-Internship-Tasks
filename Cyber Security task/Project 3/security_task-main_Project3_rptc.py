import os
import random

# ------------------------------
# Simulated Cybersecurity Threats
# ------------------------------

def ransomware_simulation(files):
    """Simulate ransomware by 'encrypting' filenames."""
    encrypted_files = [f"{file}.locked" for file in files]
    return encrypted_files, "⚠️ Files have been encrypted! Pay ransom to unlock."

def spyware_simulation(user_activity):
    """Simulate spyware stealing user data."""
    stolen_data = random.choice(user_activity)
    return stolen_data, "⚠️ Spyware detected! Data stolen."

def social_engineering_simulation(email_text):
    """Detect phishing/social engineering attempts in messages."""
    suspicious_keywords = ["urgent", "verify", "password", "click here", "prize", "lottery"]
    if any(word in email_text.lower() for word in suspicious_keywords):
        return "⚠️ Social Engineering attempt detected!"
    return "✅ No suspicious activity."

# ------------------------------
# Demo Usage
# ------------------------------
# Fake "files"
files = ["report.docx", "grades.xlsx", "photo.jpg"]

# Fake user activity logs
activity = ["Visited bank.com", "Typed password: MySecret123", "Opened suspicious email"]

# Fake phishing email
phishing_email = "Urgent! Your password will expire. Click here to verify now!"

# Run simulations
encrypted, ransomware_msg = ransomware_simulation(files)
stolen, spyware_msg = spyware_simulation(activity)
social_msg = social_engineering_simulation(phishing_email)

# Output
print("=== RANSOMWARE ===")
print("Original files:", files)
print("Encrypted files:", encrypted)
print(ransomware_msg)

print("\n=== SPYWARE ===")
print("User activity log:", activity)
print("Stolen data:", stolen)
print(spyware_msg)

print("\n=== SOCIAL ENGINEERING ===")
print("Email:", phishing_email)
print(social_msg)
