import requests
import time
from urllib import parse

HTTP_RESPONSES = {
    200: ('OK', 'Request fulfilled, document follows'),
    301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
    302: ('Found', 'Object moved temporarily -- see URI list'),
    403: ('Forbidden',
          'Request fo2rbidden -- authorization will not help'),
    500: ('Internal Server Error', 'Server got itself in trouble')
}


def get_number_of_websites():
    while True:
        num_websites = input("Enter the number of websites you want to rate: ")
        try:
            return int(num_websites)
        except ValueError:
            print("ERROR: Input number could not be converted to integer.")



def get_multiple_url_inputs(num_websites):
    urls = []
    for i in range(num_websites):
        url = input(f"Please enter the URL of website {i+1}: ")
        if url.startswith("https"):
            urls.append(url)

    if not urls:
        return None
    return urls


def measure_response_time(url):
    """
    Send a request to url and measure the time until response.
    If there is somekind of a connection problem or HTTP error (like 404),
    just raise an exception.
    """
    # Measure time and make request
    start_time = time.time()
    try:
        response = requests.get(url)
    except requests.exceptions.InvalidURL as e:
        print("Invalid url!", e)
    except requests.exceptions.ConnectionError as e:
        print("Connection Error!", e)
    except requests.exceptions.MissingSchema as e:
        print("Invalid url!", e)
    end_time = time.time()
    response_time = end_time - start_time

    if response.status_code in HTTP_RESPONSES:
        print("Got response: ", HTTP_RESPONSES[response.status_code])
    else:
        print("Got response:", response.status_code)

    # If we've had an exception or HTTP error, we should raise another exception
    if not response.ok:
        raise Exception("Error! Terminating!")

    return response_time


def main():
    # Ask the user how many websites he wants to check and get their url's
    num_websites = get_number_of_websites()
    urls = get_multiple_url_inputs(num_websites)

    # Measure each website's speed, and create a list of tuples like (url, speed)
    response_times = []
    if urls:
        for url in urls:
            response_time = measure_response_time(url)
            response_times.append((url, response_time))

    # Sort the list of tuples according to the speed and take only the top 3 tuples
    sorted_response_times = sorted(response_times, key=lambda x: x[1])
    top_3 = [sorted_response_times[0], sorted_response_times[1], sorted_response_times[2]]

    # Show top 3 websites
    print("Top 3 speed ranking:")
    for i in range(3):
            print(f"{i}. {top_3[i][0]} - {top_3[i][1]:.4f} seconds")

    # Show the average speed
    only_response_times = [response_time[1] for response_time in response_times]
    print("Average speed: ", sum(only_response_times) / len(only_response_times))

if __name__ == "__main__":
    main()