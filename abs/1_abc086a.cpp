# include <iostream>
using namespace std;

bool isOdd(int n) {
    return (n % 2 == 1);
}

int main() {
    int a, b;
    cin >> a >> b;

    string result;
    if(isOdd(a) && isOdd(b)) {
        result = "Odd";
    } else {
        result = "Even";
    }
    
    cout << result << endl;
}
