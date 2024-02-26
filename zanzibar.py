# determine how many test cases have been logged
test_count = int(input(""))

# collect each case's log
test_cases = []
for _ in range(test_count):
    data_in = input("")
    yearly_logs = data_in.split(" ")
    test_cases.append(int(yearly_log) for yearly_log in yearly_logs)

# check each case
for test_case in test_cases:
    # base year log
    last_years_log = 1
    # guaranteed imports
    lower_bound = 0

    # pass through the years
    for yearly_log in test_case:
        # determine difference between max 'birthing'
        log_difference = yearly_log - 2 * last_years_log
        if log_difference > 0:
            lower_bound += log_difference
        # update last year
        last_years_log = yearly_log

    # print the lower bound for the number of turtles not born on Zanzibar
    print(lower_bound)
