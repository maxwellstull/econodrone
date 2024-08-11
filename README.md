# Econodrone
A discord bot that is able to track economy-based traits for my Dungeons & Dragons campaign. Allows for tracking of gold/currency, health, spell slots, rations, and class trait points, as well as very basic inventory tracking. 

## Setup
This setup assumes you have Python installed. I am using Python3.11.9.
1. Clone this repository
```bash
git clone https://github.com/maxwellstull/econodrone.git
```
2. Navigate to repository
```bash
cd path/to/econodrone/
```
3. Create a virtual environment
```bash
python3 -m venv venv
```
4. Activate virtual environment
```bash
#Windows
./venv/Scripts/activate

#Linux/Mac (untested, but trivial)
source venv/bin/activate
```
5. Install requirements
```bash
pip install -r requirements.txt
```
6. Create application in discord
Use [this link](https://discord.com/developers/applications) to create application and obtain secret token

7. Replace token in secret_token.py with your secret token