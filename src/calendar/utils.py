
month_map = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12
}

weekday_map = {
    "MONDAY": 1,
    "TUESDAY": 2,
    "WEDNESDAY": 3,
    "THURSDAY": 4,
    "FRIDAY": 5,
    "SATURDAY": 6,
    "SUNDAY": 7
}


future_maturity_month_map = {
    "F": "JAN",
    "G": "FEB",
    "H": "MAR",
    "J": "APR",
    "K": "MAY",
    "M": "JUN",
    "N": "JUL",
    "Q": "AUG",
    "U": "SEP",
    "V": "OCT",
    "X": "NOV",
    "Z": "DEC"
}

call_option_maturity_month_map = {
    "A": "JAN",
    "B": "FEB",
    "C": "MAR",
    "D": "APR",
    "E": "MAY",
    "F": "JUN",
    "G": "JUL",
    "H": "AUG",
    "I": "SEP",
    "J": "OCT",
    "K": "NOV",
    "L": "DEC"
}

put_option_maturity_month_map = {
    "M": "JAN",
    "N": "FEB",
    "O": "MAR",
    "P": "APR",
    "Q": "MAY",
    "R": "JUN",
    "S": "JUL",
    "T": "AUG",
    "U": "SEP",
    "V": "OCT",
    "W": "NOV",
    "X": "DEC"
}


# option_maturity_month_map = {
#     "CALL": call_option_maturity_month_map,
#     "PUT": put_option_maturity_month_map
# }

option_maturity_month_map = {
    **call_option_maturity_month_map,
    **put_option_maturity_month_map
}











