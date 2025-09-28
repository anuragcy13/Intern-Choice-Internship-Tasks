import re

def check_phishing_email(subject, body, sender, links):
    issues = []

    # 1. Urgency keywords
    urgency_keywords = ["urgent", "immediately", "verify", "act now", "suspended", "expire"]
    if any(word.lower() in subject.lower() or word.lower() in body.lower() for word in urgency_keywords):
        issues.append("⚠️ Urgency or threat detected")

    # 2. Spelling/grammar mistakes (simple check for repeated characters or bad words)
    if re.search(r"\b(acount|suspnded|immediatly|passwrod)\b", body.lower()):
        issues.append("⚠️ Possible spelling/grammar mistakes")

    # 3. Suspicious sender
    if not sender.endswith(("@gmail.com", "@yahoo.com", "@outlook.com", "@university.edu", "@bank.com")):
        issues.append("⚠️ Suspicious sender domain")

    # 4. Suspicious links
    for link in links:
        if not re.match(r"^https://(www\.)?(trustedsite|microsoft|google|bank|university)\.com", link):
            issues.append(f"⚠️ Suspicious link found: {link}")

    # 5. Attachments (simulated check for dangerous extensions)
    dangerous_ext = [".exe", ".zip", ".scr", ".bat"]
    if any(link.lower().endswith(ext) for ext in dangerous_ext for link in links):
        issues.append("⚠️ Suspicious attachment detected")

    return issues if issues else ["✅ No major phishing signs detected"]

# ----------- Test Cases -----------
email1 = check_phishing_email(
    subject="Urgent: Verify your account now!",
    body="Your acount is suspnded immediatly. Click link to verify.",
    sender="support@bankk.com",
    links=["http://secure-bank-login.com"]
)

email2 = check_phishing_email(
    subject="Weekly Newsletter",
    body="Hello student, here are this week's campus events.",
    sender="events@university.edu",
    links=["https://www.university.com/news"]
)

print("Email 1:", email1)
print("Email 2:", email2)
