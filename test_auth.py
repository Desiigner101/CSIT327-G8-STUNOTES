# test_auth.py
# Save this file in your project root (same level as manage.py)
# Run with: python manage.py shell < test_auth.py

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stunotesapp.settings')
django.setup()

from django.contrib.auth import authenticate
from notes.models import User
import hashlib

print("="*60)
print("STUNOTES AUTHENTICATION TEST")
print("="*60)

# Test 1: Database Connection
print("\n1. TESTING DATABASE CONNECTION...")
try:
    user_count = User.objects.count()
    print(f"✅ Database connected. Total users: {user_count}")
except Exception as e:
    print(f"❌ Database error: {e}")
    exit()

# Test 2: Check if users exist
print("\n2. CHECKING EXISTING USERS...")
users = User.objects.all()[:5]  # Show first 5 users
if users:
    print("✅ Users found in database:")
    for user in users:
        print(f"   - Username: {user.username}")
        print(f"   - Email: {user.email}")
        print(f"   - Password hash: {user.password[:20]}...")
        print(f"   - Is active: {user.is_active}")
        print(f"   - Is superuser: {user.is_superuser}")
        print("   " + "-"*30)
else:
    print("❌ No users found in database")

# Test 3: Create test user
print("\n3. CREATING TEST USER...")
test_username = "testuser123"
test_password = "testpass123"

# Delete if exists
if User.objects.filter(username=test_username).exists():
    User.objects.filter(username=test_username).delete()
    print(f"🗑️  Deleted existing user: {test_username}")

try:
    test_user = User.objects.create_user(
        username=test_username,
        password=test_password,
        email="test@example.com"
    )
    print(f"✅ Test user created successfully")
    print(f"   - Username: {test_user.username}")
    print(f"   - Password hash: {test_user.password[:30]}...")
    print(f"   - Is active: {test_user.is_active}")
except Exception as e:
    print(f"❌ Error creating test user: {e}")
    exit()

# Test 4: Test password verification
print("\n4. TESTING PASSWORD VERIFICATION...")
password_check = test_user.check_password(test_password)
print(f"Password check result: {password_check}")
if password_check:
    print("✅ Password verification works")
else:
    print("❌ Password verification failed")

# Test 5: Test Django authentication
print("\n5. TESTING DJANGO AUTHENTICATION...")
auth_user = authenticate(username=test_username, password=test_password)
if auth_user:
    print("✅ Django authentication works")
    print(f"   - Authenticated user: {auth_user.username}")
    print(f"   - Same user object: {auth_user == test_user}")
else:
    print("❌ Django authentication failed")

# Test 6: Test wrong password
print("\n6. TESTING WRONG PASSWORD...")
wrong_auth = authenticate(username=test_username, password="wrongpassword")
if wrong_auth is None:
    print("✅ Wrong password correctly rejected")
else:
    print("❌ Wrong password was accepted (SECURITY ISSUE)")

# Test 7: Test your existing users
print("\n7. TESTING YOUR EXISTING USERS...")
print("Enter a username you created through your register form:")
print("(or press Enter to skip)")

# For shell testing, we'll test the first non-superuser
regular_users = User.objects.filter(is_superuser=False).exclude(username=test_username)
if regular_users:
    existing_user = regular_users.first()
    print(f"Testing existing user: {existing_user.username}")
    print(f"Password hash: {existing_user.password[:30]}...")
    print(f"Is active: {existing_user.is_active}")
    
    # You'll need to manually test with the actual password
    print(f"To test authentication with this user:")
    print(f"authenticate(username='{existing_user.username}', password='YOUR_ACTUAL_PASSWORD')")
else:
    print("No regular users found to test")

# Test 8: Check AUTH_USER_MODEL setting
print("\n8. CHECKING AUTH_USER_MODEL SETTING...")
from django.conf import settings
auth_user_model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
print(f"AUTH_USER_MODEL: {auth_user_model}")
if auth_user_model == 'notes.User':
    print("✅ AUTH_USER_MODEL correctly set to custom User model")
else:
    print("❌ AUTH_USER_MODEL not set to custom User model")

# Test 9: Check for property conflicts
print("\n9. CHECKING FOR PROPERTY CONFLICTS...")
test_user_fresh = User.objects.get(username=test_username)
print(f"has is_admin field: {hasattr(test_user_fresh, 'is_admin')}")
print(f"is_admin value: {getattr(test_user_fresh, 'is_admin', 'Not found')}")

# Check if is_admin is a property or field
is_admin_descriptor = User.__dict__.get('is_admin')
if isinstance(is_admin_descriptor, property):
    print("⚠️  WARNING: is_admin is a property (might cause conflicts)")
else:
    print("✅ is_admin is a regular field")

# Final Summary
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)

print("\n✅ TESTS THAT SHOULD PASS:")
print("- Database connection")
print("- Test user creation")
print("- Password verification")
print("- Django authentication")
print("- Wrong password rejection")

print("\n❌ IF ANY OF THESE FAIL, THERE'S A PROBLEM:")
print("- Django authentication should return User object")
print("- Password verification should return True")
print("- AUTH_USER_MODEL should be 'notes.User'")

print(f"\n🧪 TEST USER CREATED:")
print(f"Username: {test_username}")
print(f"Password: {test_password}")
print("You can now test login with these credentials in your web form")

print("\n" + "="*60)
print("Run this test and check the results above!")
print("="*60)