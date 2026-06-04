#include <iostream>
#define MAX 100
using namespace std;
class Cola {
private:
  int datos[MAX];
  int frente, fin;

public:
  Cola() { 
    frente = fin = -1;
 }
  bool estaVacia() { return frente == -1; }
  bool estaLlena() { return fin == MAX - 1; }
  void encolar(int valor) {
    if (estaLlena()) {
      cout << "Cola llena\n";
      return;
    }
    if (estaVacia())
      frente = 0;
    datos[++fin] = valor;
  }
  void desencolar() {
    if (estaVacia()) {
      cout << "Cola vacía\n";
      return;
    }
    frente++;
    if (frente > fin)
      frente = fin = -1;
  }
  int frenteCola() {
    if (!estaVacia())
      return datos[frente];
    return -1;
  }
  void mostrar() {
    for (int i = frente; i <= fin; i++)
      cout << datos[i] << " ";
    cout << endl;
  }
};
int main() {
  Cola cola;
  cola.encolar(5);
  cola.encolar(15);
  cola.encolar(25);
  cola.mostrar(); // 5 15 25
  cola.desencolar();
  cola.mostrar(); // 15 25
  cout << "Frente: " << cola.frenteCola() << endl;
  return 0;
}