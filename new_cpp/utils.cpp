#include <math.h>

double modrem(double a, double N){
    return a - N * floor(a / N);
}