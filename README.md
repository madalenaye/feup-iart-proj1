# feup-iart-proj1
## Group T09G03
| Name             | Number    | E-Mail             |
| ---------------- | --------- | ------------------ |
| Luís Duarte         | 202108734 | up202108734@fe.up.pt                |
| Madalena Ye         | 202108795 | up202108795@fe.up.pt            |
| João Figueiredo       | 202108873 | up202108873@fe.up.pt            | 
## Fanorona
### Instructions for compiling, running and using the project

#### Dependencies
Before running the program, make sure you have installed the dependencies listed in the `requirements.txt`` file. To install the dependencies, open the terminal, navigate to the project directory, and run the following command:
```bash
pip install -r requirements.txt
```
Or if you want to use poetry, you can run the following command:
```bash
poetry install
```
#### Running the project
After installing the dependencies, you can run the game by running the main.py file. Open the terminal, navigate to the project directory, and run the following command:

```bash
python src/main.py
```

Or if you want to run the project using poetry.
```bash
poetry run python src/main.py
```
This will start the game

#### Playing the game
You will be presented with a main menu. You can navigate to the "Options" window to choose the game mode for each player and the bots levels if you wish to use AI. After that, you can return to the main menu and start the game. You will be asked which player will be starting, in other words who is going to be the white pieces.

You can find out more about the game rules in the following link: [Fanorona Rules](https://www.mastersofgames.com/rules/Fanorona%20Rules.pdf)


#### Testing the AI

The `src/ai_test` Python script will use multiprocessing to run 30 games of each permutation of AI type (15 games on each side). By default, it will consume $N-2$ CPU cores and probably take around 30 mins (running on 16 cores). This makes the process of comparing the different AI algorithms easier. The multiprocessing implementation is highly scalable so adding future AI algorithms doesn't make the script impossible to run in a decent time.
