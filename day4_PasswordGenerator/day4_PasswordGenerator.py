import random
import string
import secrets
import json
from datetime import datetime

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
    def generate_password(self, length=12, uppercase=True, lowercase=True, 
                         digits=True, special=True, no_ambiguous=False):
        if length < 4:
            raise ValueError("Password must be at least 4 characters")
        
        chars = ""
        required = []
        
        if lowercase:
            chars += self.lowercase if not no_ambiguous else self.lowercase.replace('l', '')
            required.append(secrets.choice(chars[-len(self.lowercase):]))
        
        if uppercase:
            chars += self.uppercase if not no_ambiguous else self.uppercase.replace('O', '')
            required.append(secrets.choice(self.uppercase.replace('O', '') if no_ambiguous else self.uppercase))
        
        if digits:
            digit_set = self.digits if not no_ambiguous else self.digits.replace('0', '').replace('1', '')
            chars += digit_set
            required.append(secrets.choice(digit_set))
        
        if special:
            chars += self.special_chars
            required.append(secrets.choice(self.special_chars))
        
        if not chars:
            raise ValueError("Select at least one character type")
        
        password = required[:]
        for _ in range(length - len(required)):
            password.append(secrets.choice(chars))
        
        secrets.SystemRandom().shuffle(password)
        return ''.join(password)
    
    def generate_batch(self, count=5, **kwargs):
        return [self.generate_password(**kwargs) for _ in range(count)]
    
    def check_strength(self, password):
        score = 0
        tips = []
        
        if len(password) >= 12:
            score += 25
        elif len(password) >= 8:
            score += 15
            tips.append("Use 12+ characters")
        else:
            tips.append("Too short (min 8 chars)")
        
        if any(c.islower() for c in password):
            score += 15
        else:
            tips.append("Add lowercase letters")
        
        if any(c.isupper() for c in password):
            score += 15
        else:
            tips.append("Add uppercase letters")
        
        if any(c.isdigit() for c in password):
            score += 15
        else:
            tips.append("Add numbers")
        
        if any(c in self.special_chars for c in password):
            score += 20
        else:
            tips.append("Add special characters")
        
        if len(set(password)) == len(password):
            score += 10
        else:
            tips.append("Avoid repeated characters")
        
        strength_levels = [(90, "Very Strong"), (70, "Strong"), (50, "Medium"), (30, "Weak")]
        strength = next((level for threshold, level in strength_levels if score >= threshold), "Very Weak")
        
        return {"score": score, "strength": strength, "tips": tips}
    
    def save_to_file(self, passwords, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"passwords_{timestamp}.json"
        
        data = {
            "created": datetime.now().isoformat(),
            "passwords": passwords,
            "count": len(passwords)
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return filename

def get_int_input(prompt, default):
    try:
        return int(input(prompt) or str(default))
    except ValueError:
        return default

def get_yes_no(prompt, default=True):
    response = input(prompt).strip().lower()
    if not response:
        return default
    return response in ['y', 'yes']

def main():
    gen = PasswordGenerator()
    
    print("🔐 Password Generator")
    print("-" * 30)
    
    while True:
        print("\n1. Generate password")
        print("2. Generate multiple passwords")
        print("3. Check password strength")
        print("4. Generate and save to file")
        print("5. Exit")
        
        choice = input("\nChoice (1-5): ").strip()
        
        if choice == '1':
            length = get_int_input("Length (12): ", 12)
            uppercase = get_yes_no("Uppercase? (Y/n): ")
            lowercase = get_yes_no("Lowercase? (Y/n): ")
            digits = get_yes_no("Digits? (Y/n): ")
            special = get_yes_no("Special chars? (Y/n): ")
            no_ambiguous = get_yes_no("Exclude ambiguous chars? (y/N): ", False)
            
            try:
                password = gen.generate_password(
                    length=length, uppercase=uppercase, lowercase=lowercase,
                    digits=digits, special=special, no_ambiguous=no_ambiguous
                )
                
                strength = gen.check_strength(password)
                print(f"\nPassword: {password}")
                print(f"Strength: {strength['strength']} ({strength['score']}/100)")
                
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            count = get_int_input("How many? (5): ", 5)
            length = get_int_input("Length (12): ", 12)
            
            passwords = gen.generate_batch(count=count, length=length)
            print(f"\nGenerated {count} passwords:")
            
            for i, pwd in enumerate(passwords, 1):
                strength = gen.check_strength(pwd)['strength']
                print(f"{i:2}. {pwd} - {strength}")
        
        elif choice == '3':
            password = input("Enter password: ").strip()
            if password:
                analysis = gen.check_strength(password)
                print(f"\nStrength: {analysis['strength']} ({analysis['score']}/100)")
                if analysis['tips']:
                    print("Tips:")
                    for tip in analysis['tips']:
                        print(f"  • {tip}")
        
        elif choice == '4':
            count = get_int_input("How many passwords? (10): ", 10)
            length = get_int_input("Length (12): ", 12)
            
            passwords = gen.generate_batch(count=count, length=length)
            filename = gen.save_to_file(passwords)
            print(f"Saved {count} passwords to {filename}")
        
        elif choice == '5':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()