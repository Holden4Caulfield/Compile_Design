
//1
int main(){
    int a[3];
    a[0] = 1; // a[0]=1
    a[a[0]] = 2; // a[1] = 2
    a[a[a[0]]] = 3;  // a[2] = 3
    print(a[0]);
    print(a[1]);
    print(a[2]);
    return 0;
}

//2
int main() {
    int a[2][2];
    int b[3];
    b[0] = 1;
    b[1] = 1;
    a[b[1]][b[0]] = 8; // a[1][1] = 8
    int c[2][2];
    c[1][1] = 1;
    c[1][0] = 0;
    a[c[1][1]][c[1][0]] = 9; // a[1][0] = 9

    return 0;
}
