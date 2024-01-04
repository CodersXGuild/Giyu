## Deploy Methods
 

### [ Local Host or vps ] 
<details>
  <summary>Steps for local deploy</summary>
  
- `git clone https://github.com/Lynnxept/Giyu{repo last name}`
- `cd Giyu`
- `pip3 install -U -r requirements.txt`
- `python3 -m Giyu`

### [ Some important notes ]
```
1. Use only postgres db
2. This bot is inbuilt fill all your requirements in config.py before hosting
3. This bot is very advanced and highly optimised
4. you can host this bot on vps,heroku,okteto,mogenius etc.
# [ For Workflows ]
```bash
name: CI
on: 
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v3
        with: 
          python-version: "3.10"
      - name: Installation of dependencies
        run: |
          sudo apt update 
          sudo apt install ffmpeg
          pip install --upgrade pip
          pip install -U -r requirements.txt
      - name: Deploy Logs 
        run: python3 -m Giyu
