from api.models import Company
import csv

# load data and send them to sqlite database: 
def run():
    with open('utils/esg_result.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        Company.objects.all().delete()

        for row in reader:
            print(row)


            company = Company(name=row[0],
                        ric_code=row[1],
                        esg_score=row[2],
                        environment_score=row[3],
                        social_score=row[4],
                        governance_score=row[5],
                        rank=row[6],
                        total=row[7],
                        )
            company.save()