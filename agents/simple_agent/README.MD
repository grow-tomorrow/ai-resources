* Create the virtual environment: `python3 -m venv .pyenv`
* Activate the virtual environment: `source .pyenv/bin/activate`
* Install dependencies: `pip install -r requirements.txt`

Create a `.env` file with:
```
DEBUG=false
OPENAI_API_KEY=your_api_key_here
```

Run the app `python3 project.py`

## Configuration

### Debug Logging

Set `DEBUG=true` in your `.env` file to enable verbose debug output. Set `DEBUG=false` (or omit it) to disable debug logging. Error messages will always be displayed regardless of the DEBUG setting.