"""
Create Test Pet Data - Populate database with sample veterinary data

This creates realistic test data for a veterinary clinic:
- Various pets (dogs, cats, birds, etc.)
- Different owners
- Vaccination records
- Treatment history
"""

from datetime import date, timedelta, datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.patient import Patient
from app.models.vaccine import Vaccine
from app.models.treatment import Treatment
import random

def create_test_pets():
    """Create sample pet patients"""
    db = SessionLocal()
    
    try:
        print("\nCreating test pet data...")
        print("="*60)
        
        # Test data for pets
        pets_data = [
            # Dogs
            {
                "pet_name": "Max", "species": "dog", "breed": "Golden Retriever",
                "color": "Golden", "gender": "male", "weight": 30.5,
                "date_of_birth": date(2020, 3, 15),
                "chip_number": "982000123456789",
                "owner_first_name": "John", "owner_last_name": "Smith",
                "owner_email": "john.smith@email.com", "owner_phone": "5551234567",
                "owner_address": "123 Main St, City, State 12345",
                "medical_history": "Healthy, no known issues",
                "allergies": "None known"
            },
            {
                "pet_name": "Luna", "species": "dog", "breed": "Labrador",
                "color": "Black", "gender": "female", "weight": 28.0,
                "date_of_birth": date(2019, 7, 22),
                "chip_number": "982000234567890",
                "owner_first_name": "Sarah", "owner_last_name": "Johnson",
                "owner_email": "sarah.j@email.com", "owner_phone": "5552345678",
                "owner_address": "456 Oak Ave, City, State 12345",
                "medical_history": "Previous hip dysplasia, managed with medication",
                "allergies": "Chicken"
            },
            {
                "pet_name": "Charlie", "species": "dog", "breed": "Beagle",
                "color": "Tri-color", "gender": "male", "weight": 12.5,
                "date_of_birth": date(2021, 1, 10),
                "chip_number": "982000345678901",
                "owner_first_name": "Mike", "owner_last_name": "Brown",
                "owner_email": "mike.brown@email.com", "owner_phone": "5553456789",
                "owner_address": "789 Pine Rd, City, State 12345",
                "medical_history": "Healthy, active",
                "allergies": "None"
            },
            
            # Cats
            {
                "pet_name": "Whiskers", "species": "cat", "breed": "Persian",
                "color": "White", "gender": "male", "weight": 5.2,
                "date_of_birth": date(2018, 5, 3),
                "chip_number": "982000456789012",
                "owner_first_name": "Emily", "owner_last_name": "Davis",
                "owner_email": "emily.d@email.com", "owner_phone": "5554567890",
                "owner_address": "321 Elm St, City, State 12345",
                "medical_history": "Indoor cat, regular grooming needed",
                "allergies": "None"
            },
            {
                "pet_name": "Mittens", "species": "cat", "breed": "Siamese",
                "color": "Cream and brown", "gender": "female", "weight": 4.1,
                "date_of_birth": date(2020, 11, 18),
                "chip_number": "982000567890123",
                "owner_first_name": "David", "owner_last_name": "Wilson",
                "owner_email": "d.wilson@email.com", "owner_phone": "5555678901",
                "owner_address": "654 Maple Dr, City, State 12345",
                "medical_history": "Healthy, very vocal",
                "allergies": "None"
            },
            {
                "pet_name": "Shadow", "species": "cat", "breed": "Domestic Shorthair",
                "color": "Black", "gender": "male", "weight": 5.8,
                "date_of_birth": date(2019, 9, 7),
                "chip_number": "982000678901234",
                "owner_first_name": "Lisa", "owner_last_name": "Martinez",
                "owner_email": "lisa.m@email.com", "owner_phone": "5556789012",
                "owner_address": "987 Birch Ln, City, State 12345",
                "medical_history": "Outdoor/indoor cat, up to date on vaccines",
                "allergies": "None"
            },
            
            # Other pets
            {
                "pet_name": "Tweety", "species": "bird", "breed": "Canary",
                "color": "Yellow", "gender": "unknown", "weight": 0.02,
                "date_of_birth": date(2021, 4, 12),
                "chip_number": None,
                "owner_first_name": "Anna", "owner_last_name": "Garcia",
                "owner_email": "anna.g@email.com", "owner_phone": "5557890123",
                "owner_address": "147 Cedar St, City, State 12345",
                "medical_history": "Healthy, sings beautifully",
                "special_notes": "Keep away from drafts"
            },
            {
                "pet_name": "Thumper", "species": "rabbit", "breed": "Holland Lop",
                "color": "Brown and white", "gender": "male", "weight": 1.8,
                "date_of_birth": date(2020, 8, 25),
                "chip_number": None,
                "owner_first_name": "Tom", "owner_last_name": "Anderson",
                "owner_email": "tom.a@email.com", "owner_phone": "5558901234",
                "owner_address": "258 Spruce Ave, City, State 12345",
                "medical_history": "Neutered, healthy",
                "special_notes": "Needs hay and fresh vegetables daily"
            },
        ]
        
        # Create patients with tenant_id = 1 (cityclinic)
        created_pets = []
        for pet_data in pets_data:
            pet = Patient(**pet_data, tenant_id=1)
            db.add(pet)
            db.commit()
            db.refresh(pet)
            created_pets.append(pet)
            print(f"  [OK] Created: {pet.pet_name} ({pet.species}) - Owner: {pet.owner_full_name}")
        
        print(f"\nCreated {len(created_pets)} pets")
        
        # Create vaccine records
        print("\nCreating vaccine records...")
        vaccines_created = 0
        
        for pet in created_pets:
            if pet.species in ['dog', 'cat']:
                # Common vaccines for dogs and cats
                if pet.species == 'dog':
                    vaccines = [
                        {
                            "vaccine_name": "Rabies",
                            "vaccine_type": "Core",
                            "date_given": date.today() - timedelta(days=365),
                            "next_due_date": date.today() + timedelta(days=365),
                            "veterinarian_name": "Dr. Smith"
                        },
                        {
                            "vaccine_name": "DHPP",
                            "vaccine_type": "Core",
                            "date_given": date.today() - timedelta(days=180),
                            "next_due_date": date.today() + timedelta(days=185),
                            "veterinarian_name": "Dr. Johnson"
                        },
                    ]
                else:  # cat
                    vaccines = [
                        {
                            "vaccine_name": "Rabies",
                            "vaccine_type": "Core",
                            "date_given": date.today() - timedelta(days=400),
                            "next_due_date": date.today() + timedelta(days=330),
                            "veterinarian_name": "Dr. Smith"
                        },
                        {
                            "vaccine_name": "FVRCP",
                            "vaccine_type": "Core",
                            "date_given": date.today() - timedelta(days=200),
                            "next_due_date": date.today() + timedelta(days=165),
                            "veterinarian_name": "Dr. Martinez"
                        },
                    ]
                
                for vaccine_data in vaccines:
                    vaccine = Vaccine(
                        **vaccine_data,
                        patient_id=pet.id,
                        tenant_id=1
                    )
                    db.add(vaccine)
                    vaccines_created += 1
        
        db.commit()
        print(f"  [OK] Created {vaccines_created} vaccine records")
        
        # Create treatment records
        print("\nCreating treatment records...")
        treatments_created = 0
        
        treatment_types = [
            {
                "treatment_type": "Checkup",
                "treatment_name": "Annual Wellness Exam",
                "diagnosis": "Healthy",
                "treatment_plan": "Continue current care",
                "cost": 75.00
            },
            {
                "treatment_type": "Dental",
                "treatment_name": "Dental Cleaning",
                "diagnosis": "Mild tartar buildup",
                "treatment_plan": "Professional cleaning performed",
                "cost": 250.00
            },
            {
                "treatment_type": "Surgery",
                "treatment_name": "Spay/Neuter",
                "diagnosis": "Routine sterilization",
                "treatment_plan": "Surgery successful, recovery normal",
                "cost": 350.00
            },
        ]
        
        for i, pet in enumerate(created_pets[:5]):  # Add treatments for first 5 pets
            treatment_data = random.choice(treatment_types)
            treatment = Treatment(
                **treatment_data,
                patient_id=pet.id,
                tenant_id=1,
                treatment_date=date.today() - timedelta(days=random.randint(30, 180)),
                veterinarian_name=random.choice(["Dr. Smith", "Dr. Johnson", "Dr. Martinez"])
            )
            db.add(treatment)
            treatments_created += 1
        
        db.commit()
        print(f"  [OK] Created {treatments_created} treatment records")
        
        print("\n" + "="*60)
        print("Test data creation complete!")
        print("="*60)
        print(f"\nSummary:")
        print(f"  - {len(created_pets)} pets created")
        print(f"  - {vaccines_created} vaccine records")
        print(f"  - {treatments_created} treatment records")
        print(f"\nYou can now:")
        print(f"  1. View pets at: http://localhost:8000/patients")
        print(f"  2. Check API docs: http://localhost:8000/docs")
        print(f"  3. Test your frontend!")
        print()
        
    except Exception as e:
        print(f"\n[ERROR] Error creating test data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_pets()

