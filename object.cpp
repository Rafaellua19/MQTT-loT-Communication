#include <iostream>
#include <string>

using namespace std;

/*

HELLO EVERYONE! THIS IS A SIMPLE C++ PROGRAM TO DEMONSTRATE THE CONCEPT OF OBJECTS AND CLASSES.

IF YOU THINK ABOUT THIS IS SOME KIND OF CALCULATOR, BUT INSTEAD OF CALCULATING NUMBERS, IT CALCULATES THE ENERGY LEVEL OF A DOG NAMED MAX.

IT CAN BE MORE PLAYFULL THAN A CALCULATOR, BECAUSE IT CAN BARK, EAT, REST, PLAY AND WALK. ALL THESE ACTIONS AFFECT THE ENERGY LEVEL OF MAX.

YOU CAN CUSTOMIZE THE NAME, CREATE NEW FUNCTIONS, OR EVEN CREATE NEW ANIMAL CLASSES LIKE CAT, BIRD, ETC. THE POSSIBILITIES ARE ENDLESS!

*/

class Animal {
    private:
    string name;
    int energy;

protected:
void increaseEnergy (int amount) {
energy += amount;
if (energy > 100) energy = 100;
}

void decreaseEnergy (int amount) {
energy -= amount;
if (energy < 0) { 
energy = 0;
}
}

string getName() {
return name;
}

public:

Animal(string name, int energy) {
this->name = name;
this->energy = energy;
}

void showEnergy() {
cout << name << " has energy = " << energy << endl;
}
};

class Dog : public Animal {
public:
Dog(string name, int energy) : Animal(name, energy) {}

void bark() {
cout << getName() << " says: It's wicked outside Woof!" << endl;
decreaseEnergy(80);
}

void rest() {
cout << getName() << " is resting " << endl;
increaseEnergy(20);
}

void play() {
cout << getName() << " is playing with his ball " << endl;
decreaseEnergy(15);
}

void walk() {
cout << getName() << " is walking by your side " << endl;
decreaseEnergy(20);
}
};


class Cat : public Animal {
public:
Cat(string name, int energy) : Animal(name, energy) {}

void meow() {
cout << getName() << " says: Meow!Meow! " << endl;
decreaseEnergy(5);
}

void sleep() {
cout << getName() << " is sleeping " << endl;
increaseEnergy(25);
}
};


class Bird : public Animal {
public:
Bird(string name, int energy) : Animal(name, energy) {}

void fly() {
cout << getName() << " is flying " << endl;
decreaseEnergy(20);
}

void sing() {
cout << getName() << " is singing " << endl;
decreaseEnergy(5);
}
};


int main() {

int choice;
string name;

cout << "Choose your animal: \n";
cout << "1. Dog\n2. Cat\n3. Bird\n";
cin >> choice;

cout << "Enter the name: ";
cin >> name;

if (choice == 1) {
Dog pet(name, 100);
int option;

do {
cout << "\n1. Bark\n2. Rest\n3. Play\n4. Walk\n5. Show Energy\n0. Exit\n";
cin >> option;

switch(option) {
case 1: pet.bark(); break;
case 2: pet.rest(); break;
case 3: pet.play(); break;
case 4: pet.walk(); break;
case 5: pet.showEnergy(); break;
}

} while(option != 0);
}

else if (choice == 2) {
Cat pet(name, 100);
int option;

do {
cout << "\n1. Meow\n2. Sleep\n3. Show Energy\n0. Exit\n";
cin >> option;

switch(option) {
case 1: pet.meow(); break;
case 2: pet.sleep(); break;
case 3: pet.showEnergy(); break;
}

} while(option != 0);
}

else if (choice == 3) {
Bird pet(name, 100);
int option;

do {
cout << "\n1. Fly\n2. Sing\n3. Show Energy\n0. Exit\n";
cin >> option;

switch(option) {
case 1: pet.fly(); break;
case 2: pet.sing(); break;
case 3: pet.showEnergy(); break;
}

} while(option != 0);
}
cout << "Goodbye!" << endl;

return 0;
}
