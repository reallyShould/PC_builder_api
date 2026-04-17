import datetime

log_file = "main.log"

def log(text, level="info"):
    with open(log_file, "a+") as f:
        f.write(f"{datetime.datetime.now()} [{level}] {text}\n")

#TODO Create logger for parser