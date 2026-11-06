print("Hello, I'm learning Python")

# Personal Information (Example Data - Safe to Share)
first_name = "Alex"
last_name = "Johnson"
age = 28
email = "alex.johnson@example.com"
city = "Toronto"
country = "Canada"

# Print information in a formatted way
print(f"""
    Name: {first_name} {last_name}
    Age:  {age}
    Email: {email}
    Location: {city} {country}
""")

# Perform Arithmetic Operations
    # How old will Alex be in 10 years?
future_age = age + 10
print(f"In 10 years, {first_name} will be {future_age} years old.")

    # How old was Alex 5 years ago?
past_age = age - 5
print(f"5 years ago, {first_name} was {past_age} years old.")

    # How many days has Alex been alive? (rough estimate)
days_alive = age * 365 #assume 365 days in a year
print(f"{first_name} has been alive for roughly {days_alive} days.")

    # How many years until retirement at 65?
years_to_retirement = 65 - age
print(f"{first_name} has {years_to_retirement} years until retirement at 65.")
