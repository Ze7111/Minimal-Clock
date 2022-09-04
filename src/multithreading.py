import threading # impoort threading

threads = 8 # max threads
stop_thread = False # stop threads
thread_names = [] # list of threads 
debug = False # debug mode

def start_thread(func): # start thread
    def wrapper(*args, **kwargs): # wrapper
        global stop_thread, thread_names, debug # global variables
        if debug == True: print(f"Starting thread Function: {func.__name__}") # print debug
        
        if stop_thread == True: # if stop_thread is true
            for thread in thread_names: # for each thread in thread_names
                if debug == True: print(f"Stopping thread {thread}") # print debug
                thread.join().stop() # stop thread
                return True # return true
        
        if threads >= len(thread_names): # if the max threads is greater than or equal to the length of thread_names
            thread_names.append(threading.Thread(target=func, args=args, kwargs=kwargs)) # append thread to thread_names
            if debug == True: print(f"Thread {func.__name__} started"); print(f"There are {len(thread_names)} threads running") # print debug
            thread_names[-1].start() # start thread
        else: return 'Max threads reached' # return max threads reached
        
        if debug == True: print(f"Thread {func.__name__} finished") # print debug
    return wrapper # return wrapper

def main(func): # main function
    def wrapper(*args, **kwargs):
        global stop_thread, thread_names, debug # global variables
        stop_thread = False # set stop_thread to false
        @start_thread # use start thread decorator
        def new_func(*args, **kwargs): # new function
            func(*args, **kwargs) # call function
        new_func(*args, **kwargs) # call new_func
    return wrapper # return wrapper

def placeholder(): # placeholder function
    pass # pass

def stop_threads(): # stop threads
    global stop_thread # global variable
    if stop_thread == True: # if stop_thread is true
        return True # return true
    
def stop_all_threads(): # stop all threads
    global stop_thread # global variable
    stop_thread = True # set stop_thread to true