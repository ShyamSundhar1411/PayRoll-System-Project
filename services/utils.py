import pandas as pd
def generate_dictionary(dataframe):
    employee_status = {}
    employee_total = {}
    current_emp_code = None
    for index, row in dataframe.iterrows():
        emp_code = row["Emp_Code"]
        status = row["Status"]
        total = row["Total"]
        if pd.isna(total):
            total = pd.to_datetime("00:00:00")
        if not pd.isna(emp_code):
            current_emp_code = emp_code
            employee_status[current_emp_code] = []
            employee_total[current_emp_code] = []
        if not pd.isna(status):
            print("{}:{}".format(current_emp_code,status))
            employee_status[current_emp_code].append(status)
            employee_total[current_emp_code].append(total)
    return employee_status,employee_total


    