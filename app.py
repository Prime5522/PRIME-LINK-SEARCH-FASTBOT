import logging
from flask import Flask

app = Flask(__name__)

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%I:%M:%S %p'
)

@app.route('/')
def hello_world():
    app.logger.info("LazyURLhunter is running.")
    return 'LazyURLhunter is Running ! Smile Baby'

if __name__ == "__main__":
    app.run(debug=True)
