//Fibonacci
int Fibon(int n) {
    if (n <= 2) {
        return 1;
    }
    else {
        return Fibon(n - 1) + Fibon(n - 2);
    }
}

int main() {
    int n = 6;
    int ret = Fibon(n);
    print(ret);//8
    return 0;
}