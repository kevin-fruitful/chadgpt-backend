# ETH TOKYO TPAIN GPT PYTHON BACKEND

## Setup

Clone the repository:

```zsh
git clone https://github.com/your-username/your-repo-name.git
```

```zsh
cd your-repo-name
```

Create and activate a virtual environment:

```zsh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

Install the dependencies:

```zsh
pip install -r requirements.txt
```

### Run the application

```zsh
python app.py
```

Now, the backend is running on `http://127.0.0.1:5000/`

### Docker / DigitalOcean hosting

Our backend is hosted at `http://64.226.69.24`

```zsh
docker run -d -p 80:5000 --name practical_mcclintock your-image-name
```

### Notes

After installing dependencies, add them to `requirements.txt`

```zsh
pip freeze > requirements.txt
```
