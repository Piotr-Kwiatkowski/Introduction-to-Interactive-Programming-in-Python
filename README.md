# CodeskulptorSIMPLEGUI

What you can find here are the projects created for **[Introduction to Interactive Programming in Python](https://www.coursera.org/learn/interactive-python-2)**.
For online testing purposes every project is put in one .py file.

To run any of these programs you have to visit [CodeSkulptor.org](http://codeskulptor.org), paste the code delivered and then click Run or... *simply use the link placed at the beginning of every file*.

In the near future I'm planning to re-work all of these using [SimpleGUICS2Pygame](https://simpleguics2pygame.readthedocs.io/en/latest), so there would be no need for visiting CodeSkulptor (and no more global-like nonsense!), but please, be patient.

Feel free to leave any comments.
Piotr


# **Formatting tests:**


python:
```python
class Deck:
    def __init__(self):
        self.cards_list = []
        for rank in RANKS:
            for suit in SUITS:
                self.cards_list.append(Card(suit, rank))
        random.shuffle(self.cards_list)

    def shuffle(self):
        random.shuffle(self.cards_list)

    def deal_card(self):
        return self.cards_list.pop()
    
    def __str__(self):
        deck = "Deck contains: "
        for card in self.cards_list:
            deck += str(card) + " "
return deck
```


c++:
```c++
Bunny::Bunny()
{
    setNamesList();
    int randomNum = rand() % namesList.size();
    std::vector<std::string>::iterator it = namesList.begin();
    std::cout << *(it + randomNum) << std::endl;
    name = "Default";
	sex = setSex();
	age = 0;
}
```


c:
```c
void pushBackReg(PATIENT patient2Reg) 
{
	NODE *currNode = (NODE *)malloc(sizeof(NODE));
	currNode->m_Patient = patient2Reg; 
	currNode->m_nextNode = NULL;
	if (NULL == firstNode) 
  {	
		firstNode = currNode; // patient becomes first node
	}
	else 
  {
		lastNode->m_nextNode = currNode; // penultimateNode->m_nextNode = currNode
	}
	lastNode = currNode; // new patient becomes last node
	return;
}
```
