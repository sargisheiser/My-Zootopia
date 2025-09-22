# 🦊 My Zootopia


A simple Python project that fetches animal data from the [API Ninjas Animals API](https://api-ninjas.com/api/animals) and generates a styled HTML website to display animal information.


---


## 🚀 Features
- Fetch animal data dynamically from the API
- Generate an HTML website with animal cards
- Supports filtering animals by skin type
- Secure API key handling using `.env`


---


## 📦 Installation


Clone the repository:


```bash


git clone https://github.com/sargisheiser/My-Zootopia.git
cd My-Zootopia
```


## Install dependencies:
```bash
  pip install -r requirements.txt
```
## ⚙️ Usage


Run the website generator:
```bash
  python animals_web_generator.py
```


Example:
```bash


Please enter an animal: Fox
Website was successfully generated to animals.html
```


Then open animals.html in your browser to view the results.


## 🔑 Environment Variables


You’ll need an .env file in the project root with your API key:
```bash
 API_KEY='your_api_key_here'
```
## 🛠 Tech Stack


Python 3


Requests for HTTP requests


python-dotenv for environment variables


HTML + CSS for website output


## 🤝 Contributing


Pull requests are welcome!
If you’d like to contribute, fork the repo and create a feature branch. Please open an issue first to discuss what you’d like to change.


## 📄 License


This project is for educational purposes only.
