import config  # Import your configuration settings
from runner import run  # Import the function from runner.py

def main():
    # Example of printing configuration settings (optional)
    print("Configuration loaded from config.py:")
    print(config.SETTING_1)
    print(config.SETTING_2)

    # Run the main function
    run()

if __name__ == "__main__":
    main()