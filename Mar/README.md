<<<<<<< HEAD

# mar-lang
Mar  is a modern and easy-to-learn programming language designed for various applications, including database softwares and automation.
=======
Mar Programming Language



# Chapter 1 Introduction:
Welcome to the Mar programming language tutorial! This chapter will guide you through the initial steps of getting started with 
Mar. We will cover the basic introduction to the language, installation, and running your first program.


# 1.1 Introduction to Mar Programming Language:
Mar is a modern and easy-to-learn programming language designed for various applications, including database softwares and automation. 
It offers a simple syntax, powerful features, and a robust ecosystem of libraries and frameworks. 
In this section, we will explore the key features of Mar and understand why it is a great choice for your projects.


# 1.1.1 Key Features:
- Clean and intuitive syntax.
- Dynamic typing and automatic memory management.
- Built-in support for functions, classes, and modules(Awesome! No more garbage collectors).
- Extensive standard library with useful utilities(Standard library under development too).
- Strong community support from the creator and active development.


# 1.1.2 Use Cases:
- Automation: Build scripts and automate repetitive tasks.
- Prototyping: Quickly build prototypes and proof-of-concepts.
- Database Softwares: QuikDB, a DB framework on Mar can be used to make DBMS.


# 1.2 Installation
To get started with Mar, you need to install the Mar interpreter on your machine. 
Follow the steps below to install Mar:

- Clone the Mar repository from GitHub:
	$ git clone https://github.com/laradeaque/mar.git

- Change to the mar directory:
	$ cd mar

- Run the installation command:
	$ python setup.py install
	
- Verify the installation by running the following command:
	$ mar
If the installation was successful, you should see 'Hi' in Swahili from Mar. Mar prompt in under development.


# 1.3 Writing Your First Mar Program
Now that you have Mar installed, let's write a simple "Hello, world" program.
Follow the steps below to write your first program in Mar:

- Open a text editor and create a new file named hello.mar.

- In the hello.mar file, write the following code:
  	print('Hello, world!')

- Save the file and navigate to its location in the terminal.

- Run the Mar program using the following command:
	$ mar hello.mar

- You should see the output Hello, world! printed to the console.
Congratulations! You have written and executed your first Mar program.

# 1.4 Next Steps
Now that you have successfully written and executed a "Hello, world" program in Mar, you are ready to explore more 
features and concepts of the language. In the upcoming chapters, we will cover topics such as data types, variables, 
expressions, selection flow, loops, functions, classes, OOP and other additional details. Each chapter will provide 
detailed explanations and code examples to reinforce your understanding.

Feel free to experiment with the code examples and modify them to gain a deeper understanding of Mar. Happy coding!


# 1.5 Contributing
Contributions to the Mar programming language are welcome! If you find any bugs, issues, or have suggestions for 
improvements, please open an issue or submit a pull request.


# 1.6 License
This project is licensed under the MIT License. See the LICENSE file for more information.
For more details on using Mar and learning the language, refer to the chapters in this tutorial.
Enjoy coding with Mar!



# Chapter 2 Data Types and Variables
In this chapter, we will explore the different data types available in Mar and learn how to declare and assign values to variables.

# 2.1 Data Types
Mar supports the following data types:
- Number 
	The number data type represents numeric values and can be either an integer or a floating-point number.

	let x = 1
	let y = -23
	let z = 0.989

- String
	The string data type represents a sequence of characters enclosed in single or double quotes.
  
	let str = "This is a string"
	let student_name = 'Alice'
  
- Bool
	The bool data type represents boolean values, which can be either True or False.
  
	let lights_on = False
	let task_completed = True
  
- None
	The None data type represents the absence of a value.
  
	let book = None
	let car;  # Declared to have the value None
  
- Vector
	The vector data type represents an ordered collection of elements. We will discuss vectors in depth in Chapter 4.
  
	let letters = ["A", "B", "C", "D"]
	let numbers = []
  

# 2.2 Variable Declaration and Assignment
In Mar, variables are declared using the let keyword, followed by the variable name and an optional initial value.


# 2.2.1 Variable declaration example:
	
	let employee;
	
In the above example, employee is declared as a variable without an initial value. By default, the variable is 
assigned the value None.
NB : If initial value is not set then you should add a semicolon.


# 2.2.2 Variable assignment example:
Variable assignment is done using the = operator.
	
	let x = 3
	let y = 8
	let name = "Bob"
	let lights_on = false
	let car;
	
In the above example, 
    - x is assigned the value 3
    - y is assigned the value 8
    - name is assigned the string value "Bob"
    - lights_on is assigned the boolean value false 
    - car is assigned value None.


# 2.3 Variable declaration rules
Remember the following rules for variable names:
- Variable names can contain letters (a-z, A-Z), digits (0-9), and underscores (_).
- Variable names must start with a letter or an underscore.
- Variable names are case-sensitive.
- Avoid using reserved keywords as variable names (e.g., let, if, for).
- It is important to note that Mar does not require variable types to be explicitly defined. Variables in Mar are 
	dynamically typed, meaning they can hold values of any data type.
- Use snake case for variables and function names (e.g., lights_on, task_completed) not a must though.
- Use Pascal case for class names (e.g., Car, Employee) not a must though

It is important to follow consistent naming conventions to make your code more readable and maintainable.


That's it for Chapter 2! In the next chapter, we will explore selection flow and learn how to make decisions in 
Mar programs.

But before we go here is an Intermission I love motivational speaking so much that I cant hold myself back from 
sharing this with you


# 2.4 Mar Code Wisdom [Optional]
1. Embrace simplicity.
	Strive for simplicity in your code. Just as in life, simplicity leads to elegance and clarity in your programs.
2. Learn from others.
	Just as we seek advice from mentors and experienced individuals, embrace the knowledge and wisdom shared by 
	the Mar programming community. Collaborate, learn from others' experiences, and build upon existing knowledge.
3. Adapt to change.
	In the world of programming, change is inevitable. Embrace new technologies, languages, and paradigms. Stay 
	open-minded and adapt to keep your code relevant and future-proof.
4. Focus on the essentials.
	Similar to prioritizing what truly matters in life, focus on writing code that solves the core problem at hand. 
	Avoid overengineering and unnecessary complexity.
5. Seek balance.
	Balance is key in both life and coding. Strive for balance between performance and readability, efficiency and 
	maintainability. Aim for code that strikes a harmonious balance between different aspects.
6. Embrace continuous improvement.
	Just as personal growth is a lifelong journey, strive for continuous improvement in your coding skills. Learn 
	new concepts, explore different techniques, and refine your craft.
7. Practice empathy.
	Consider the needs and experiences of other developers who will read and maintain your code. Write code that 
	is easy to understand, empathizing with those who come after you.
8. Embrace diversity.
	Encourage diversity in your codebase. Different programming paradigms, approaches, and perspectives can lead 
	to more innovative and robust solutions.
9. Celebrate small victories.
	Acknowledge and appreciate the small victories in your coding journey. Whether it's solving a tricky bug or 
	implementing a new feature, take pride in your accomplishments.
10. Enjoy the process.
	Programming is not just about the end result but also about the joy of creation. Embrace the process, enjoy the 
	challenges, and find fulfillment in the act of coding itself.

... lastly this hits it right:
	- Embrace Imperfection, Nurture Growth
	In the pursuit of coding excellence, remember that perfection is an elusive concept. Embrace imperfections as 
	opportunities for growth and learning. Strive for continuous improvement, iterate, and refine your code. 
	Embrace the beauty of progress rather than seeking an unattainable perfection.


# Chapter 3: Expressions and Selection Flow Control
# 3.1 Expressions
Mar supports a wide range of operators for performing mathematical and logical operations. These operators include 
arithmetic operators `(+, -, *, /, %)`, comparison operators `(>, <, >=, <=, ==, !=)`, and logical operators 
`(&&, ||, !)`.

Expressions in Mar are formed by combining variables, literals, and operators. The operators follow the same 
precedence rules as in Python, meaning that certain operators have higher precedence and are evaluated before 
others.

# 3.2.1 Numbers
For example, you can use expressions to perform arithmetic operations:
	
	let a = 5
	let b = 3
	let c = a + b
	print(c)  # Output: 8

	let x = 10
	let y = 2
	let z = x * y - 5
	print(z)  # Output: 15
	
In this code snippet, the + operator is used to add the values of a and b, while the * operator multiplies x 
and y, and then subtracts 5.


# 3.2.2 String
Expressions can also be used for string concatenation using the + operator:
	
	let greeting = "Hello, "
	let name = "Alice"
	let message = greeting + name
	print(message)  # Output: Hello, Alice
	
In this example, the + operator concatenates the greeting and name strings to create the message string.


# 3.2.3 Bool
You can also use comparison operators to perform logical comparisons and obtain boolean results:
	
	let num1 = 10
	let num2 = 5
	let result1 = num1 > num2  # True
	let result2 = num1 == num2  # False
	let result3 = num1 != num2  # True
	print(result1, result2, result3)  # Output: True False True
	
In this code snippet, the > operator compares num1 and num2, the == operator checks for equality, and 
the != operator checks for inequality.

These are just a few examples of how expressions and operators can be used in Mar to perform calculations, 
comparisons, and string manipulations. 
Feel free to explore and experiment with different operators and expressions in your code.


# 3.3 Selection Flow
In programming, it's often necessary to make decisions based on certain conditions. Selection flow control 
allows us to choose different paths of execution based on the evaluation of conditions. 

In Mar, we use if-elif-else statements for selection flow control.
# Syntax
	
	if (<condition>){
		<code block>
	} elif (<condition>){
		<code block>
	else{
		<code block>
	}
	
# Example
In the code snippet provided, we have an example of selection flow control:
	
	let y = 5
	let x = 5

	if (x > y) {
		print(x, " > ", y)
	} elif (x == y) {
		print(x, " == ", y)
	} else {
		print(x, " < ", y)
	}
	
In this example, we compare the values of x and y using different conditions. Here's how the flow 
control works:
- The condition x > y is evaluated. Since x is not greater than y, we move to the next condition.
- The condition x == y is evaluated. Since x is equal to y, we execute the corresponding code block and 
	print 5 == 5.
- The else block is skipped because the previous condition was true.
- The output will be:
	
	5 == 5
	
Additionally, the code snippet below demonstrates the concept of truthiness in Mar. In Mar, non-zero 
numbers, non-empty strings, and non-empty vectors are considered true. Here's an example:
	
	if (y) {
		print(y)
	}
	
	Since the value of y is 5 (a non-zero number), the condition is considered true, and 5 will be printed.

Lastly, the example includes an empty vector g to demonstrate how empty values are evaluated in if statements:
	
	let g = []
	if (g) {
		print("Not Expected")
	} else {
		print("Was Expected")
	}
	
Since g is an empty vector, it is considered false in the if statement. Therefore, the code block within 
the else statement will be executed, and the output will be:
	
	Was Expected
	
Understanding selection flow control is crucial as it allows us to make decisions and execute different 
code paths based on conditions. 
It gives our programs the ability to respond dynamically to different scenarios, enhancing their flexibility 
and functionality.


# 3.4 Rules for if-elif-else block
- The condition is surrounded by parentheses (). For example: if (condition), elif (condition), else.

- The body of the if, elif, or else block is always surrounded by curly braces {}.

# Example:
	
	if (condition) {
		// Code block for if statement
	} elif (condition) {
		// Code block for elif statement
	} else {
		// Code block for else statement
	}
	
- The if statement is followed by zero or more elif statements, which can also be followed by an optional 
	else statement.
	
- The conditions in the if and elif statements are evaluated in sequential order. Once a condition evaluates 
	to true, the corresponding code block is executed, and the rest of the statements are skipped.
	
- If none of the conditions in the if and elif statements evaluate to true, the code block associated 
	with the else statement (if present) is executed.

In the next chapter, we'll explore the concept of vectors and loops in Mar programming.


# Chapter 4: Vectors and Loops
# 4.1 Vectors
In Mar, vectors are similar to Python lists and provide a way to store multiple values in a single variable. 
They have special capabilities and support various operations and functions. In this chapter, we will 
explore vectors and learn how to work with them effectively.


# 4.1.1 Defining a Vector:
	let numbers = [1, 2, 3, 4, 5]
	let fruits = ["apple", "banana", "orange"]
	

# 4.1.2 Accessing Vector Elements:
	let firstElement = numbers[0]
	let secondElement = fruits[1]
	
	
# 4.2 Vector Operations
# 4.2.1 Updating Vector Elements:
Mar does not support direct updating of vector elements by index, such as 
	
 	let numbers[1] = 3.
  	
However, there are alternative way to achieve the desired update using set() method.

Using the set() method: takes the syntax 
	
	set(<list>, <key>, <value>)
	

Takes a list and in modifies it in place
	
	set(numbers, 1, 3)
	
yields the Vector
	
	[1, 3, 3, 4, 5]
	

# 4.2.2 Iterating over a Vector:
You can iterate over a vector using a for loop and perform operations on each element. Mar follows the LIFO 
(Last-In, First-Out) principle while iterating over vectors.
   # Example:
	
	let numbers = [1, 2, 3, 4, 5]
	for (numbers: number) {
		print("Current number:", number)
	}
	
Output: 
	
	Current number: 5
	Current number: 4
	Current number: 3
	Current number: 2
	Current number: 1
	
Note that the last items was printed first.


# 4.2.3 Vector Functions:
Mar provides a variety of vector functions that can be used to manipulate and analyze vectors. These 
functions include *length()*, *append()*, *remove()* and *insert()*. They operate on vectors and modify them 
accordingly.
   # Example:
	
	let numbers = [3, 1, 4, 2, 5]
	print("Original numbers:", numbers)

	let len = length(numbers)
	print("Length of list of numbers:", len)

	numbers.append(6)
	print("Updated numbers:", numbers)

	numbers.remove(0)
	print("Updated numbers:", numbers)

	numbers.insert(0, 3)
	print("Updated numbers:", numbers)
	
By utilizing these vector methods and functions, you can efficiently update and manipulate vectors in Mar.
Vectors are powerful data structures that allow you to work with collections of values effectively.


# 4.3 Loops
Loops are an essential part of programming, allowing you to repeat a block of code multiple times. 
In Mar, you can use two types of loops: while and for loops. In this chapter, we will explore how to 
use loops effectively in Mar.


# 4.3.1 While Loops:
A while loop repeats a block of code as long as a specified condition is true. Let's look at some 
examples:
   # Example 1 - Basic While loop:
	
	let counter = 0

	while (counter < 5) {
		print("Counter: ", int(counter))
		let counter = counter + 1
	}
	
In the above code, the while loop will continue to execute the block of code as long as the counter 
variable is less than 5. The counter variable is incremented by 1 in each iteration.

   # Example 2 - Using break:
	
	let counter = 0

	while (counter < 5) {
		print("Counter: ", int(counter))
		let counter = counter + 1
		if (counter == 2) {
			break
		}
	}
	
In this example, the break statement is used to exit the loop when the counter variable reaches the 
value 2. This causes the loop to terminate prematurely.

   # Example 3 - Using continue:
	
	let counter = 0

	while (counter < 5) {
		if (counter == 2) {
			continue
		}
		print("Counter: ", int(counter))
		let counter = counter + 1
	}
	
Here, the continue statement is used to skip the iteration when the counter variable equals 2. This 
means that the print statement is not executed when the counter is 2.


# 4.3.2 For Loops:
A for loop is used to iterate over a collection of values, such as a vector, and execute a block of 
code for each element in the collection. They are used for iterating Vectors only or an iterable object
   # Basic syntax: 
	
	for(<iterable>: <loop, variable>) {
		<block>
	}
	
Let's see an example:
   # Example:
	
	let numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

	for (numbers: number) {
		print("number -> ", number)
	}
	
In this example, the for loop iterates over the numbers vector, assigning each element to the number 
variable. The block of code inside the loop is executed for each element in the vector.

Loops are powerful tools for automating repetitive tasks and iterating over data collections in your 
programs.


# Chapter 6: Functions
Functions are a fundamental concept in programming that allow you to organize and reuse code. They 
enable you to encapsulate a block of code that performs a specific task and can be called multiple 
times throughout your program. In Mar, you can define functions using the func keyword. 
There are two types of functions:
- Builtin functions
- Custom user-defined functions
	
# 6.1 BuiltIn Functions
They are functions that are avaliable to the developer from the Mar interpreter. They include
	`
 	print
  	`
	- Used to print a line to the console.
	- If the objects being printed are of different type you should use `,` to separate them else you.
		can use `+` to concatenate strings
	
	`
 	int
  	`
	- Converts a number to an int
	
	`
 	readline
  	`
	- Takes an input from the user.

	`
 	sysprint
  	`
	- Same as print but used in the system libraries. It is under development but will be used to print 
		system information asked as parameter
		`sysprint(__scope__)` - Print all variables and their values in the current scope
	
	`
 	length
  	`
	- Returns the length of a Vector

	`
 	set
  	`
	- Used to update values of a Vectors at a certain key

6.2 User-defined Functions
6.2.1 Function Syntax:
The basic syntax for defining a function in Mar is as follows:
There are two types of functions: 
   -``Basic Function`` 
   - ``Smart Return Functions``
	
# a) Basic Functions Syntax
Recieve some parameter, do operation and return some expression
	
	func function_name(formal_parameters) {
		// Function body
		// Code to be executed
		return expression;
	}
	
# b) Smart Return Functions Syntax
In smart return functions, the output_parameters section defines the expected output of the function. 
The Mar interpreter will keep track of the variable specified in the output_parameters and 
automatically return its value when necessary.
	
	func function_name(formal_parameters: output_parameters) {
		// Function body
		// Code to be executed
	}
	
The colon is optional if there is no return to be made.
Let's go through some examples to understand how functions work in Mar:


# 6.2.2 Basic Function
This are functions that are similar to any programming  language i.e. takes in parameters 
does some internal processing then returns some value.
   # Example
	
	func sum(a, b) {
		let c = a + b;
		return c;
	}
	
In this example, we define a function named sum that takes two parameters, a and b. It computes 
the sum of a and b and assigns the result to the local variable c. 
The function then returns the value of c.


# 6.3 Smart Return Functions
This is a feature in Mar functions. To explain further lets see an example:
	
	func set_name(name: name) (
	}
	
	let username = set_name("Alice")
	
This example demonstrates a function with a "smart return" feature. The setName function does not 
explicitly return a value. However, since the function is expected to return a value as there is an 
output parameter specified, the Mar interpreter keeps track of the variable ``name`` to return and 
automatically returns it. This takes no extra cost in terms of time and space.

Another example using updated version of the sum function we created using basic function syntax:
	
	func sum(a,b: (a+b)) {}
	
	let x = 5
	let y = 5
	
	let z = sum(x, y)
	
	print(z) #: Output is 10
	
	
In this updated version, the function sum takes two parameters, a and b. The sum of a and b 
is now specified as the output parameter (a + b). The Mar interpreter will keep track of the 
computed value and automatically return it when the function is called.

The smart return feature enhances code readability and reduces the need for explicit return 
statements in cases where the output parameter can be directly computed within the function's body.

NB: *If a return statement is found in a function then the interpreter returns it and the smart 
	feature is overridden.*	
    *Remember to include the semicolon at the end of the return statement to indicate the end 
	of the line. Else an syntax error is raised.*

By utilizing the smart return feature, you can write more concise code and let the Mar interpreter 
handle the return value efficiently.

# Example 3: Function with Conditional Return Statements
	
	func check(age: category) {
		let category;
		if (age < 16) {
			let category = 'Highschool Kid'
		} elif (age < 20) {
			let category = 'College Teen'
		} elif (age < 25) {
			let category = 'Young Graduant'
		} else {
			let category = 'Older'
		}
	}
	
	let cat = check(17)
	print(cat) #: College Teen
	
	let cat = check(35)
	print(cat) #: Older
	
In this example, the check function takes an age parameter and returns a category based on the 
age value. The function uses conditional statements (if, elif, and else) to determine the 
appropriate category and returns the corresponding value using smart return.


# 6.4 Final Note:
In this chapter, we explored functions in Mar. We learned about the syntax for defining 
functions and how to use parameters and return values. We discussed the smart return 
feature, which automatically returns the expected value if no explicit return statement 
is present. Additionally, we saw an example of a function with conditional return statements. 
Functions are essential for code organization, reusability, and modular programming. 
They allow you to encapsulate logic and perform specific tasks within your programs.

Exercise more on working with Smart return functions to increase readability and let the 
Mar interpreter handle the return value efficiently.


# Chapter 7: Classes
In Mar, classes are used to define custom data types and encapsulate related data and 
behavior into objects. Objects are instances of a class, and they can have their own 
unique data and methods.
Let's explore the code below to understand how classes work in Mar:

# 7.1 Employee class
	
	class Employee {
		func Employee(me, name, age:) {
			let me.name = name
			let me.age = age
			# Causes error since this object is not yet declared
			# me is not defined
			# me.display()
		}
		
		func display(me) {
			print("Employee Name: ", me.name)
			print("Employee Age: ", int(me.age))
		}
	}

	let employee = Employee("Alice", 21)
	employee.display()
	
In this code, we define a class called Employee with a constructor method Employee. The 
constructor is called automatically when an object of the class is created. 
It initializes the object's name and age attributes.

Constructor method in Mar is a single function that has the same name as the class name 
it is executed when an instance of the class is created.

We then create an object employee of the Employee class with the name "Alice" and age 21. 
We can call the display method on the employee object to print out the employee's name and age.

We cannot call any class method in the constructor as the object is not yet completely constructed.
Thus calling ``me.display()`` will cause the error ``me.display() is not declared``

``me`` is used in Mar as the self reference in class method. The first parameter for any class 
should be ``me`` to provide the details or features and attributes of the class. It acts as a connection

# 7.2  Student class
	
	class Student {
		func Student(me, name, cls, age, adm_no) {
			let me.name = name
			let me.cls = cls
			let me.age = age
			let me.adm_no = adm_no
		}
		
		func show_etails(me) {
			print()
			print("Student Name: ", me.name)
			print("Student Class: ", me.cls)
			print("Student Age: ", int(me.age))
			print("Admission Number: ", int(me.adm_no))
			print()
		}
		
		func set_marks(me, maths, eng, kisw, sci, sscre) {
			# cannot return directly me.marks as it has not been interpreted
			let me.marks = [maths, eng, kisw, sci, sscre]
		}
		
		func get_total_marks(me : total_marks) {
			let total_marks = 0
			for(me.marks : mark) {
				let total_marks = total_marks + mark
			}
			return total_marks;
		}
		
		func update_detail(me, field, change : change_commited) {
			if (field == "name") {
				let me.name = change
			} elif (field == "cls") {
				let me.cls = change
			} elif (field == "age") {
				let me.age = change
			} elif (field == "adm_no") {
				let me.adm_no = change
			} else {
				return False;
			}
			
			return True;
		}
	} 

	let student = Student("Alice", "A", 24, 1234)
	student.show_details()

	student.set_marks(87, 52, 67, 69, 82)
	let total = student.get_total_marks()
	let mean = total / 5

	print("Student Name: ", student.name)
	print("Total Marks : ", total)
	print("Mean Points : ", mean)


	if (student.update_detail("age", student.age + 1)) {
		student.show_details()
	} else {
		print("Ooops! No change was made")
	}
	

In this code, we define a class called Student. The Student class has several methods, including 
``show_details()``, ``set_marks``, ``get_total_marks``, and ``update_detail``. Each method takes 
a parameter me that represents the instance of the class.

We create an object student of the Student class with the specified attributes: name, class, 
age, and admission number. We can call the ``show_details()`` method on the student object to 
print out the student's details.

The ``set_marks`` method sets the marks attribute of the student object. The ``get_total_marks`` 
method calculates and returns the total marks based on the marks attribute. The ``update_detail`` 
method allows us to update specific attributes of the student object.

Lastly, we calculate the mean points. The update age of the student object is printed if the 
age update is successful.


# 7.3 Automatic Memory Management
The execution of any function involves the manipulation of some data to create some output. This 
now necessitates the need of using variables. These variables require some space to be stored
on the memory. If the variables are let to just occupy to continue to exist even after they are 
out of scope or they are not needed we could end up running out of memory. also we can get wrong 
variables when we access a certain variable not available in the current scope thus generating 
undesired results

In Mar, to avoid such situations function call are accompanied by three function execution. Note 
these are executed by the interpreter internally.
	1. `clean_up`
		- Removes formal paremeters from the current scope since they are passed after argument
			passing
		- This ensures all parameters are removed from the current scope in memory.
		
	2. `clean_scope`
		- Before returning control to parent function we need to remove all local variables that 
			were declared in the function
		- The only exception is that the class attributes are not removed as me is not defined in 
			the function
		
	3.  `destroy_current_scope`
		- When a function calls a function internally we need to create a new scope for the function 
			to use. After finishing execution we need to remove the new scope that was created from s
			current scope and set parent scope as the current scope. The new scope of the function that 
			just finished execution needs to be destroyed, since it is of no need.
			
	Now from that you can think how these three functions are called: Order of execution.
		`clean_up`
		`destroy_current_scope`
		*reseting current scope to parent scope*
		`clean_scope`	


# 7.4 Garbage Collection
Since Mar is an Object Oriented Programming Language, It thus follow there is creation and use of 
instances or objects. The objects reside in the heap area of the memory and it can get messy if the 
area is not correctly managed. A garbage collector is used to manage the heap section. 

Suprisingly, Mar does not use a garbage collector to manage objects it uses a simple procedure to 
regulate the objects in memory.

Once a class it is defined, it is stored in a Python dict, with the key as class name and the value
as the body which is also a dict with key as class methods name and the value as a tuple of method 
parameters and class method body. The last key-item in the body is an important pair. It is:
`1: [parent classes]` It shall be discussed in the next chapter. 

When we want to create an object Mar now just creates a dict with the following:

	
	{'me': {}, '::type':[], '::alias': None, 1: []}
	
The `me` is used to hold all class attributes/features. The `::type` is a list that states the 
classes which the object will be made up of. These is important for the inheritance(discussed 
in the next chapter). The list will help us when searching for object methods. The first element 
is the Base type of which we are creating the object of. `::alias` is used has a value if the 
class being used is an aliased name this is incase of importing classes(Importing is discussed 
in chapter 9)

With that we can conclude that since the object carries the type we do not need to write a 
garbage collector as the object is not carrying any method with it.

# 8.5 Final Note
Classes in Mar provide a way to define and organize related data and behavior, allowing for code 
reusability and encapsulation. You can create multiple objects from a class, each with its own 
unique data and behavior.



# Chapter 9: Inheritance
In Mar, classes can inherit attributes and methods from other classes through inheritance. 
Inheritance allows for code reuse and the creation of class hierarchies. In this chapter, we'll 
explore how inheritance works in Mar.
Let's consider the code below to understand inheritance:


# 9.1 Example 1
	
	class Worker {
		func Worker(me, company:) {
			let me.company = company
		}
		
		func work(me, post:) {
			print("Employee Post  : " + post)
		}
	}

	class Labour {
		func Labour(me) {
			# pass
		}
		
		func manual_work(me, post:) {
			print("Name: " + me.name)
			print("Post: " + post)
		}
	}

	class Employee(Worker, Labour) {
		func Employee(me, name, id, age, company) {
			parent Worker(company)
			let me.name = name
			let me.id = id
			let me.age = age
		}
		
		func details(me) {
			print("Employee Name  : ", me.name)
			print("Employee ID No : ", me.id)
			print("Employee Age   : ", int(me.age))
			print("Employee At    : ", me.company)
		}
	}

	let employee = Employee("Alice", "CFEX132", 24, "ABC Limited")

	print()
	employee.details()
	employee.work("Secretary")
	print()
	
	
In this code, we have three classes: Worker, Labour, and Employee.

The Worker class has a constructor method that initializes the company attribute and a work 
method that takes a post parameter and prints the employee's post. The Labour class has a 
constructor method and a labour method that takes a post parameter and prints the name and 
post of the labour.

The Employee class inherits from both the Worker and Labour classes by adding the class 
names of parent class to the parent class list. The list is used to define the type of an 
object i.e. an object of a subclass has its type as the subclass and parent class(es). This 
list also is used during importation of a class. If we are importing a class, which has some 
atttributes and features from the parent class, we need to have the parent class also loaded. 
Thus the interpreter shall load the classes loaded in this list. The last reason is to increase
code readability as we can see directly the parent classes of a class.

The classes in parent class list are not executed automatically when we are creating an instance
using the subclass we must explicitly tell the interpreter to execute the class by:
	
	`
 parent *ParentClassName* ( *args* `)
	`
	e.g.
	`
 parent Worker(company)
 `


The keyword parent is used to invoke the constructor method of the parent class. It allows the 
child class to inherit and initialize the attributes defined in the parent class. e.g. The 
`company` attribute is set in the Employee class


# 9.2 Example 2
	class Shape {
	    func Shape(me, name) {
	        let me.name = name
	    }
	    
	    func find_area(me) {
	        print(me.name, " -- Finding Area")
	    }
	} 
	
	class Circle(Shape) {
	    func Circle(me) {
	        parent Shape("Circle")
	    }
	} 
	
	class Square(Shape) {
	    func Square(me) {
	       #: parent Shape("Square")
	    }
	} 
	
	let circle = Circle()
	circle.find_area()
	
	let square = Square()
	square.find_area() #: cause error as parent is not invoked

In this example, we have three classes: Shape and their child classes Circle and Square. 
The Shape class is a base class that serves as a common parent for all figures. It has the 
method `find_Area()` defined, but it is used to establish a hierarchical relationship.

The Circle class inherits from Shape classes. Since it invokes parent class using 
	`
	parent Shape("Circle") 
	`
in its constructor, the parent constructor is executed. This initializes the name attribute 
of the Circle object with the value "Circle". Therefore, when `find_area()` is called on a Circle 
object, it prints "Circle -- Finding Area".

The Square class inherits from the Shape class. It does not invokes the parent constructor hence 
the attribute is not set and `find_area()` is also not inherited in Square Class. Thus, 
`square.find_area()` causes an error `find_area() not defined on object square`.

Finally, we create instances of Circle and Square classes, and call the `find_area()` method on 
each object. 

This demonstrates how the child classes inherit and utilize the attributes and methods defined 
in their parent classes.


# 9.3 Final Note
By using parent, you can access and utilize the functionality and attributes defined in the parent 
class within the child class. It helps in creating a hierarchical relationship between classes and 
enables code reuse and modularity.

Inheritance in Mar provides a powerful mechanism for code reuse and the creation of class 
hierarchies, enabling you to build complex systems with structured and organized code.



# Chapter 9: Others
# 9.1 Import
Takes the syntax:

`
from parent_module use module as alias
`

Note `as` is not working properly **so do not use it for this version(we are working on it)**

Here's an example to illustrate the usage of the import statement:
	
	from math use pi, pow

	let radius = 5
	let area = pi * pow(radius, 2)

	print("The area of the circle is: ", area)
	
	
In this example, we import the math module using the from keyword, and we assign it an alias m 
using the as keyword. This allows us to refer to the functions and constants from the math module 
using the m alias.

We then calculate the area of a circle by using the pi constant and the pow() function from the 
math module, which are accessed through the m alias. The calculated area is stored in the area 
variable.

Finally, we print the calculated area using the print() function.

**Note: The current version of Mar import is many having problems in the following areas: (we are working on them)
- Currently use can:
	- Get module, classes, functions, variables, file from the Mar Library COMFORTABLY.
	- Get module, classes, functions, variables, file from only one sub directory, 
		e.g. utils/functions.mar or helper/variables.mar
		
ELSE THE USE STATEMENT WILL RAISE AN ERROR
.**


# 9.2 Mar Libraries
As Mar continues to develop, its libraries continue to advance. The only module written in 
Mar is `sys`:

`sys` module
The sys module provides some useful functions to inspect the current scope, classes, and 
functions. 

Here's an example of how you can use the sys module and its functions:
	
	from sys use memoryview

	let x = 10
	let y = "Hello"
	let z = True

	memoryview()  # Prints the variables in the current scope
	
Output
	
	{s: {...}, x:10, y: 'Hello', z: True}
	
	
The memoryview() function from the sys module will print the variables in the current scope. 
In this example, it will display the variables s, x, y, and z along with their corresponding 
values.

Other functions in sys module are:
1. **heapview()**
Prints classes that are defined in the program
# Example
	from sys use heapview

	class MyClass {
		func my_function(me) {
			s.stackview()  # Prints the stack trace of function calls
		}
	}

	heapview()  # Prints the classes defined
	
# Output
	`
	{'MyClass': {'my_function': (([me], []), [('call', ('.', 's', 'stackview'), [])])}}
	`
	
2. **stackview()**
Prints the stack trace of function calls
	
	from sys use stackview
	
	func c() {
		stackview()
	}
	func b() {
		c()
	}
	func a() {
		b()
	}
	func main() {
		a()
	}
	main()
 # Output
	[main, a, b, c, stackview]

By utilizing the sys module and its functions, you can gain insights into the variables, classes, and function calls within your Mar programs.
Finally Mar is under active development and things are going to change rapidly as i handle more functionalites in Mar

Language creator: **Arnold Kamau Ngaruiya**
Version: **Mar 0.0.1**
>>>>>>> 8d1fa30 (Initial Commit)
