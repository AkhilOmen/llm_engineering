from utils.llm_utils.ollama_utils import OLLAMA_MODEL, create_ollama_client
from utils.llm_utils.openai_utils import create_openai_client
from utils.system_info import retrieve_system_info

OPENAPI_MODEL = "gpt-5.6-luna"
MAIN_MODEL = OLLAMA_MODEL


def get_cpp_compiler(system_info):
    user_message = f"""
    Here is a report of system information for my computer.
    I want to run a C++ compiler to compile a single C++ file called gpt_main.cpp and then execute it in simple way 
    possible.
    Please reply with whether I want to install any C++ compiler to do this. If so, please provide the simplest step by 
    step instructions to do so.
    
    If I'm already set to compile C++ code, then I'd like to run something like this in Python to compile and execute 
    the code.
    ```python
    compile_command = # something here
    compile_results = subprocess.run(compile_command, check=True, text=True, capture_output=True)
    run_command = # something here
    run_results = subprocess.run(run_command, check=True, text=True, capture_output=True)
    return run.stdout
    ```
    
    Please tell me exactly what I should use for the compile_command and run_command.
    
    System_information:
    {system_info} 
    """

    # openai = create_openai_client()
    # messages = [{"role": "user", "content": user_message}]
    # response = openai.chat.completions.create(
    #     model=OPENAPI_MODEL,
    #     messages=[{"role": "user", "content": user_message}]
    # )


    ollama_client = create_ollama_client()
    messages = [{"role": "user", "content": user_message}]
    response = ollama_client.chat.completions.create(
        model=MAIN_MODEL,
        messages=messages
    )
    results = response.choices[0].message.content
    print(results)


def convert_python_to_cpp(system_info, python_code):
    # compile_command = ["clang++", "-std=c++20", "gpt_main.cpp", "-o", "main"]
    compile_command = ["clang++", "-std=c++20", "-Wall", "-Wextra", "-O2", "gpt_main.cpp", "-o", "main"]
    run_command = ["./main"]

    system_prompt = """
    Your task it to convert python code into high performance C++ code
    Respond only with C++ code. Do not provide any explanation other than occasional comments
    The C++ response needs to produce an identical output in the fastest possible time.
    """

    user_prompt = f"""
    Port this Python code to C++ with the fastest possible implementation that produces identical output in the least 
    time.
    The system information is:
    {system_info}
    Your response will write to a file called gpt_main.cpp and then compiled and execute; the compilation command is:
    {compile_command}
    Respond on with C++ code.
    Python code to port:
    
    ```python
    {python_code}
    ```
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # GPT
    # openai_client = create_openai_client()
    # reasoning_effort = "high" if "gpt" in MAIN_MODEL else None
    # response = openai_client.chat.completions.create(
    #     model=MAIN_MODEL,
    #     messages=messages,
    #     reasoning_effort=reasoning_effort,
    # )

    ollama_client = create_ollama_client()
    reasoning_effort = "high" if "gpt" in MAIN_MODEL else None
    response = ollama_client.chat.completions.create(
        model=MAIN_MODEL,
        messages=messages,
        reasoning_effort=reasoning_effort,
    )
    results = response.choices[0].message.content
    cpp = results.replace('```cpp', '').replace('```', '')

    if cpp:
        with open("main.cpp", "w", encoding="utf-8") as f:
            f.write(cpp)
    else:
        print("Nothing was generated")


if __name__ == '__main__':
    system_info_str = retrieve_system_info()
    # get_cpp_compiler(system_info_str)

    python_code_1 = pi = """
import time

def calculate(iterations, param1, param2):
    result = 1.0
    for i in range(1, iterations+1):
        j = i * param1 - param2
        result -= (1/j)
        j = i * param1 + param2
        result += (1/j)
    return result

start_time = time.time()
result = calculate(200_000_000, 4, 1) * 4
end_time = time.time()

print(f"Result: {result:.12f}")
print(f"Execution Time: {(end_time - start_time):.6f} seconds")
    """

    python_code_2 = """# Be careful to support large numbers

def lcg(seed, a=1664525, c=1013904223, m=2**32):
    value = seed
    while True:
        value = (a * value + c) % m
        yield value
        
def max_subarray_sum(n, seed, min_val, max_val):
    lcg_gen = lcg(seed)
    random_numbers = [next(lcg_gen) % (max_val - min_val + 1) + min_val for _ in range(n)]
    max_sum = float('-inf')
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += random_numbers[j]
            if current_sum > max_sum:
                max_sum = current_sum
    return max_sum

def total_max_subarray_sum(n, initial_seed, min_val, max_val):
    total_sum = 0
    lcg_gen = lcg(initial_seed)
    for _ in range(20):
        seed = next(lcg_gen)
        total_sum += max_subarray_sum(n, seed, min_val, max_val)
    return total_sum

# Parameters
n = 10000         # Number of random numbers
initial_seed = 42 # Initial seed for the LCG
min_val = -10     # Minimum value of random numbers
max_val = 10      # Maximum value of random numbers

# Timing the function
import time
start_time = time.time()
result = total_max_subarray_sum(n, initial_seed, min_val, max_val)
end_time = time.time()

print("Total Maximum Subarray Sum (20 runs):", result)
print("Execution Time: {:.6f} seconds".format(end_time - start_time))
"""
    # run_python_code_str(python_code)
    convert_python_to_cpp(system_info_str, python_code_2)

