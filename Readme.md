# LANG 27

## The language supports:

- Basic Syntax (e.g., ```variables, functions```)
- Data Types (e.g., ```integers, strings, character, boolean, float```)
- Operators (```+, -, *, /, =``` for assignment)
- Control Flow (e.g., ```if-else, for loop```)
- Inbuilt Function (e.g., ```Lenght, To number```)
- Output/Input (e.g., ```drucken, eingabe```)
- Function Declaration (e.g., ```func```)


## Example code:
```py
## Basic variable declarations with different types
num x = 10
str greeting = "Hello, World!"
dec pi = 3.14159
chr firstLetter = 'A'
bool isTrue = true

## Simple printing
drucken("Welcome to the 'LIP' Language Test!")
drucken(greeting)
drucken("The value of x is:")
drucken(x)
drucken("Pi is approximately:")
drucken(pi)
drucken("First letter is:")
drucken(firstLetter)
drucken("Boolean value:")
drucken(isTrue)

## Mathematical operations
num a = 5
num b = 3
drucken("Addition: 5 + 3 =")
drucken(a + b)
drucken("Subtraction: 5 - 3 =")
drucken(a - b)
drucken("Multiplication: 5 * 3 =")
drucken(a * b)
drucken("Division: 5 / 3 =")
drucken(a / b)

## Decimal operations
dec c = 5.5
dec d = 2.5
drucken("Decimal addition: 5.5 + 2.5 =")
drucken(c + d)
drucken("Decimal division: 5.5 / 2.5 =")
drucken(c / d)

## String operations
str firstname = "John"
str lastname = "Doe"
str fullname = firstname + " " + lastname
drucken("Concatenated string:")
drucken(fullname)

## Length function
drucken("Length of fullname:")
drucken(len(fullname))

## Comparison operators
drucken("Comparisons:")
drucken("5 == 3:")
drucken(a == b)
drucken("5 != 3:")
drucken(a != b)
drucken("5 > 3:")
drucken(a > b)
drucken("5 < 3:")
drucken(a < b)
drucken("5 >= 3:")
drucken(a >= b)
drucken("5 <= 3:")
drucken(a <= b)

## If-else statements
drucken("Testing if-else:")
if (a > b) {
    drucken("a is greater than b")
} el {
    drucken("a is not greater than b")
}

## Nested if statements
if (a > 0) {
    if (b > 0) {
        drucken("Both a and b are positive")
    } el {
        drucken("a is positive, b is not")
    }
} el {
    drucken("a is not positive")
}

## For loop
drucken("For loop counting from 1 to 5:")
num i = 1
for (i = 1; i <= 5; i = i + 1) {
    drucken(i)
}

## Prompt for user input with type conversion
drucken("Testing user input:")
num userNumber = eingabe("Enter a number: ", num )
drucken("You entered:")
drucken(userNumber)

str userString = eingabe("Enter your name: ", str)
drucken("Hello, " + userString + "!")

## Function definition and call
func add(a, b) {
    return a + b
}

drucken("Function call result - add(10, 20):")
drucken(add(10, 20))

## Function with calculations
func calculateAverage(num1, num2, num3) {
    dec sum = num1 + num2 + num3
    dec average = sum / 3
    return average
}

drucken("Average of 10, 20, 30:")
drucken(calculateAverage(10, 20, 30))

## Function with conditional logic
func max(a, b) {
    if (a > b) {
        return a
    } el {
        return b
    }
}

drucken("Maximum of 42 and 17:")
drucken(max(42, 17))

## More complex function with loops
func factorial(n) {
    num result = 1
    num i = 1
    for (i = 1; i <= n; i = i + 1) {
        result = result * i
    }
    return result
}

drucken("Factorial of 5:")
drucken(factorial(5))

## Type conversion function
drucken("Type conversion:")
str numberStr = "42"
num convertedNum = to_num(numberStr)
drucken("Converted string '42' to number:")
drucken(convertedNum)
drucken("Adding 8 to the converted number:")
drucken(convertedNum + 8)

## Nested function calls
drucken("Nested function calls:")
drucken(add(factorial(3), max(5, 10)))

## Final message
drucken("All tests completed!")
```