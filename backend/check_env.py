from dotenv import load_dotenv
import os

load_dotenv()

def check_env():
    required_vars = {
        "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY"),
        "REPLICATE_API_TOKEN": os.getenv("REPLICATE_API_TOKEN"),
        "APP_URL": os.getenv("APP_URL", "http://localhost:5173"),
        "CORS_ORIGINS": os.getenv("CORS_ORIGINS", "http://localhost:5173")
    }

    missing = []
    for var, value in required_vars.items():
        if not value:
            missing.append(var)
        else:
            print(f"✓ {var} is set")
            if var in ["OPENROUTER_API_KEY", "REPLICATE_API_TOKEN"]:
                print(f"  Value: {value[:4]}...{value[-4:]}")

    if missing:
        print("\n❌ Missing environment variables:")
        for var in missing:
            print(f"  - {var}")
        return False
    
    return True

if __name__ == "__main__":
    print("Checking environment variables...")
    if check_env():
        print("\n✓ All required environment variables are set")
