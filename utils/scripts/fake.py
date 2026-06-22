import sys
from faker import Faker

def main():
    if len(sys.argv) < 2:
        print("Error: Missing faker module argument")
        sys.exit(1)
        
    module = sys.argv[1]
    fake = Faker()
    
    try:
        print(getattr(fake, module)())
    except AttributeError:
        print(f"Error: Invalid faker module '{module}'")
        sys.exit(1)

if __name__ == "__main__":
    main()