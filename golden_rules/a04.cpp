# include <iostream>
# include <string>
using namespace std;

int main() {
    int n;
    cin >> n;
    
    string result = "";
    
    int base = n;
    for (int i = 0; i < 10; i++) {
        char bit = (base & 1) ? '1' : '0';
        result = bit + result;
        base = base >> 1;
    }
    
    cout << result << endl;
}
