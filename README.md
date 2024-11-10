
# PyQt Solitaire Game

This is a solitaire game built with PyQt5 for the graphical user interface. The game includes classic solitaire features such as tableau columns, stockpile, waste pile, and foundation piles. It follows the rules of standard solitaire, where cards can be moved based on alternating colors and descending order. These features are implemented with data structures such as stacks, queues etc.


## Installation

Install this game:

```bash
git clone https://gitlab.com/Mustafa-Noor/csc200m24pid17.git
cd csc200m24pid17
```
```bash
pip install pyqt5
```
    
## How To Run
Go to the address where folder clone is then on terminal:
```bash
python solitaire.py
```

## Features

- Tableau Columns: Seven tableau columns where cards can be moved according to solitaire rules (alternating colors, descending order)

- Stockpile: The top card from the stockpile is revealed and can be moved to tableau or foundation piles

- The waste pile keeps track of discarded cards and lets you continue gameplay without drawing from the stockpile.

- Foundation Piles: Four foundation piles, one for each suit, to build up from Ace to King

- Single and multiple selection movement




## Dependencies
- Python 3.7+

- PyQt5: For the graphical user interface.