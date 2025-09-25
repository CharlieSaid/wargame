#!/usr/bin/env python3
"""
Cleanup script to remove empty squads from the database.
This script finds and deletes squads that have no units.
"""

import sys
from db_utils import execute_sql

def find_empty_squads():
    """Find all squads that have no units"""
    query = """
    SELECT s.id, s.name, s.commander, s.level, s.created_at
    FROM squads s
    LEFT JOIN units u ON s.id = u.squad_id
    WHERE u.squad_id IS NULL
    ORDER BY s.created_at DESC
    """
    return execute_sql(query, fetch_all=True)

def delete_empty_squads():
    """Delete all squads that have no units"""
    query = """
    DELETE FROM squads 
    WHERE id NOT IN (SELECT DISTINCT squad_id FROM units WHERE squad_id IS NOT NULL)
    """
    result = execute_sql(query)
    return result

def main():
    print("🔍 Checking for empty squads...")
    
    # Find empty squads
    empty_squads = find_empty_squads()
    
    if not empty_squads:
        print("✅ No empty squads found!")
        return
    
    print(f"❌ Found {len(empty_squads)} empty squads:")
    for squad in empty_squads:
        print(f"  - Squad ID {squad['id']}: {squad['name']} (Level {squad['level']}, Created: {squad['created_at']})")
    
    # Ask for confirmation
    response = input(f"\n🗑️  Delete all {len(empty_squads)} empty squads? (y/N): ")
    if response.lower() != 'y':
        print("❌ Cancelled.")
        return
    
    # Delete empty squads
    print("🗑️  Deleting empty squads...")
    deleted_count = delete_empty_squads()
    print(f"✅ Deleted {deleted_count} empty squads!")
    
    # Verify cleanup
    remaining_empty = find_empty_squads()
    if not remaining_empty:
        print("✅ All empty squads have been removed!")
    else:
        print(f"⚠️  {len(remaining_empty)} empty squads still remain.")

if __name__ == "__main__":
    main()
