# include <iostream>
# include <vector>
# include <string>
using namespace std;

int main() {
    int n, k;
    cin >> n >> k;
    
    vector<int> p(n), q(n);
    for (int i = 0; i < n; i++) {
        cin >> p[i];
    }
    for (int j = 0; j < n; j++) {
        cin >> q[j];
    }
    
    bool isYes = false;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (p[i] + q[j] == k) {
                isYes = true;
                break;
            }
        }
        if (isYes) {
            break;
        }
    }
    
    string result = isYes ? "Yes" : "No";
    cout << result << endl;
}
