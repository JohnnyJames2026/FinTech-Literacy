#0 is per year, 1 is per semester, 2 is per month, 3 is biweekly, 4 is weekly
#requires tuition value (list w/per value, scholarships and aid (list of lists w/ per value), and loans w/ per value where the first value is money amount and second value is per value
#costOfLiving is for rent and utilities

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)






#semester length
def convertToYear(conversion,months = 8):
    conversion[0] = int(conversion[0])
    if conversion[1] == 'Year':
        print(conversion[0])
        return conversion[0]
    elif conversion[1] == 'Semester':
        conversion[0] *= 2
    elif conversion[1] == 'Monthly':
        conversion[0] *= 12 #rough calculation maybe revisit this
    elif conversion[1] == '10 Month Term':
        #conversion[0] *= 1.0/3.0 * 52 
        #very rough calculation probably ask for length of semester
        conversion[0] *= 10
    elif conversion[1] == 4:
        conversion[0] *= months * 4 
        #very rough calculation probably ask for length of semester
    return conversion[0]
            

def loanCalc(loans):
    #loans are lists in lists
    #each loan list has [0]: money, [1]: perValue, [2]: subsidized or unsubsidized (true false respectively), [3]: interest rate, [4]: semester tag ('Semester1, Semester2, SemesterSummer, Year)
    #calculated loan will be [0][x]: subsidized, [1][x]: unsubsidized
    #[0][0]: money to pay back (written at end of calculator), [1][0]: interest (that can be paid per month), [1][1]: total interest, [1][2]: total money to pay by end of school career
    if loans[1] == 'Subsidized':
        loanTotal = loans[0]
    else:
        loanTotal = - (int(loans[0]) * 0.04) + int(loans[0])
    
    
    #loans = [subLoans,unsubLoans]
    return loanTotal
            

def tuitionCalc(tuitions, scholarships, loans, costOfLiving, income):
    print(tuitions)
    print(scholarships)
    print(loans)
    print(income)
    print(costOfLiving)
  
    #convert everything to be by semester basis for ease of calculation
    #tuition
    #tuition is list of lists where tuition[x][1] are all the same value
    tuitionTotal = 0
    
    tuitionTotal = convertToYear(tuitions)

    #scholarships
    scholarshipTotal = 0
    scholarshipTotal = convertToYear(scholarships)

    #loans
    #loans is list of lists
    #loan list - [0], money: [1], perValue: [2], subsidized (True) or unsubsidized (False): [3], interest rate:
    loanTotal = loanCalc(loans)
        



    #income
    #income has options for per year, per semester, per month, biweekly, and weekly
    incomeTotal = 0
    incomeTotal = convertToYear(income)

    #cost of living
    #cost of living is list of lists - list 1 has rent,perValue,False,months and list 2 has utilities,perValue,False,months
    #if per month is chosen, months changes depending on length of lease, ask that,
    costOfLivingTotal = 0
    costOfLivingTotal = convertToYear(costOfLiving)

    #work study
    #work study is list - [0], money: [1], perValue: [2], hourlyWage (if there is an hourly wage, else value is False): [3], hours per week (if Nan, then False)
    #workStudy = convertToYear(workStudy)
    
    
    #final calc
    print(tuitionTotal)
    print(scholarshipTotal)
    print(loanTotal)
    print(incomeTotal)
    print(costOfLivingTotal)

    return scholarshipTotal + loanTotal + incomeTotal - costOfLivingTotal - tuitionTotal

  
def calcDistrution(remainder):
    fixed_expenses = remainder * .5
    savings = remainder * .2
    flex_expenses = remainder * .3
    distribution = (fixed_expenses, savings, flex_expenses)
    return distribution

#def tester():
 #   print('something')

@app.route('/')
def loader():
    
    return render_template('index.html')

@app.route('/evaluate', methods = ['GET','POST'])
def evaluate():
    if request.method == 'POST':
        content = request.json
    fixed_expenses = tuitionCalc([content["tuition_amount"],content["tuitionDrop"]],[content["aidTypeText"],content["aidTypeDrop"]],[content["typeLoanText"],content["typeLoanDrop"]],[content["rentText"],content["rentDrop"]],[content["misc"],content["miscDrop"]])
    print(fixed_expenses)
    fixed_expenses = str(fixed_expenses)

    # do the calculations
    return jsonify(fixed_expenses)




'''def main():
    while True:
        pass'''

if __name__ == '__main__':
    app.run()