BINGO 75 GAME

This project contains a Python implementation to simulate the Bingo 75 game using Message Passing Interface (MPI). There is also the skeleton file (Bingo-student.py) to be provided if the assignment is given to a student that is asked to incorporate MPI directives.

----------------
PROJECT CONTENT

- Bingo-student.py --> Bingo game logic skeleton code ready to be given to the students when asked to incorporate MPI directives on it
- Bingo-teacher.py --> Bingo game logic code completed ready to be executed, including MPI directives 
- EduHPC_peachy.log --> output observed in the terminal when executing the game with 4 MPI processes

- src/Bingo75.py --> definition of the class Bingo75 used in the game logic (either Bingo-student.py or Bingo-teacher.py)
- src/Bingo75UI.py --> game graphical user interface (GUI)
- src/\_\_init\_\_.py
- src/utils.py --> utilities, particularly a function to print the player cards nicely

- src/images/bingo-icon.png --> Bingo game GUI icon
- src/images/person.jpg --> Bingo players GUI icon

----------------
HOW TO RUN

- OPTION A) Without GUI:

  mpirun -n 4 python3 Bingo-teacher.py

- OPTION B) With GUI:

  mpirun -n 4 python3 Bingo-teacher.py --gui

Note that, from the number of MPI processes specified, one will be the game master (rank 0) and the others will be players (rank > 0).

----------------
FURTHER CONSIDERATIONS

This work has been submitted to EduHPC 2022 Workshop as a Peachy Assignment.

In that submission, we incorporate a screenshot of the GUI when executing the code with 4 MPI processes through: 

  mpirun -n 4 python3 Bingo-teacher.py --gui
  
The output observed in the terminal during the execution is stored in the file EduHPC_peachy.log of this project to ease reproducilibity.
