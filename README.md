## Deployment

To clone this project 
```bash
  git clone https://github.com/nicolevgarduno/UserSens.git
  cd UserSens
```
You will also need to clone the following two repos:
```bash
git clone https://github.com/antoinelame/GazeTracking.git
git clone https://github.com/davisking/dlib.git
```
 - [GazeTracking](https://github.com/antoinelame/GazeTracking)
 - [dlib C++ library](https://github.com/davisking/dlib)


This project also requires Intel architecture (x86_64). For macOS, use:
```bash
arch -x86_64 /usr/bin/python3 -m venv venv
source venv/bin/activate
```

For Windows you can create a venv using:
```bash
arch -x86_64 /usr/bin/python3 -m venv venv
source venv/bin/activate
```

After creating a virtual environment, install required packages using requirements.txt file. Dependencies may mess up if you bare metal this project, so it is recommended to use a venv:
```bash
pip install -r requirements.txt
```

### When Re-Running Project:
Whenever you run to the project, pull from main and activate venv:
```bash
git pull origin main
source venv/bin/activate
```
