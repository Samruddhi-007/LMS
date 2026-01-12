"""
Database Diagnostic Tool
Check if data is actually being saved to the database
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL not found in .env file")
    exit(1)

print("=" * 60)
print("🔍 Database Diagnostic Tool")
print("=" * 60)

try:
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Test connection
    with engine.connect() as conn:
        print("\n✅ Database connection successful!")
        
        # Check if organizations table exists
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'organizations'
            );
        """))
        
        table_exists = result.scalar()
        
        if table_exists:
            print("✅ 'organizations' table exists")
            
            # Count organizations
            result = conn.execute(text("SELECT COUNT(*) FROM organizations"))
            count = result.scalar()
            
            print(f"\n📊 Total organizations in database: {count}")
            
            if count > 0:
                # Show recent organizations
                result = conn.execute(text("""
                    SELECT id, lab_name, lab_city, lab_state, status, created_at 
                    FROM organizations 
                    ORDER BY created_at DESC 
                    LIMIT 5
                """))
                
                print("\n📋 Recent organizations:")
                print("-" * 60)
                for row in result:
                    print(f"  ID: {row[0]}")
                    print(f"  Name: {row[1]}")
                    print(f"  City: {row[2]}, State: {row[3]}")
                    print(f"  Status: {row[4]}")
                    print(f"  Created: {row[5]}")
                    print("-" * 60)
            else:
                print("\n⚠️  No organizations found in database")
                print("   This means data is NOT being saved!")
                print("\n💡 Possible issues:")
                print("   1. Frontend is not calling the API")
                print("   2. API is returning errors")
                print("   3. CORS is blocking requests")
        else:
            print("❌ 'organizations' table does NOT exist")
            print("   Run the backend server to create tables automatically")
            
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nMake sure:")
    print("  1. DATABASE_URL in .env is correct")
    print("  2. Database is accessible")
    print("  3. Backend has been started at least once")

print("\n" + "=" * 60)
