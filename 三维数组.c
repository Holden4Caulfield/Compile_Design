//current result
//0 1
//1 2
//1 2
//2 3
int main() {
    int a[2][2][2];

    int i = 0;
    while(i < 2) {
        int j = 0;
            while(j < 2) {
                int k = 0;
                while(k < 2) {
                    a[i][j][k] = i + j + k;
                    k = k + 1;
                }
                j = j + 1;
            }
        i = i + 1;
    }
    i = 0;
    while(i < 2) {
        int j = 0;
            while(j < 2) {
                int k = 0;
                while(k < 2) {
                    print(a[i][j][k]);
                    k = k + 1;
                }
                j = j + 1;
            }
        i = i + 1;
    }


    return 0;
}
