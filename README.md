# Google Books Search CLI

**Welcome to the Google Books Search CLI! 
This command line interface allows you to search for books using the Google Books API.**

**My process in crafting this program was as follows: I wrote the MVP first, 
then added classes and broke up methods to adhere to the single responsibility principle. 
Next, I added validation and error handling for various edge cases that I encountered while manually testing. 
Finally, I added testing.**

**REFACTOR~I started refactoring my program on another branch right after I submitted my first attempt for review. 
There were some things I was eager to adjust, such as:**

**1. implementing menu functionality**

**2. adding str() and repr() methods for the Book class**

**3. implementing a reading list check for books that have already been saved**

**4. exception handling for api timeouts, server errors and saving/opening/reading files.**

**These adjustments were fun but uneventful puzzles for the most part.**

**The feedback I got from Sam was informative and thoughtful. I am grateful for the book recommendation on 
Test Driven Development since it is specifically an area I am trying to improve in.** 

**The suggestion on breaking up my BookSearch class was something I had been considering and it was good to have 
clarity around this decision. This ended up being one of the more challenging aspects of my refactor. 
Breaking up the BookSearch class revealed a lot of coupling in my code. I refactored methods to make many of 
them pure functions, thereby removing side effects that created dependencies between classes. 
I then broke up BookSearch into APIFetch class and BookList class. Eventually I took Sam’s suggestion about 
making each class its own file. This helped me see how to decouple my code further. All of this resulted in me 
doing away with the BookSearch class completely.** 

**An unforeseen result of all the decoupling was a somewhat messy main function due to it now handling all the control 
flow. After cleaning this up by separating main into different functions, I came across a few bugs stemming from 
validation. I fixed these by moving the problematic validation calls to ensure that they did not take the program 
out of the main control loop.**

**As a result of following Sam’s suggestions, I have crafted a much more readable and robust program.**

## Installation

**To use the Google Books Search CLI, you will need to have Python 3 installed 
on your machine. You can check if you have Python 3 installed by running the following command in your terminal:**

```python --version```

**If you do not have the correct Python version installed, you can download it from the Python website.**

**Once you have Python 3 installed, you can install the required libraries "requests" and "JSON" 
by running the following command:**

```pip3 install requests```
**and**
```pip3 install JSON```

## Usage

**To search for books using the Google Books Search CLI, simply run the following command in your terminal:**

```python3 main.py```

**This will run the main.py file using the Python interpreter. 
The output of the program will be displayed in the terminal or command prompt window.**

**You can run the test.py file by using the following command in your terminal or command prompt:**

```python3 test.py```

**This will run the test.py file using the Python interpreter. 
The output of the tests will be displayed in the terminal or command prompt window.**

## Options

**You can search for books by terms matching the book's author, title, publisher, or subject.**

## Author

**This program was written by Rian Pickell. You can find me at: [LinkedIn](https://www.linkedin.com/in/rianpickell/)**
