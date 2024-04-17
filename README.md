# LimeLang
A general purpose programming language built with Python 3.12 and LLVM.
- Statically Typed
- GenZ Interop Syntax
- JIT Compiled

## Getting Started
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