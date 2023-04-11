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