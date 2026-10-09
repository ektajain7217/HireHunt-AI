
import os
from dotenv import load_dotenv
from tinyfish import TinyFish

# Load the key from the local .env file
load_dotenv()

api_key = os.getenv("TINYFISH_API_KEY")

if not api_key:
    raise SystemExit(
        "API key not found. Check that .env is in the project folder."
    )

print("API key found. Its value will not be displayed.")

try:
    client = TinyFish(api_key=api_key)

    # A small live-web test using TinyFish Agent
    response = client.agent.run(
        url="https://example.com",
        goal="Read this webpage and return its page title "
             "and a one-sentence summary."
    )

    print("TinyFish request completed.")
    print("Result:", response.result)

except Exception as error:
    # Do not print request headers or the API key.
    print("TinyFish request failed.")
    print("Error type:", type(error).__name__)
    print("Check your API key, network connection, "
          "SDK documentation, and account access.")