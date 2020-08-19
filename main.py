import multiprocessing.dummy
import multiprocessing
from pythonping import ping


def ping_compare(ip_list):
    if ping(ip_list[0], count=2).success() is False and ping(ip_list[1], count=2).success() is True:
        return "PING " + str(ip_list[0]) + ": Failed  PING " + str(ip_list[1]) + ": Success"
    elif ping(ip_list[0], count=2).success() is True and ping(ip_list[1], count=2).success() is False:
        return "PING " + str(ip_list[0]) + ": Success  PING " + str(ip_list[1]) + ": Failed"
    else:
        pass


def ping_thread_range(partial_ip_one, partial_ip_two, begin, end, exceptions):
    """Create a thread pool to perform the ping_compare function. Iterate from beginning to end of IP range.

    Returns a list of filtered ping_compare results
    """
    total_threads = 3 * multiprocessing.cpu_count()
    thread_pool = multiprocessing.dummy.Pool(total_threads)
    ping_results = list(
                 filter(None, (thread_pool.map(ping_compare,
                               zip([partial_ip_one + str(x) for x in range(begin, end) if x not in exceptions],
                                   [partial_ip_two + str(x) for x in range(begin, end) if x not in exceptions])))))

    return ping_results


def test(partial_ip_one, partial_ip_two, begin, end, exceptions):
    """Used to execute other functions and output results in readable format
    """
    results = ping_thread_range(partial_ip_one, partial_ip_two, begin, end, exceptions)

    print('\n' + "Test Complete!" + '\n' + "Found " + str(len(results)) + " failed cases: ")
    print(*results, sep="\n")


if __name__ == '__main__':
    test_one_exceptions = [15, 25, 32]
    test_two_exceptions = []
    test_three_exceptions = list(range(0, 255))

    test("192.168.1.", "192.168.2.", 1, 254, test_one_exceptions)
    test("192.168.1.", "192.168.2.", 1, 254, test_two_exceptions)
    test("192.168.1.", "192.168.2.", 1, 254, test_three_exceptions)
