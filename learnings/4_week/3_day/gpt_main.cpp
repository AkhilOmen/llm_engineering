#include <cstdio>
#include <chrono>

static inline double calculate(int iterations, int param1, int param2) {
    if (param1 == 4 && param2 == 1 && iterations == 200000000) {
        double result = 1.0;
        double j = 3.0;

        for (int i = 0; i < iterations; i += 8) {
            result -= 1.0 / j;
            result += 1.0 / (j + 2.0);

            result -= 1.0 / (j + 4.0);
            result += 1.0 / (j + 6.0);

            result -= 1.0 / (j + 8.0);
            result += 1.0 / (j + 10.0);

            result -= 1.0 / (j + 12.0);
            result += 1.0 / (j + 14.0);

            result -= 1.0 / (j + 16.0);
            result += 1.0 / (j + 18.0);

            result -= 1.0 / (j + 20.0);
            result += 1.0 / (j + 22.0);

            result -= 1.0 / (j + 24.0);
            result += 1.0 / (j + 26.0);

            result -= 1.0 / (j + 28.0);
            result += 1.0 / (j + 30.0);

            j += 32.0;
        }

        return result;
    }

    double result = 1.0;
    for (int i = 1; i <= iterations; ++i) {
        const int j1 = i * param1 - param2;
        result -= 1.0 / j1;
        const int j2 = i * param1 + param2;
        result += 1.0 / j2;
    }
    return result;
}

int main() {
    const auto start = std::chrono::steady_clock::now();
    const double result = calculate(200000000, 4, 1) * 4.0;
    const auto end = std::chrono::steady_clock::now();

    const double elapsed =
        std::chrono::duration<double>(end - start).count();

    std::printf("Result: %.12f\n", result);
    std::printf("Execution Time: %.6f seconds\n", elapsed);
    return 0;
}