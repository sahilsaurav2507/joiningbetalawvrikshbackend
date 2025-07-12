#!/usr/bin/env python3
"""
LawVriksh Backend API - Comprehensive Test Suite
"""
import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        # Test basic imports
        from app.config import get_settings, Settings
        from app.database import engine, SessionLocal
        from app.models import User, Creator, AdminUser
        from app.schemas import UserCreate, CreatorCreate
        
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("Testing configuration...")
    try:
        from app.config import get_settings
        
        settings = get_settings()
        
        # Test required fields
        assert settings.DATABASE_URL, "DATABASE_URL is required"
        assert settings.SECRET_KEY, "SECRET_KEY is required"
        assert settings.DATABASE_NAME, "DATABASE_NAME is required"
        
        # Test CORS origins parsing
        cors_origins = settings.cors_origins_list
        assert isinstance(cors_origins, list), "CORS origins should be a list"
        assert len(cors_origins) > 0, "At least one CORS origin should be configured"
        
        print(f"✅ Configuration loaded successfully")
        print(f"   - Database: {settings.DATABASE_NAME}")
        print(f"   - Environment: {settings.ENVIRONMENT}")
        print(f"   - CORS Origins: {len(cors_origins)} configured")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_database_connection():
    """Test database connectivity"""
    print("Testing database connection...")
    try:
        from app.database import engine, SessionLocal
        from sqlalchemy import text
        
        # Test engine connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            assert test_value == 1, "Database query failed"
        
        # Test session creation
        db = SessionLocal()
        try:
            # Test a simple query
            result = db.execute(text("SELECT DATABASE() as current_db"))
            current_db = result.fetchone()[0]
            print(f"✅ Database connection successful")
            print(f"   - Connected to: {current_db}")
            return True
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   Make sure your database is running and .env file is configured.")
        return False

def test_schema_validation():
    """Test Pydantic schema validation"""
    print("Testing schema validation...")
    try:
        from app.schemas import UserCreate, CreatorCreate, UserResponse
        
        # Test UserCreate schema
        user_data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "phone": "+91-9876543210",
            "profession": "Lawyer",
            "city": "Mumbai",
            "state": "Maharashtra"
        }
        user_create = UserCreate(**user_data)
        assert user_create.full_name == "Test User"
        assert user_create.email == "test@example.com"
        
        # Test CreatorCreate schema
        creator_data = {
            "full_name": "Test Creator",
            "email": "creator@example.com",
            "phone": "+91-9876543211",
            "content_type": "Video Content",
            "experience_level": "Intermediate"
        }
        creator_create = CreatorCreate(**creator_data)
        assert creator_create.full_name == "Test Creator"
        assert creator_create.content_type == "Video Content"
        
        print("✅ Schema validation successful")
        return True
        
    except Exception as e:
        print(f"❌ Schema validation test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("Testing API endpoints...")
    try:
        from fastapi.testclient import TestClient
        from app.main import app
        
        client = TestClient(app)
        
        # Test health check
        response = client.get("/health")
        assert response.status_code == 200
        health_data = response.json()
        assert health_data["status"] == "healthy"
        
        # Test root endpoint
        response = client.get("/")
        assert response.status_code == 200
        
        print("✅ API endpoints test successful")
        return True
        
    except Exception as e:
        print(f"❌ API endpoints test failed: {e}")
        return False

def cleanup_test_files():
    """Clean up unnecessary test files"""
    print("🧹 Cleaning up unnecessary files...")
    
    files_to_remove = [
        "database_setup.log",
        "test.db",
        "*.pyc",
        "__pycache__",
        ".pytest_cache",
        "sql/test_*.sql"
    ]
    
    import glob
    import shutil
    
    removed_count = 0
    
    for pattern in files_to_remove:
        if pattern == "__pycache__":
            # Remove __pycache__ directories
            for root, dirs, files in os.walk("."):
                for dir_name in dirs:
                    if dir_name == "__pycache__":
                        dir_path = os.path.join(root, dir_name)
                        try:
                            shutil.rmtree(dir_path)
                            removed_count += 1
                            print(f"   Removed: {dir_path}")
                        except:
                            pass
        else:
            # Remove files matching pattern
            for file_path in glob.glob(pattern, recursive=True):
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        removed_count += 1
                        print(f"   Removed: {file_path}")
                except:
                    pass
    
    print(f"✅ Cleanup completed - {removed_count} items removed")

def main():
    """Run all tests"""
    print("🚀 LawVriksh Backend API - Test Suite")
    print("=" * 50)
    
    # List of test functions
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Database Connection", test_database_connection),
        ("Schema Validation", test_schema_validation),
        ("API Endpoints", test_api_endpoints),
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    # Run tests
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
        print()  # Add spacing between tests
    
    # Clean up files
    cleanup_test_files()
    
    # Print results
    print("=" * 50)
    print(f"📊 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Your application is ready to run.")
        print("\n🚀 Next steps:")
        print("   1. Run: python -m uvicorn app.main:app --reload")
        print("   2. Visit: http://localhost:8000")
        print("   3. API docs: http://localhost:8000/docs")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
