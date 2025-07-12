#!/usr/bin/env python3
"""
Generate password hash for admin user
"""
import bcrypt
import getpass

def generate_password_hash(password: str) -> str:
    """Generate bcrypt hash for password"""
    salt = bcrypt.gensalt(rounds=12)
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hash.decode('utf-8')

def main():
    print("🔐 Password Hash Generator for LawVriksh Admin")
    
    # Get password from user
    password = getpass.getpass("Enter password for admin user: ")
    
    if not password:
        print("❌ Password cannot be empty!")
        return
    
    # Generate hash
    password_hash = generate_password_hash(password)
    
    print(f"\n✅ Password hash generated:")
    print(f"Password: {password}")
    print(f"Hash: {password_hash}")
    
    print(f"\n📝 SQL to insert admin user:")
    print(f"""
INSERT INTO admin_users (username, email, password_hash, is_superuser, is_active) 
VALUES (
    'admin', 
    'admin@lawvriksh.com', 
    '{password_hash}',
    TRUE,
    TRUE
);
""")

if __name__ == "__main__":
    main()