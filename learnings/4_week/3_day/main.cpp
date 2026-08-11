
#include <bits/stdc++.h>
using namespace std;

// Linear congruential generator step: state = (a * state + c) mod 2^32
static inline uint32_t lcg_next(uint32_t &state) {
    state = (static_cast<uint64_t>(1664525u) * state + 1013904223u);
    return state;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    const int n = 10000;
    const uint32_t initial_seed = 42;
    const int min_val = -10;
    const int max_val = 10;
    const int range = max_val - min_val + 1; // 21

    long long total_sum = 0;

    auto start = chrono::high_resolution_clock::now();

    uint32_t outer_state = initial_seed;
    vector<int> arr(n);
    for (int run = 0; run < 20; ++run) {
        // Obtain seed for this run
        uint32_t seed = lcg_next(outer_state);
        uint32_t state = seed;

        // Generate the random numbers
        for (int i = 0; i < n; ++i) {
            uint32_t v = lcg_next(state);
            arr[i] = static_cast<int>(v % range) + min_val;
        }

        // Kadane's algorithm for maximum subarray sum
        long long max_ending = arr[0];
        long long max_sum = arr[0];
        for (int i = 1; i < n; ++i) {
            long long x = arr[i];
            long long cand = max_ending + x;
            max_ending = (x > cand) ? x : cand;
            if (max_ending > max_sum) max_sum = max_ending;
        }

        total_sum += max_sum;
    }

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;

    cout << "Total Maximum Subarray Sum (20 runs): " << total_sum << "\n";
    cout << "Execution Time: " << fixed << setprecision(6) << elapsed.count() << " seconds\n";

    return 0;
}
