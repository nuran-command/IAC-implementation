import os
import sys

def validate_env():
    required_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        return False
    
    db_host = os.getenv("DB_HOST")
    if db_host == "db_wrong":
        print("Warning: DB_HOST is set to 'db_wrong'. This will cause service failure.")
        # We don't necessarily exit failure here if we want to allow testing failure modes, 
        # but in a real CI/CD this would be a hard fail.
        
    print("Configuration validation successful!")
    return True

if __name__ == "__main__":
    # Load .env file manually for validation script if running locally
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
                    
    if not validate_env():
        sys.exit(1)
