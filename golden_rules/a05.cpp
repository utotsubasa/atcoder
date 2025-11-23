# include <iostream>
using namespace std;

int main() {
    int n, k;
    cin >> n >> k;
    
    int result = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            int rem = k - i - j;
            if (rem >= 1 && rem <= n) {
                result++;
            }
        }
    }
    
    cout << result << endl;
}
