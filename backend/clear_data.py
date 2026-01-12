"""
Clear Database and Upload Folder
Resets the system for fresh testing
"""
import os
import shutil
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
UPLOAD_DIR = "./uploads"

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL not found in .env file")
    exit(1)

print("=" * 60)
print("🧹 Clear Database and Upload Folder")
print("=" * 60)

# Confirm action
print("\n⚠️  WARNING: This will:")
print("   1. Delete ALL organizations from the database")
print("   2. Delete ALL uploaded files")
print("   3. Clear localStorage organizationId")
print()
response = input("Are you sure you want to continue? (yes/no): ")

if response.lower() != 'yes':
    print("\n❌ Operation cancelled")
    exit(0)

try:
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Clear database
    print("\n🗑️  Clearing database...")
    with engine.connect() as conn:
        # Delete in reverse order of dependencies
        tables = [
            'quality_procedures',
            'quality_formats',
            'sops',
            'quality_manuals',
            'other_lab_details',
            'accreditation_documents',
            'infrastructure_details',
            'policy_documents',
            'compliance_documents',
            'shift_timings',
            'working_schedules',
            'bank_details',
            'parent_organizations',
            'top_management',
            'registered_offices',
            'organizations'
        ]
        
        for table in tables:
            try:
                result = conn.execute(text(f"DELETE FROM {table}"))
                conn.commit()
                print(f"   ✅ Cleared {table}")
            except Exception as e:
                print(f"   ⚠️  {table}: {str(e)}")
    
    # Clear upload folder
    print("\n🗑️  Clearing upload folder...")
    if os.path.exists(UPLOAD_DIR):
        for item in os.listdir(UPLOAD_DIR):
            item_path = os.path.join(UPLOAD_DIR, item)
            try:
                if os.path.isfile(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                print(f"   ✅ Deleted {item}")
            except Exception as e:
                print(f"   ⚠️  Error deleting {item}: {e}")
        
        # Recreate subdirectories
        os.makedirs(os.path.join(UPLOAD_DIR, "logos"), exist_ok=True)
        os.makedirs(os.path.join(UPLOAD_DIR, "documents"), exist_ok=True)
        print("   ✅ Recreated upload directories")
    else:
        print("   ℹ️  Upload folder doesn't exist")
    
    print("\n" + "=" * 60)
    print("✅ Database and upload folder cleared successfully!")
    print("=" * 60)
    print("\n💡 Next steps:")
    print("   1. Clear browser localStorage (F12 → Application → Local Storage → Clear)")
    print("   2. Refresh your React app")
    print("   3. Start fresh testing!")
    print()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nMake sure:")
    print("  1. DATABASE_URL in .env is correct")
    print("  2. Database is accessible")
    print("  3. Backend is not running (stop it first)")

print("=" * 60)
