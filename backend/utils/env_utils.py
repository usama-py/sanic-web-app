import os
from dotenv import load_dotenv

def get_env_var(variable):
    dotenv_path = os.path.join(os.getcwd(), '.env')
    load_dotenv(override=True, dotenv_path=dotenv_path)
    return os.getenv(variable)
