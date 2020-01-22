import os
import os.path
import dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

WEB_APP_URL = os.environ.get("WEB_APP_URL")
