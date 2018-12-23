
//factorial
int fun(int n) {
    int f;
    if (n == 1) {
        f=1;
    }
    else {
        f = fun(n-1) * n;
    }
    return f;
}

//add function
int add(int x, int y) {
    return x + y;
}

int main() {
    int a = 4;
    int b = 5;
    int z = add(fun(a), fun(b));//4!+5!=90H
    print(z);
    return 0;
}