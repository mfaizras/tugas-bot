import datetime
class SystemMessage:
    @staticmethod
    def log(message):
        print(f"\033[85m{datetime.datetime.now()} \033[0m  \033[96m[LOG]\033[0m \033[32m {message}\033[0m")

    @staticmethod
    def warning(message):
        print(f"\033[85m{datetime.datetime.now()} \033[0m  \033[96m[WARN]\033[0m \033[32m {message}\033[0m")