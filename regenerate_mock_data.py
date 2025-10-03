#!/usr/bin/env python3
"""
Script to regenerate mock data with updated ATM and branch information
"""

import json
from mock_data import MockDataGenerator

def main():
    print("Regenerating mock data with Mauryan Bank...")
    
    # Generate new mock data
    generator = MockDataGenerator()
    
    # Save ATM data
    with open('mock_data/atms.json', 'w') as f:
        json.dump(generator.atms, f, indent=2)
    print(f"Generated {len(generator.atms)} ATMs")
    
    # Save Branch data
    with open('mock_data/branches.json', 'w') as f:
        json.dump(generator.branches, f, indent=2)
    print(f"Generated {len(generator.branches)} branches")
    
    # Analyze ATM status distribution
    active_count = sum(1 for atm in generator.atms if atm['status'] == 'ACTIVE')
    out_of_service_count = sum(1 for atm in generator.atms if atm['status'] == 'OUT_OF_SERVICE')
    maintenance_count = sum(1 for atm in generator.atms if atm['status'] == 'MAINTENANCE')
    
    print(f"\nATM Status Distribution:")
    print(f"ACTIVE: {active_count} ({active_count/len(generator.atms)*100:.1f}%)")
    print(f"OUT_OF_SERVICE: {out_of_service_count} ({out_of_service_count/len(generator.atms)*100:.1f}%)")
    print(f"MAINTENANCE: {maintenance_count} ({maintenance_count/len(generator.atms)*100:.1f}%)")
    
    # Analyze 24x7 distribution
    yes_24x7 = sum(1 for atm in generator.atms if atm['24x7'] == 'YES')
    no_24x7 = sum(1 for atm in generator.atms if atm['24x7'] == 'NO')
    
    print(f"\n24x7 Distribution:")
    print(f"YES: {yes_24x7} ({yes_24x7/len(generator.atms)*100:.1f}%)")
    print(f"NO: {no_24x7} ({no_24x7/len(generator.atms)*100:.1f}%)")
    
    # Check all ATMs use Mauryan Bank
    mauryan_count = sum(1 for atm in generator.atms if atm['bank_name'] == 'Mauryan Bank')
    print(f"\nBank Name Check:")
    print(f"Mauryan Bank: {mauryan_count}/{len(generator.atms)}")
    
    # Check all branches use Mauryan Bank
    mauryan_branches = sum(1 for branch in generator.branches if 'Mauryan Bank' in branch['name'])
    print(f"Mauryan Bank branches: {mauryan_branches}/{len(generator.branches)}")
    
    # City distribution
    cities_atm = {}
    for atm in generator.atms:
        city = atm['city']
        cities_atm[city] = cities_atm.get(city, 0) + 1
    
    print(f"\nATM Distribution by City (top 10):")
    sorted_cities = sorted(cities_atm.items(), key=lambda x: x[1], reverse=True)
    for city, count in sorted_cities[:10]:
        print(f"{city}: {count}")
    
    print("\nMock data regeneration completed successfully!")

if __name__ == "__main__":
    main()