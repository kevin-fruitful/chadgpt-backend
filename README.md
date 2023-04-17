# ChadGPT Backend

**WARNING THIS REPO HAS TONS OF ISSUES AND IS NOT SAFE TO USE FOR PRODUCTION**

Backend for ChadGPT - ETH Tokyo Hackathon

This project is the backend for ChadGPT, which was created during the ETH Tokyo Hackathon in 36 hours. The backend is designed to support the ChadGPT application, an innovative solution for using AI to help with coding and finding bugs, with a focus on smart contracts.

[ETH Global ChadGPT showcase](https://ethglobal.com/showcase/chadgpt-kikng)

Thank you to [Filecoin FVM](https://fvm.filecoin.io/) for awarding us with a prize!

## Getting Started

These instructions will help you set up the project on your local machine for development and testing purposes. See the deployment section for notes on how to deploy the project on a live system.

### Prerequisites

To run the backend, you will need:

- Python >=3.9
- Docker (optional)

### Installing

Clone the repository:

```zsh
git clone https://github.com/kevin-fruitful/chadgpt-backend.git
```

Create and activate a virtual environment:

```zsh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

Install the required packages:

```zsh
pip install -r requirements.txt
```

Set up the environment variables:

```zsh
OPENAI_API_KEY=
```

Run the backend locally:

```zsh
flask run --port 8000
```

or

```zsh
python app.py
```

Your backend should now be running at `http://localhost:8000`.

## Deployment

To deploy the backend, containerize it using Docker and deploy it on your preferred cloud provider or VPS. See the [Docker documentation](https://docs.docker.com/) and the specific cloud provider's documentation for more details on how to deploy the Docker container.

## Built With

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [LangChain SDK](https://github.com/hwchase17/langchain)

## ETH Tokyo ChadGPT Team

[Kevin Park](https://github.com/kevin-fruitful) [@kevin-fruitful](https://github.com/kevin-fruitful)
[Ariel Chen](https://github.com/Arielpopcorn) [@Arielpopcorn](https://github.com/Arielpopcorn)
[Caitlin Zhang](https://github.com/caitlinthebest) [@caitlinthebest](https://github.com/caitlinthebest)
[Tesa Ho](https://github.com/tesaho) [@tesaho](https://github.com/tesaho)
[Tim Cox](https://github.com/timncox) [@timncox](https://github.com/timncox)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/yourusername/projectname/blob/master/LICENSE.md) file for details.

## Acknowledgments

- The ETH Tokyo Hackathon organizers and sponsors for providing the opportunity to build this project.
- The amazing mentors and fellow participants at ETH Tokyo for their support and collaboration.
-- Special shoutout to [Jeff Lau](https://github.com/jefflau) [@jefflau](https://github.com/jefflau)
- Everyone who has contributed to the open-source tools and libraries used in this project.

### Notes

After installing dependencies, add them to `requirements.txt`

```zsh
pip freeze > requirements.txt
```
