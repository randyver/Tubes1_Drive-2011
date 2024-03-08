# Tubes1_Drive-2011

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#algorithm-explained">Algorithm Explained</a>
    </li>
    <li>
      <a href="#directory-layout">Directory Layout</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#run-the-bot">Run the Bot!</a></li>
      </ul>
    </li>
    <li><a href="#authors">Authors</a></li>
  </ol>
</details>

## About the Project

This project is part of Algorithm Strategies project that implements a bot capable of playing a game strategically using greedy algorithm. The bot we're implementing is for the game Etimo Diamonds, a programming challenge where bots are competing to collect as many diamonds as possible. To increase the challange, this game includes many features to further complexify the rules, such as teleporters, random button, and tackling systems.

Full description and game rules can be seen [here](https://github.com/Etimo/diamonds2/blob/main/RULES.md)


## Algorithm Explained

The main greedy strategy used contains 4 main components, which are:
1. Collecting closest diamonds from bot.
2. Collecting closest diamonds from base.
3. Using teleport.
4. Using red button.

As we are using greedy strategy, we aim for collecting as many diamonds are possible. The maximum nuber of diamonds can be collected is 5, where after it's achieved we would want to go back to base as soon as possible. This is where the teleport is utilized if it's a shorter route home. In the other hand, our strategy to collect diamonds differ based on time. Starting on we would evaluate if the nearest diamond is close enough, otherwise we would rather hit the red button first. Diamonds are collected one by one greedily by considering the closest one to our bot, including red ones. After we hit 15 seconds on the countdown the bot would aim for the closest diamonds from base first, at max 5 steps from base. And lastly, for the final 7 seconds bot would collect diamonds no more than 2 steps from base, before saving it back home.

## Directory Layout

```
src/
├── game/
│   ├── logic/
│   │   ├── unused/
│   │   │   ├── begal.py
│   │   │   ├── collectChase.py
│   │   │   └── fullTackle.py
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── myBot.py
│   │   ├── random.py
│   │   └── testBot.py
│   ├── __init__.py
│   ├── api.py
│   ├── board_handler.py
│   ├── bot_handler.py
│   ├── models.py
│   └── util.py
├── decode.py
├── main.py
├── run-bots.bat
└── run_bot.sh
```

<!-- GETTING STARTED -->
## Getting Started

The program is only for implementing the bot itself. The game engine can be installed from [this](https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0) repository.

### Prerequisites

The following are required to be installed for this bot to run
* Node.js
* Docker Desktop
* Python
* npm
  ```sh
  npm install npm@latest -g
  ``` 
* yarn
  ```sh
  npm install --global yarn
  ```
  
### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
2. Change directory to the root of the cloned local repository using
   ```sh
   cd Tubes1_Drive-2011
   ```
3. Install dependencies using
   ```sh
   pip install -r requirements.txt
   ```

### Run the bot!
1. Make sure the game engine had been succesfully built on your machine, run it with
   ```sh
   npm run start
   ```
2. To run a single bot, use the following command
   ```sh
   python main.py --logic MyBot --email=drive2011@email.com --name=drive2011 --password=123456 --team etimo
   ```
3. For running multiple bots, run the following command
   - Windows
   ```sh
   ./run-bots.bat
   ```
   
   - Linux / (possibly) macOS
   ```sh
   ./run-bots.sh
   ```
   
## Authors
| NIM      | Name                     |
|----------|--------------------------|
| 13522027 | Muhammad Althariq Fairuz |
| 13522037 | Farhan Nafis Rayhan      |
| 13522067 | Randy Verdian            |
