# LimeLang

None of the features, all the fun

## Installation + Usage
- Download `lime.exe` from the releases tab
  - Optionally you can set this file location of lime.exe to your PATH
- Put the `lime.exe` file in the folder that houses you `.ll` files
- Run `lime.exe <file_name>`
  - Ex. `lime.exe test.ll`

## LimeLang Program
``test.ll``
```python
fun works() {
    # For loop
    for i = 0 to 2 {
        print("works")
    }

    # Variable Assignment
    var i = 0

    # While Loop
    while i < 2 {
        print("while")
        var i = i + 1
    }

    # Combine two lists
    var listA = [1, 2, 3]
    var listB = [4, 5, 6]
    extend(listA, listB)

    if len(listA) > 10 {
        print(10)
    } elif 1 == 2 {
        print(69)
    } else {
        print("AHA")
    }
}

works()
```

## Arithmetics
`+, -, +, /, ^`

## Types
`int, float, string, list`
- Booleans are represented as a 0 or 1

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
