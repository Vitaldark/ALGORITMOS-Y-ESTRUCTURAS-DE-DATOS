#include <iostream>
using namespace std;
const int MAX = 100;

class Pila {
    int arr[MAX];
    int tope;
public:
    Pila() : tope(-1) {}

    void push(int val) {
        if (tope < MAX - 1)
            arr[++tope] = val;
    }

    void pop() {
        if (tope >= 0)
            tope--;
    }

    int getTope() {
        return (tope >= 0) ? arr[tope] : -1;
    }

    void mostrar() {
        cout << "Pila (tope -> base): ";
        for (int i = tope; i >= 0; i--)
            cout << arr[i] << " ";
        cout << endl;
    }
};

int main() {
    Pila p;
    int datos[] = {5, 10, 15, 20, 25};
    for (int x : datos)
        p.push(x);

    cout << "Despues de insertar:" << endl;
    p.mostrar();

    p.pop();
    p.pop();
    cout << "Despues de 2 pop:" << endl;
    p.mostrar();
    cout << "Tope actual: " << p.getTope() << endl;
    return 0;
} 