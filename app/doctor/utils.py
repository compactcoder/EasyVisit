import secrets
from PIL import Image
from flask import current_app

import os

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

doctor_specialties = [
    "Allergist/Immunologist",
    "Anesthesiologist",
    "Cardiologist",
    "Cardiothoracic Surgeon",
    "Colorectal Surgeon",
    "Dentist",
    "Dermatologist",
    "Dermatopathologist",
    "Diagnostic Radiologist",
    "Emergency Medicine Physician",
    "Endocrinologist",
    "Family Medicine Physician",
    "Forensic Pathologist",
    "Gastroenterologist",
    "General Surgeon",
    "Geriatrician",
    "Hematologist",
    "Hepatologist",
    "Infectious Disease Specialist",
    "Internal Medicine Physician",
    "Interventional Radiologist",
    "Maternal-Fetal Medicine Specialist",
    "Medical Geneticist",
    "Neonatologist",
    "Nephrologist",
    "Neurological Surgeon",
    "Neurologist",
    "Neuropathologist",
    "Neuroradiologist",
    "Obstetrician/Gynecologist (OB/GYN)",
    "Occupational Medicine Specialist",
    "Oncologist",
    "Ophthalmologist",
    "Oral and Maxillofacial Surgeon",
    "Orthodontist",
    "Orthopedic Surgeon",
    "Otolaryngologist (ENT)",
    "Pathologist",
    "Pediatric Cardiologist",
    "Pediatric Dentist",
    "Pediatric Endocrinologist",
    "Pediatric Gastroenterologist",
    "Pediatric Hematologist/Oncologist",
    "Pediatric Nephrologist",
    "Pediatric Neurologist",
    "Pediatric Ophthalmologist",
    "Pediatric Orthopedic Surgeon",
    "Pediatric Surgeon",
    "Pediatrician",
    "Periodontist",
    "Physical Medicine and Rehabilitation Physician",
    "Plastic Surgeon",
    "Preventive Medicine Specialist",
    "Psychiatrist",
    "Pulmonologist",
    "Radiation Oncologist",
    "Radiologist",
    "Reproductive Endocrinologist",
    "Rheumatologist",
    "Sleep Medicine Specialist",
    "Sports Medicine Physician",
    "Surgical Oncologist",
    "Thoracic Surgeon",
    "Urologist",
    "Vascular Surgeon"
]

indian_languages = [
    "English",
    "Hindi",
    "Assamese",
    "Bengali",
    "Gujarati",
    "Kannada",
    "Kashmiri",
    "Konkani",
    "Malayalam",
    "Manipuri",
    "Marathi",
    "Nepali",
    "Odia",
    "Punjabi",
    "Sanskrit",
    "Santali",
    "Sindhi",
    "Tamil",
    "Telugu",
    "Urdu"
]

indian_cities = [
    "Agra",
    "Ahmedabad",
    "Ajmer",
    "Akola",
    "Aligarh",
    "Allahabad",
    "Ambattur",
    "Amravati",
    "Amritsar",
    "Asansol",
    "Aurangabad",
    "Bangalore",
    "Baranagar",
    "Barasat",
    "Bareilly",
    "Belgaum",
    "Bhavnagar",
    "Bhilai",
    "Bhiwandi",
    "Bhopal",
    "Bhubaneswar",
    "Bihar Sharif",
    "Bikaner",
    "Bilaspur",
    "Bokaro",
    "Chandigarh",
    "Chandrapur",
    "Coimbatore",
    "Cuttack",
    "Darbhanga",
    "Dehradun",
    "Delhi",
    "Dewas",
    "Dhanbad",
    "Durg",
    "Durgapur",
    "Eluru",
    "Erode",
    "Etawah",
    "Faridabad",
    "Farrukhabad",
    "Firozabad",
    "Gandhidham",
    "Gaya",
    "Ghaziabad",
    "Gorakhpur",
    "Gulbarga",
    "Guntur",
    "Gurgaon",
    "Guwahati",
    "Gwalior",
    "Haridwar",
    "Hisar",
    "Howrah",
    "Hubli-Dharwad",
    "Hyderabad",
    "Ichalkaranji",
    "Imphal",
    "Indore",
    "Jabalpur",
    "Jaipur",
    "Jalandhar",
    "Jalgaon",
    "Jammu",
    "Jamnagar",
    "Jamshedpur",
    "Jhansi",
    "Jodhpur",
    "Junagadh",
    "Kadapa",
    "Kakinada",
    "Kalyan-Dombivli",
    "Kamarhati",
    "Kanpur",
    "Karawal Nagar",
    "Karnal",
    "Katni",
    "Kochi",
    "Kolhapur",
    "Kollam",
    "Kolkata",
    "Kota",
    "Kozhikode",
    "Kulti",
    "Kurnool",
    "Latur",
    "Loni",
    "Lucknow",
    "Ludhiana",
    "Madurai",
    "Maheshtala",
    "Malegaon",
    "Mangalore",
    "Mathura",
    "Meerut",
    "Mirzapur",
    "Moradabad",
    "Mumbai",
    "Muzaffarnagar",
    "Muzaffarpur",
    "Mysore",
    "Nagpur",
    "Naihati",
    "Nanded",
    "Nashik",
    "Navi Mumbai",
    "Nellore",
    "New Delhi",
    "North Dumdum",
    "Panihati",
    "Panipat",
    "Parbhani",
    "Patiala",
    "Patna",
    "Pimpri-Chinchwad",
    "Pondicherry",
    "Pune",
    "Purnia",
    "Raichur",
    "Raipur",
    "Rajkot",
    "Rajpur Sonarpur",
    "Rampur",
    "Ranchi",
    "Ratlam",
    "Rewa",
    "Rohtak",
    "Rourkela",
    "Sagar",
    "Saharanpur",
    "Salem",
    "Sangli-Miraj & Kupwad",
    "Satara",
    "Satna",
    "Secunderabad",
    "Shahjahanpur",
    "Shimoga",
    "Silchar",
    "Siliguri",
    "Sivakasi",
    "Srinagar",
    "Srirampur",
    "Surat",
    "Surendranagar Dudhrej",
    "Tambaram",
    "Thane",
    "Thanjavur",
    "Thoothukudi",
    "Thrissur",
    "Tiruchirappalli",
    "Tirunelveli",
    "Tirupati",
    "Tirupur",
    "Tiruvottiyur",
    "Tiruvannamalai",
    "Tiruvottiyur",
    "Titagarh",
    "Trichy",
    "Trivandrum",
    "Tumkur",
    "Ulhasnagar",
    "Uluberia",
    "Ujjain",
    "Udaipur",
    "Udupi",
    "Vadodara",
    "Varanasi",
    "Vasai-Virar",
    "Vijayawada",
    "Vijayanagaram",
    "Visakhapatnam",
    "Warangal",
    "Yamunanagar"
]

week_days = [
    "Monday", 
    "Tuesday", 
    "Wednesday", 
    "Thursday", 
    "Friday", 
    "Saturday", 
    "Sunday"
]


specialities_set = ["Anaesthesia","Breast cancer","Cardiac surgery","Cardiology","Clinical Nutrition and Dietetics","Cranio Maxillo Facial Surgery","Critical Care Medicine","Dental Sciences","Dermatology and Cosmetology","Electrophysiology","Emergency Medicine","Endocrinology and Diabetes","ENT","Family Medicine","Gastrointestinal oncology","General Surgery","Gynaecology-Oncology","Haematology and Haemato-Oncology","Haematology","Head and Neck Surgery","HPB Surgery","Infectious Diseases","Internal Medicine","Interventional radiology","Medical Gastroenterology","Medical Oncology","Microbiology","Nephrology","Neurology","Neurosurgery","Obstetrics & Gynaecology","Oncology","Ophthalmology","Orthopedics and Trauma","Pathology","Physiotherapy and Rehabilitation","Plastic surgery","Pulmonology","Radiation Oncology","Radiology","Rheumatology","Speech and swallow rehabilitation","Spine Surgery","Surgical gastroenterology","Surgical Oncology","Thoracic Surgery","Vascular Surgery","Urology","Uro-Oncology","Other"]