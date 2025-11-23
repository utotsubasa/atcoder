# include <iostream>
# include <vector>
using namespace std;

int main() {
    int n, q;
    cin >> n >> q;
    int a;
    vector<int> sum(n+1);
    sum[0] = 0;
    for (int i = 0; i < n; i++) {
        cin >> a;
        sum[i+1] = sum[i] + a;
    }
    
    int l, r;
    for (int i = 0; i < q; i++) {
        cin >> l >> r;
        cout << sum[r] - sum[l-1] << endl;
    }
}
