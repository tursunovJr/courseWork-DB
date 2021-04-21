from faker import Faker
from random import randint
from random import choice

MAX_PATIENTS = 10
MAX_RECORDS = 40
doctors = ['Невропатолог', 'Стоматолог', 'Кардиолог']
payment_status = ['Да', 'Нет']

neurolog_services = {
    'consultation': 50000,
    'eeg': 40000,
    'reg': 45000,
    'exo': 40000
}

kardiolog_services = {
    'consultation': 50000,
    'ekg': 40000
}

stomatolog_services = {
    'consultation': 50000,
    'treatment': 100000,
    'implant': 3500000,
    'braces': 5000000,
   'inspection': 50000
 }

def count_services_and_total_sum(doctor):
    res = []
    i = 0
    total_sum = 0
    if doctor == 'Невропатолог':
        servise = choice(list(neurolog_services.keys()))
        while servise not in res and i < 3:
            res.append(servise)
            total_sum += neurolog_services[servise]
            i=i-1
            servise = choice(list(neurolog_services.keys()))
    if doctor == 'Стоматолог':
        servise = choice(list(stomatolog_services.keys()))
        while servise not in res and i < 3:
            res.append(servise)
            total_sum += stomatolog_services[servise]
            i=i-1
            servise = choice(list(stomatolog_services.keys()))
    if doctor == 'Кардиолог':
        servise = choice(list(kardiolog_services.keys()))
        res.append(servise)
        total_sum += kardiolog_services[servise]
    return res, total_sum




def generate_names():
    faker = Faker()
    names = []
    for _ in range(MAX_PATIENTS):
        names.append(faker.name())
    return names

def generate_patients(names):
    faker = Faker() 
    f = open('patients.csv', 'w')
    for i in range(MAX_PATIENTS):
        line = "{0},{1},{2}\n".format(
                                      names[i],
                                      faker.date(),
                                      faker.phone_number())
        f.write(line)
    f.close()

def generate_records(names):
    faker = Faker()
    f = open('records.csv', 'w')
    for i in range(MAX_RECORDS):
        patient_id = randint(0, 9)
        doctor_type = choice(doctors)
        pay_status = choice(payment_status)
        used_services, total_sum = count_services_and_total_sum(doctor_type)
        line = "{0},{1},{2},{3},{4},{5},{6}\n".format(
                                            names[patient_id], 
                                            faker.date(), 
                                            doctor_type, 
                                            pay_status,
                                            used_services,
                                            total_sum,
                                            patient_id)
        f.write(line)
    f.close()

if __name__ == "__main__":
    names = generate_names()
    generate_patients(names)
    generate_records(names)