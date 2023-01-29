#0 is per year, 1 is per semester, 2 is per month, 3 is biweekly, 4 is weekly
#requires tuition value (list w/per value, scholarships and aid (list of lists w/ per value), and loans w/ per value where the first value is money amount and second value is per value
#costOfLiving is for rent and utilities

from flask import Flask, render_template, request
app = Flask(__name__)




#semester length
def convertToYear(conversion,months = 8):
    if conversion[1] == 0:
        return conversion[0]
    elif conversion[1] == 1:
        conversion[0] *= 2
    elif conversion[1] == 2:
        conversion[0] *= months #rough calculation maybe revisit this
    elif conversion[1] == 3:
        #conversion[0] *= 1.0/3.0 * 52 
        #very rough calculation probably ask for length of semester
        conversion[0] *= months * 2
    elif conversion[1] == 4:
        conversion[0] *= months * 4 
        #very rough calculation probably ask for length of semester

    if len(conversion) > 2:
        if not conversion[2] == False:
            conversion[0] *= months * 4 * conversion[3]
            

def loanCalc(loans):
    #loans are lists in lists
    #each loan list has [0]: money, [1]: perValue, [2]: subsidized or unsubsidized (true false respectively), [3]: interest rate, [4]: semester tag ('Semester1, Semester2, SemesterSummer, Year)
    #calculated loan will be [0][x]: subsidized, [1][x]: unsubsidized
    #[0][0]: money to pay back (written at end of calculator), [1][0]: interest (that can be paid per month), [1][1]: total interest, [1][2]: total money to pay by end of school career
    subLoans = []
    unsubLoans = []
    for loan in loans:
        if loan[2]:
            subLoans += loan[0]
        else:
            interest = loan[0] * loan[3]
            if loan[1] == 0:
                loan = [loan[0],interest,interest/8]
            elif loan[1] == 1:
                loan = [loan[0], interest*2, interest/4]    
            unsubLoans.append(loan)
    
    loans = [subLoans,unsubLoans]
    return loans
            

def tuitionCalc(tuitions, scholarships, loans, costOfLiving, income = 0, workStudy = 0):
  
    #convert everything to be by semester basis for ease of calculation
    #tuition
    #tuition is list of lists where tuition[x][1] are all the same value
    tuitionTotal = 0
    for tuition in tuitions:
        tuition = convertToYear(tuition)

    #scholarships
    scholarshipTotal = 0
    for scholarship in scholarships:
        scholarshipTotal += convertToYear(scholarship)

    #loans
    #loans is list of lists
    #loan list - [0], money: [1], perValue: [2], subsidized (True) or unsubsidized (False): [3], interest rate:
    loanTotal = loanCalc(loans)
        



    #income
    #income has options for per year, per semester, per month, biweekly, and weekly

    income = convertToYear(income)

    #cost of living
    #cost of living is list of lists - list 1 has rent,perValue,False,months and list 2 has utilities,perValue,False,months
    #if per month is chosen, months changes depending on length of lease, ask that,
    costOfLivingTotal = 0
    for cost in costOfLiving:
        if len(cost) > 3:
            costOfLivingTotal += convertToYear(cost,cost[3])
        else:
            costOfLivingTotal += convertToYear(cost)

    #work study
    #work study is list - [0], money: [1], perValue: [2], hourlyWage (if there is an hourly wage, else value is False): [3], hours per week (if Nan, then False)
    workStudy = convertToYear(workStudy)
    
    
    #final calc
    return tuitionTotal - scholarshipTotal - loanTotal - income + costOfLivingTotal - workStudy
  
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

@app.route('/evaluate', methods = ['POST'])
def evaluate():
    if request.method == 'POST':
        content = request.json
        print(content)
    
    # do the calculations

    return render_template('index.html')

'''def main():
    while True:
        pass

if __name__ == '__main__':
    main()'''