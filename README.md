# FastReact-api

## 📋 Description

Fast React API is the backend of a full-stack application that includes user authentication, complete CRUD functionality for products.

---

## 🛠️ Main Features

### 🔑 User Management

- Registration and authentication with JWT.
- Admin managment.

### 📝 Product Management

- Adding products.
- Updating products.
- Deleting products.
- View products.

## 📂 Folder Architecture

```plaintext
FASTReact-API/
├── env/
│   ├── include/    
│   ├── lib/         
│   ├── scripts/         
│   └── pyvenv.cfg
├── app/
│   ├── users/    
│   ├── products/         
│   ├── AppFixtures.py         
│   ├── main.py    
│   ├── security.py          
│   └── utils.py 
├── uploads/         
├── requirements.txt        
├── README.md           
└── .env 


                
```

⚙️ Installation and Launch

1. Clone the repository:

```bash
git clone https://github.com/fad-anes/FastReact-api.git
```

2. Install a virtual environment:

```bash
pip install virtualenv

```

3. Create a virtual environment:

```bash
python -m venv env

```
4. Enable virtual environment:

```bash
.\env\Scripts\activate

```
5. Install Dependencies:

```bash
pip install -r requirements.txt

```

6. Add the .env file to the project (outside the app folder)

7. Start the server:

```bash
uvicorn app.main:app --reload
```
