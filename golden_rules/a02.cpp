# include <iostream>
# include <string>
using namespace std;

int main() {
    int n, x;
    cin >> n >> x;
    
    string result = "No";
    int a;
    for(int i = 0; i < n; i++){
        cin >> a;
        if(a == x) {
            result = "Yes";
            break;
        }
    }
    
    cout << result << endl;
}
