# Question Answer Application for OpenAI(Web based Python solution)

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.

3. Navigate into the project directory:

   ```bash
   $ cd web-crawler/python-solution
   ```

4. Create a new virtual environment:

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file:

   ```bash
   $ cp .env.example .env
   ```

7. Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file or export the environment variable as OPENAI_API_KEY

9. run the following commands
python3 scraper.py - (for scraping the data)
python3 embed.py - (for generating embeddings)
flask run

OPTIONAL - Alternatively you can run ./run to install the required dependencies and run the app

You should now be able to access the app at [http://localhost:5000]

Link to presentation
https://npuniversityedu-my.sharepoint.com/:p:/g/personal/psethi21343_student_sfbu_edu/Ec18lP9dV2NBnq3ot4qJwd4BZnl3qr-klyRi1m6RUDWPMw?e=gQNXcn
