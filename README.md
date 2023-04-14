# LimeLang

None of the features, all the fun

## Installation + Usage
- Download `lime.exe` from the releases tab
  - Optionally you can set this file location of lime.exe to your PATH
- Put the `lime.exe` file in the folder that houses you `.ll` files
- Run `lime.exe <file_name>`
  - Ex. `lime.exe test.ll`

## LimeLang Program
``showcase.ll``
```python
# LimeLang Showcase

# Import Statements (Horribly Implemented)
import "requests";

# Variable Assignment + Types
var a = 1
var b = 2.5
var c = "test"
var d = [1, 2, 3]
var e = {id: 0, location: "Applebees"}
var f = """
multi-line
"""

# List Methods
var element = d[0]
var listA = [1, 2, 3]
var listB = [4, 5, 6]
extend(listA, listB) # Combines listB into listA

# Dictionaries (Only one line currently supported)
var dict1 = {id: 0, firstName: "Lime", lastName: "Lang"}
var firstName = dict1["firstName"]

# For Loops
for i = 0 to 5 {
   var a = a + i  # Still need to signify the 'var' keyword for re-setting variables until implemented otherwise
}

# With 'step' (AKA how much the 'i' variable is added to after each iteration)
for i = 0 to 10 step 5 {
    print(dict1["lastName"])
}

# While Loops
var j = 0
while j < 10 {
    var j = j + 2
    print("while")

    # The 'break' and 'continue' keywords can be used in for loops too
    if j == 69 {
        continue
    }

    if j == 4 {
        break
    }
}

# Foreach Loops
var elements = [1, 2, 3, 4, 5]
foreach element in elements {
    print(element)
}

var obj = {id: 0, name: "Applebees", color: "red"}
foreach key in obj {
    print(obj[key])
}

# Function Declaration ('return' keyword is optional)
fun add(a, b) {
    return a + b
}

# Function calling
var numbers = add(5, 5)
print(numbers)

# If Statements + Conditionals
# <, >, <=, >=, ==, !=, and, or
var testValue = 1
if testValue == 1 and 15 == 15 {
    print("if condition")
} elif testValue == 2 or 10 == 69 {
    print("elif condition")
} else {
    print("else condition")
}

# Executing python code (Must only be used with multi-line strings)
# This returns back a dict with all local variables set
var pythonCode = """
def spam():
    spam_count = 0
    for i in range(5):
        print('SPAM')
        spam_count += 1
    return spam_count

spam_count = spam()
"""

var spam = exec(pythonCode)
print(spam["spam_count"])
```

## Arithmetics
`+, -, +, /, ^`

## Types
`int, float, string, list, dict`
- Booleans are represented as a 0 or 1
- Access dicts: `dictionary["key"]`
- Access lists: `list[0]`

## Built-In Functions
- `print(<value>) -> Null`
- `input() -> <str>`
- `is_number(<value>) -> <0|1>`
- `is_string(<value>) -> <0|1>`
- `is_list(<value>) -> <0|1>`
- `is_function(<value>) -> <0|1>`
- `append((<list>) -> Null`
- `pop(<list>, <index>) -> <element>`
- `extend(<listA>, <listB>) -> <0|1>`
- `len(<list>) -> <int>`
