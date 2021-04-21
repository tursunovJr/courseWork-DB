copy control_patients(full_name, date, phone) 
from 'home/asus/home/projects/medlight-dbCourseWork/generate_data/patients.csv' delimiter ',' csv;

copy control_records(full_name, register_date, doctor_type, payment_status, used_services, total_sum, patient) 
from 'home/asus/home/projects/medlight-dbCourseWork/generate_data/records.csv' delimiter ',' csv;