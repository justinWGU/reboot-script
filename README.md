# Reboot Script

## Author 
Justin Ortiz

## Description 
Console-based app engineered to effortlessly reboot machines on
our LEI network. It is designed to require as little input as possible
and save time on repetitive password entries.

## Installation Instructions

### Prerequisites:
- python 3.6+
- pip

### Steps:
1. Clone repository:
    ```
        git clone https://github.com/justinWGU/reboot-script.git    
    ```
2. CD into directory:
   ```
      cd reboot-script/
   ```
3. Install requirements: 
    ```
        pip install -r requirements.txt
    ```
4. Run program with the hostname you want to reboot:
   - ONLY include hostname without the domain extension!
    ```
        python main.py $HOSTNAME
    ```
