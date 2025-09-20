import requests
import random
import string
import time
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Corrected code length based on user's valid links
CODE_LENGTH = 6
# Output file name for saving hits
FILE_NAME = "vgy_hits.txt"

def generate_vgy_url():
    """Generates a random vgy.me URL."""
    characters = string.ascii_letters + string.digits
    random_code = ''.join(random.choice(characters) for _ in range(CODE_LENGTH))
    return f"https://vgy.me/u/{random_code}"

def check_vgy_link(url):
    """
    Checks if a vgy.me URL contains a valid image.
    Returns the URL if a hit is found, otherwise None.
    """
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            return url
        return None
    except requests.exceptions.RequestException:
        return None

def open_link(url):
    """Opens the provided URL in a new browser tab."""
    try:
        webbrowser.open_new_tab(url)
        print("Link opened in your browser!")
    except webbrowser.Error as e:
        print(f"Error opening browser: {e}")

def save_hit_to_file(url):
    """Appends a found URL to the specified text file."""
    try:
        with open(FILE_NAME, 'a') as f:
            f.write(url + '\n')
    except IOError as e:
        print(f"Error saving file: {e}")

def main():
    """Main function to orchestrate the multithreaded scanning."""
    print(Fore.CYAN + "========================================")
    print(Fore.CYAN + "         RANDOM VGY.ME SCANNER")
    print(Fore.CYAN + "========================================")
    print(Fore.YELLOW + "Scanning for vgy.me images. Press Ctrl+C to stop.")
    
    hits_found = 0
    scanned_count = 0
    start_time = time.time()
    
    # You can adjust the number of threads for your system
    num_threads = 100
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(check_vgy_link, generate_vgy_url()) for _ in range(num_threads)}
        
        try:
            while True:
                for future in as_completed(futures):
                    scanned_count += 1
                    result_url = future.result()
                    
                    if result_url:
                        hits_found += 1
                        elapsed_time = time.time() - start_time
                        print(Fore.GREEN + f"\n[HIT] 🎯 Valid link found! (Hit #{hits_found})")
                        print(Fore.GREEN + f"      Attempts since last hit: {scanned_count} | Time: {elapsed_time:.2f}s")
                        print(Fore.GREEN + f"      Link: {result_url}")
                        
                        save_hit_to_file(result_url)
                        open_link(result_url)
                        
                        print(Fore.CYAN + "----------------------------------------")
                        scanned_count = 0
                        start_time = time.time()
                    else:
                        print(Fore.BLUE + f"Status: Scanned {scanned_count} links...", end="\r", flush=True)

                    # Submit a new task to replace the one that just completed
                    futures.add(executor.submit(check_vgy_link, generate_vgy_url()))
                    futures.remove(future)
        
        except KeyboardInterrupt:
            print(Fore.RED + "\nScan interrupted by user.")
    
    print(Fore.CYAN + "\n========================================")
    print(Fore.GREEN + f"   Total hits found: {hits_found}")
    print(Fore.CYAN + "========================================")

if __name__ == "__main__":
    main()
