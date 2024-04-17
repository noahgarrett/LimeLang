# LimeLang
A general purpose programming language built with Python 3.12 and LLVM.
- Statically Typed
- GenZ Interop Syntax
- JIT Compiled

## Getting Started (Pre-Built)
1. Download the latest `lime.exe` file from the **Releases** section.
2. Place somewhere you will remember on your PC
    - *An installer application is under development to handle this part for you*
3. Copy the path to the `lime.exe` file
    - For example:
        - Save the `lime.exe` file to `C:\Users\noahw\Desktop\Lime`
        - Copy the path `C:\Users\noahw\Desktop\Lime` **NOT** `C:\Users\noahw\Desktop\Lime\lime.exe`
4. Add the copied path to your system `PATH` environment variables
    - [Windows](https://www.mathworks.com/matlabcentral/answers/94933-how-do-i-edit-my-system-path-in-windows)
    - [Mac + Linux](https://gist.github.com/nex3/c395b2f8fd4b02068be37c961301caa7)
5. Open a brand new terminal, and you should now be able to use the `lime` command
6. Create a new folder and create a new file named `main.lime`
7. Add the `main` function to your `main.lime` file. This is required for all lime programs.
```cpp
fn main() -> int {

    printf("I dropped my limes :(");

    return 0;
}
```
8. Compile/Run your lime program with `lime main.lime`

## Getting Started (Source)
1. Fork/Clone this repository to your machine.
2. Initialize a new `Anaconda` or `Miniconda` environment in the repository location
    - `conda create --name limelang python=3.12`
3. Activate the environment
    - `conda activate limelang`
4. Install the required dependencies
    - `conda install llvmlite`
    - `pip install pyinstaller`
5. Build the executable
    - `pyinstaller --onefile --name lime --icon=assets/lime_icon.ico main.py`
6. Add the `dist` folder to your system PATH environment variables
    - `..\..\limelang\dist` (your path will be similar)
7. Follow the rest of the instructions shown above for using the pre-built exe

## Benchmarks
These are just crude and very specific benchmarks comparing vs LimeLang

### Fibonacci
Limelang proves to be **~31.87x** speedup when compared to Python
- LimeLang (**10.020018 ms**)
- Python (**319.3933 ms**)
```cpp
fn fib(n: int) -> int {
    if n == 1 {
        return 0;
    }

    if n == 2 {
        return 1;
    }

    return fib(n - 1) + fib(n - 2);
}

fn main() -> int {
    return fib(32);
}
```

## Features
All current features are subject to change as this language is still in the **Alpha** stages.

### Value Types
- Strings (`str`)
- 32-bit Integers (`int`)
- Floats (`float`)
- Void (`void`)
- Bool (`bool`)

### Arithmetic Operators
- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division
- `^` Power/Exponent
- `%` Modulus

### Comparison Operators
- `<`   Less-Than
- `<=`  Less-Than Equal-To
- `>`   Greater-Than
- `>=`  Greater-Than Equal-To
- `!=`  Not-Equal
- `==`  Equal-To

### Assignment Operators
- `=`   Equals
- `+=`  Plus-Equals
- `-=`  Minus-Equals
- `*=`  Multiply-Equals
- `/=`  Divide-Equals

### Prefix Operators
- `!`   Not
- `-`   Negative

### Postfix Operators
- `++`  Increment
- `--`  Decrement

### Reserved Keywords -> GenZ Interop
- `let`         -> `lit`        Mutable Variable Declaration
- `fn`          -> `bruh`       Function Declaration
- `return`      -> `pause`      Return Statement
- `if`          -> `sus`        If Statement
- `else`        -> `imposter`   Else Statement
- `true`        -> `nocap`      True Boolean
- `false`       -> `cap`        False Boolean
- `while`       -> `wee`        While Loop
- `break`       -> `yeet`       Break Statement
- `continue`    -> `anothaone`  Continue Statement
- `for`         -> `dab`        For Loop
- `import`      -> `gib`        Import Statement

### Symbols -> GenZ Interop
- `=`   -> `be`     Equals
- `;`   -> `rn`     Semi-Colon
- `:`   -> `:`      Colon
- `->`  -> `->`     Arrow
- `(`   -> `(`      Left-Paren
- `)`   -> `)`      Right-Paren
- `{`   -> `{`      Left-Brace
- `}`   -> `}`      Right-Brace

### Built-In Functions
- `printf` C-Like format print to console function
    - `printf("Format ints: %i", 12);`

### Function Declaration + Usage
```cpp
fn add(a: int, b: int) -> int {
    return a + b;
}

fn main() -> int {
    return add(1, 2);
}
```

### Variable Delclaration + Usage
```cpp
fn main() -> int {
    let a: int = 14;

    return a + 6;
}
```

### If Statement Declaration + Usage
```cpp
fn main() -> int {
    let a: int = 5;

    if a == 5 {
        return 14;
    } else {
        return 0;
    }
}
```

### While Loop Delcaration + Usage
```cpp
fn main() -> int {
    let a: int = 0;

    while a < 10 {
        printf("a = %i", a);
        a++;
    }

    return a;
}
```

### For Loop Delcaration + Usage
```cpp
fn main() -> int {
    
    for (let i = 0; i < 10; i++) {
        printf("i = %i", i);
    }

    return 8;
}
```

### All Value Types
```cpp
fn test() -> void {
    printf("called from test()");
}

fn main() -> int {
    let a: int = 2;
    let b: float = 2.22;
    let c: str = "limes";
    let d: bool = true;

    test();

    return 5;
}
```