#!/usr/bin/env python3
"""
Test Supabase database connection
"""
import os
import asyncio
import asyncpg
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    database_url = os.getenv('DATABASE_URL', '').replace('postgresql+asyncpg://', 'postgresql://')
    print(f"Testing DATABASE_URL: {database_url}")
    
    try:
        conn = await asyncpg.connect(database_url)
        print("✅ Connection successful!")
        
        # Test a simple query
        result = await conn.fetchval("SELECT 1 as test")
        print(f"✅ Query test successful: {result}")
        
        await conn.close()
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        
        # Check common issues
        if "Tenant or user not found" in str(e):
            print("🔍 Likely issues:")
            print("   - Wrong project reference in hostname")
            print("   - Incorrect password")
            print("   - Wrong region (us-east-1 vs us-west-1)")
            print("   - Database not found")
        elif "connection refused" in str(e).lower():
            print("🔍 Likely issues:")
            print("   - Wrong port (should be 5432)")
            print("   - Firewall blocking connection")
        elif "timeout" in str(e).lower():
            print("🔍 Likely issues:")
            print("   - Network connectivity")
            print("   - Database server down")

if __name__ == "__main__":
    asyncio.run(test_connection())
