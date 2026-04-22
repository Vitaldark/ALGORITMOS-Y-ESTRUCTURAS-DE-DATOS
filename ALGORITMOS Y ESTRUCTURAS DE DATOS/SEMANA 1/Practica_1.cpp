#include <bits/stdc++.h>
using namespace std;
// --- Algoritmos de búsqueda ---
int busquedaLineal(const vector<int>& a, int x){
 for (size_t i=0;i<a.size();++i) if(a[i]==x) return (int)i;
 return -1;
}
int busquedaBinaria(const vector<int>& a, int x){
 int l=0, r=(int)a.size()-1;
 while(l<=r){
 int m = l + (r-l)/2;
 if(a[m]==x) return m;
 else if(a[m]<x) l=m+1;
 else r=m-1;
 }
 return -1;
}
int busquedaExponencial(const vector<int>& a, int x){
 if(a.empty()) return -1;
 if(a[0]==x) return 0;
 int i=1;
 while(i<(int)a.size() && a[i] < x) i<<=1; // duplica rango
 int l = i/2, r = min(i,(int)a.size()-1);
 // binaria en [l, r]
 while(l<=r){
 int m = l + (r-l)/2;
 if(a[m]==x) return m;
 else if(a[m]<x) l=m+1;
 else r=m-1;
 }
 return -1;
}
int busquedaInterpolacion(const vector<int>& a, int x){
 int low=0, high=(int)a.size()-1;
 while(low<=high && x>=a[low] && x<=a[high]){
 if(a[low]==a[high]) return (a[low]==x? low: -1);
 // posición estimada por interpolación
 long long pos = low + (long long)( (double)(high-low) * (
(double)(x-a[low]) / (double)(a[high]-a[low]) ) );
 if(pos<low || pos>high) break;
 if(a[pos]==x) return (int)pos;
 if(a[pos]<x) low=(int)pos+1; else high=(int)pos-1;
 }
 return -1;
}
// --- Utilidades de benchmarking ---
template <class F>
double medir(const vector<int>& a, const vector<int>& queries, F
buscador){
 using clk=chrono::high_resolution_clock;
 auto t0=clk::now();
 volatile long long checksum=0; // evita optimizaciones
 for(int x: queries) checksum += buscador(a,x);
 auto t1=clk::now();
 chrono::duration<double,milli> ms=t1-t0;
 // opcional: cout<<"checksum="<<checksum<<"\n";
 return ms.count()/ (double)queries.size(); // ms por búsqueda
}
int main(){
 ios::sync_with_stdio(false);
 cin.tie(nullptr);
 vector<int> ns = {10000, 100000, 500000};
 std::mt19937 rng(123);
 for(int n: ns){
 // a) uniforme ordenado
 vector<int> uni(n);
 iota(uni.begin(), uni.end(), 0); // 0..n-1
 // b) sesgado ordenado
 vector<int> ses(n);
 // 80% en [0, 0.1n), 20% en [0.1n, 5n)
 for(int i=0;i<n;i++){
 double u =
std::uniform_real_distribution<double>(0,1)(rng);
 if(u<0.8) ses[i] = std::uniform_int_distribution<int>(0,
(int)(0.1*n))(rng);
 else ses[i] =
std::uniform_int_distribution<int>((int)(0.1*n), 5*n)(rng);
 }
 sort(ses.begin(), ses.end());
 // c) desordenado
 vector<int> des = uni;
 shuffle(des.begin(), des.end(), rng);
 // queries: 1000 (70% hits, 30% miss) para cada dataset
 auto mkqueries=[&](const vector<int>& base, bool sorted){
 vector<int> q; q.reserve(1000);
 std::uniform_int_distribution<int> idx(0,
(int)base.size()-1);
 for(int i=0;i<700;i++) q.push_back(base[idx(rng)]); // hits
 for(int i=0;i<300;i++) q.push_back( (int) (10*base.size())
+ i ); // misses
 shuffle(q.begin(), q.end(), rng);
 return q;
 };
 auto q_uni = mkqueries(uni,true);
 auto q_ses = mkqueries(ses,true);
 auto q_des = mkqueries(des,false);
 auto report=[&](const string& nombre, const vector<int>& arr,
const vector<int>& q){
 cout<<"n="<<n<<", dataset="<<nombre<<"\n";
 cout<<" lineal : "<<medir(arr,q,busquedaLineal)<<" ms/busq\n";
 if(is_sorted(arr.begin(), arr.end())){
 cout<<" binaria : "<<medir(arr,q,busquedaBinaria)<<" ms/busq\n";
 cout<<" exponencial : "<<medir(arr,q,busquedaExponencial)<<" ms/busq\n";
 cout<<" interpolacion : "<<medir(arr,q,busquedaInterpolacion)<<" ms/busq\n";
 } else {
 cout<<" (datos no ordenados: usar lineal o ordenar primero)\n";
 }
 };
 report("uniforme_ordenado", uni, q_uni);
 report("sesgado_ordenado", ses, q_ses);
 report("desordenado", des, q_des);
 cout<<"-----------------------------\n";
 }
 return 0;
}
