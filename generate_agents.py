#!/usr/bin/env python3
"""
Dedicated script for generating human agent data with Indian names
for the BankWise AI Banking Support System.
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from faker import Faker
import os

# Initialize Faker with Indian locale
fake = Faker('en_IN')

class AgentDataGenerator:
    """Generate realistic human agent data for banking support"""
    
    def __init__(self):
        self.agents = []
        
    def generate_agents(self, count: int = 25) -> List[Dict[str, Any]]:
        """Generate a list of human agents with Indian names and details"""
        
        # Indian first names and last names for more realistic generation
        indian_first_names = [
            "Rahul", "Priya", "Amit", "Sneha", "Vikram", "Anjali", "Rohit", "Kavita",
            "Suresh", "Meena", "Arun", "Pooja", "Vijay", "Neha", "Rajesh", "Swati",
            "Manish", "Divya", "Sanjay", "Rashmi", "Alok", "Kiran", "Deepak", "Shweta",
            "Mukesh", "Anita", "Ramesh", "Geeta", "Ashok", "Rekha", "Vinod", "Sunita",
            "Prakash", "Usha", "Mahesh", "Sarita", "Dinesh", "Meera", "Naveen", "Lata",
            "Harish", "Savita", "Gopal", "Radhika", "Kamal", "Archana", "Brijesh", "Renu"
        ]
        
        indian_last_names = [
            "Sharma", "Verma", "Gupta", "Agarwal", "Jain", "Joshi", "Patel", "Shah",
            "Singh", "Kumar", "Reddy", "Nair", "Menon", "Iyer", "Pillai", "Rao",
            "Mishra", "Dubey", "Tiwari", "Tripathi", "Chaturvedi", "Pandey", "Yadav",
            "Chauhan", "Rathore", "Shekhawat", "Khandelwal", "Goenka", "Bansal",
            "Malhotra", "Khanna", "Kapoor", "Malik", "Chopra", "Bhatia", "Sethi",
            "Dutta", "Chatterjee", "Mukherjee", "Banerjee", "Sengupta", "Chakraborty"
        ]
        
        departments = [
            "Customer Service", "Card Services", "Loan Department", 
            "Account Services", "Dispute Resolution", "Technical Support",
            "Priority Banking", "NRI Services", "Business Banking", "Wealth Management"
        ]
        
        specializations = [
            "Account Queries", "Card Issues", "Loan Processing", "Transaction Disputes",
            "Technical Support", "KYC Verification", "Investment Services", 
            "International Banking", "Business Accounts", "Premium Services"
        ]
        
        languages = [
            ["English", "Hindi"], ["English", "Hindi", "Bengali"],
            ["English", "Hindi", "Tamil"], ["English", "Hindi", "Telugu"],
            ["English", "Hindi", "Marathi"], ["English", "Hindi", "Gujarati"],
            ["English", "Hindi", "Kannada"], ["English", "Hindi", "Malayalam"],
            ["English", "Hindi", "Punjabi"], ["English", "Hindi", "Urdu"]
        ]
        
        cities = [
            "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata",
            "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Chandigarh", "Indore",
            "Nagpur", "Kochi", "Coimbatore", "Bhopal", "Visakhapatnam", "Thiruvananthapuram"
        ]
        
        for i in range(count):
            agent_id = f"AGENT{random.randint(1000, 9999)}"
            first_name = random.choice(indian_first_names)
            last_name = random.choice(indian_last_names)
            full_name = f"{first_name} {last_name}"
            
            # Generate employee ID
            employee_id = f"EMP{random.randint(10000, 99999)}"
            
            # Contact information
            email = f"{first_name.lower()}.{last_name.lower()}@bankwise.com"
            phone = f"+91{random.randint(7000000000, 9999999999)}"
            
            # Professional details
            department = random.choice(departments)
            specialization = random.choice(specializations)
            languages_spoken = random.choice(languages)
            
            # Experience and performance
            years_experience = random.randint(1, 15)
            performance_rating = round(random.uniform(3.5, 5.0), 1)
            cases_handled = random.randint(500, 5000)
            satisfaction_rate = round(random.uniform(85, 98), 1)
            
            # Availability and schedule
            shift_start = random.choice(["06:00", "08:00", "10:00", "14:00", "16:00"])
            shift_end = self._calculate_shift_end(shift_start)
            working_days = random.choice(["Mon-Fri", "Mon-Sat", "Tue-Sun", "Wed-Sun"])
            
            # Location
            base_city = random.choice(cities)
            work_mode = random.choice(["Office", "Hybrid", "Remote"])
            
            # Status and availability
            current_status = random.choice(["Available", "Busy", "On Break", "In Training", "Off Duty"])
            is_available = current_status == "Available"
            
            # Skills and certifications
            skills = self._generate_skills(specialization)
            certifications = self._generate_certifications()
            
            agent = {
                "agent_id": agent_id,
                "employee_id": employee_id,
                "first_name": first_name,
                "last_name": last_name,
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "department": department,
                "specialization": specialization,
                "languages_spoken": languages_spoken,
                "years_experience": years_experience,
                "performance_rating": performance_rating,
                "cases_handled": cases_handled,
                "customer_satisfaction_rate": satisfaction_rate,
                "shift_start": shift_start,
                "shift_end": shift_end,
                "working_days": working_days,
                "base_city": base_city,
                "work_mode": work_mode,
                "current_status": current_status,
                "is_available": is_available,
                "skills": skills,
                "certifications": certifications,
                "join_date": (datetime.now() - timedelta(days=years_experience * 365)).isoformat(),
                "last_training_date": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat(),
                "next_available_time": self._calculate_next_available_time(current_status, shift_start, shift_end),
                "average_response_time": random.randint(30, 120),  # seconds
                "resolution_rate": round(random.uniform(85, 99), 1),  # percentage
                "escalation_level": random.choice(["L1", "L2", "L3"]),
                "team_lead": f"AGENT{random.randint(1000, 9999)}" if random.random() > 0.7 else None
            }
            
            self.agents.append(agent)
        
        return self.agents
    
    def _calculate_shift_end(self, shift_start: str) -> str:
        """Calculate shift end time based on start time"""
        start_hour, start_min = map(int, shift_start.split(':'))
        # Shift duration of 8-9 hours
        shift_hours = random.randint(8, 9)
        end_hour = (start_hour + shift_hours) % 24
        
        if end_hour == 0:
            end_hour = 12
        elif end_hour > 12:
            end_hour = end_hour - 12
        
        return f"{end_hour:02d}:{start_min:02d}"
    
    def _calculate_next_available_time(self, current_status: str, shift_start: str, shift_end: str) -> Optional[str]:
        """Calculate when the agent will be next available"""
        if current_status == "Available":
            return None
        
        now = datetime.now()
        
        if current_status == "Busy":
            # Available in 15-60 minutes
            next_available = now + timedelta(minutes=random.randint(15, 60))
        elif current_status == "On Break":
            # Available in 10-30 minutes
            next_available = now + timedelta(minutes=random.randint(10, 30))
        elif current_status == "In Training":
            # Available in 1-4 hours
            next_available = now + timedelta(hours=random.randint(1, 4))
        else:  # Off Duty
            # Available next shift
            next_available = now + timedelta(hours=random.randint(8, 24))
        
        return next_available.isoformat()
    
    def _generate_skills(self, specialization: str) -> List[str]:
        """Generate relevant skills based on specialization"""
        all_skills = {
            "Account Queries": ["Account Management", "Balance Inquiries", "Statement Generation", "Account Opening"],
            "Card Issues": ["Card Blocking", "Card Replacement", "Dispute Resolution", "Fraud Detection"],
            "Loan Processing": ["Loan Applications", "Documentation", "Eligibility Assessment", "Interest Calculations"],
            "Transaction Disputes": ["Investigation", "Chargeback Processing", "Merchant Disputes", "Fraud Analysis"],
            "Technical Support": ["Online Banking", "Mobile App", "API Integration", "Troubleshooting"],
            "KYC Verification": ["Document Verification", "Compliance", "Risk Assessment", "Regulatory Requirements"],
            "Investment Services": ["Financial Planning", "Investment Products", "Risk Analysis", "Market Research"],
            "International Banking": ["Forex Services", "NRI Banking", "International Transfers", "Trade Finance"],
            "Business Accounts": ["Corporate Banking", "Business Loans", "Cash Management", "Trade Services"],
            "Premium Services": ["Wealth Management", "Priority Banking", "Personalized Service", "High Value Transactions"]
        }
        
        base_skills = ["Customer Service", "Communication", "Problem Solving", "Time Management"]
        specialized_skills = all_skills.get(specialization, ["General Banking"])
        
        return base_skills + random.sample(specialized_skills, min(3, len(specialized_skills)))
    
    def _generate_certifications(self) -> List[str]:
        """Generate professional certifications"""
        all_certifications = [
            "Certified Banking Professional (CBP)",
            "Financial Services Certified Professional (FSCP)",
            "Certified Customer Service Professional (CCSP)",
            "Anti-Money Laundering Certified (AML)",
            "KYC Compliance Certified",
            "Digital Banking Certified",
            "Risk Management Certified",
            "Financial Planning Certified",
            "ITIL Foundation",
            "Six Sigma Green Belt",
            "PMP Certification",
            "Agile Certified Practitioner"
        ]
        
        # Each agent has 1-3 certifications
        num_certs = random.randint(1, 3)
        return random.sample(all_certifications, num_certs)
    
    def save_agents_to_json(self, filename: str = "mock_data/agents.json") -> None:
        """Save generated agents to JSON file"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.agents, f, indent=2, ensure_ascii=False)
        
        print(f"Generated {len(self.agents)} agents and saved to {filename}")
    
    def get_available_agents(self, specialization: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of currently available agents, optionally filtered by specialization"""
        available_agents = [agent for agent in self.agents if agent["is_available"]]
        
        if specialization:
            available_agents = [
                agent for agent in available_agents 
                if agent["specialization"] == specialization
            ]
        
        # Sort by performance rating and customer satisfaction
        available_agents.sort(
            key=lambda x: (x["performance_rating"], x["customer_satisfaction_rate"]), 
            reverse=True
        )
        
        return available_agents
    
    def get_agent_by_id(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent details by ID"""
        for agent in self.agents:
            if agent["agent_id"] == agent_id:
                return agent
        return None
    
    def update_agent_status(self, agent_id: str, new_status: str) -> bool:
        """Update agent availability status"""
        for agent in self.agents:
            if agent["agent_id"] == agent_id:
                agent["current_status"] = new_status
                agent["is_available"] = new_status == "Available"
                agent["next_available_time"] = self._calculate_next_available_time(
                    new_status, agent["shift_start"], agent["shift_end"]
                )
                return True
        return False


def main():
    """Main function to generate and save agent data"""
    print("Generating human agent data for BankWise AI Banking Support System...")
    
    generator = AgentDataGenerator()
    agents = generator.generate_agents(count=25)
    
    # Save to JSON file
    generator.save_agents_to_json()
    
    # Display some statistics
    print(f"\nGenerated {len(agents)} agents with the following distribution:")
    
    dept_count = {}
    for agent in agents:
        dept = agent["department"]
        dept_count[dept] = dept_count.get(dept, 0) + 1
    
    print("\nDepartment Distribution:")
    for dept, count in dept_count.items():
        print(f"  {dept}: {count} agents")
    
    available_count = len([a for a in agents if a["is_available"]])
    print(f"\nCurrently Available: {available_count}/{len(agents)} agents")
    
    # Show sample agent
    print(f"\nSample Agent Profile:")
    sample_agent = agents[0]
    for key, value in sample_agent.items():
        if key not in ["skills", "certifications"]:
            print(f"  {key}: {value}")
    print(f"  skills: {', '.join(sample_agent['skills'])}")
    print(f"  certifications: {', '.join(sample_agent['certifications'])}")


if __name__ == "__main__":
    main()