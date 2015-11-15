import cmath,time

class polyroots:
    
    def __init__(self, coarray=[], overflow=1, precision=4):
        self.overflow = overflow
        self.coarray = coarray
        self.precision = precision
        self.timeout=False
    
    
    def set_overflow(self, overflow):
        '''Sets timeout in seconds.
        Stops the process if the time limit exceeded'''
        self.overflow = overflow
        return
    
    def set_coarray(self, coarray):
        self.coarray = coarray        
        return
    
    
    def set_precision(self, precision):
        self.precision = precision
        return
    
    def derivative(self, array):
        arr_size = len(array)
        new_arr = []
        for id,element in enumerate(array[:-1]):
            new_arr.append(element*(arr_size-id-1))
        return new_arr  
    
    
    def _solve(self,x, array, debug=False):
        arr_size = len(array)
        result = 0
        for id,element in enumerate(array):
            if debug:
                print(result, element)
            result += element*x**(arr_size-id-1)
        return result
    
    
    def divide_arr(self,big, small):
        big_num = len(big)
        small_num = len(small)
        ret_arr = []
        for id,element in enumerate(big):
            tmp_div = element / small[0]
            if id != big_num-1:
                big[id+1] -= tmp_div * small[1]
            ret_arr.append(tmp_div)
        return ret_arr
    
    
    def newton_c(self,x_0, array, debug=False):
        x_n = x_0
        der_arr = self.derivative(array)
        t0 = time.clock()
        while True:
            try:
                x_n = x_n - self._solve(x_n, array)/self._solve(x_n, der_arr)
            except:
                x_n += 0.1
                continue
            if debug:
                print(round(x_n, 4))
            if round(self._solve(x_n, array).real, self.precision*2) + round(self._solve(x_n, array).imag, self.precision*2)*1j == 0j:
                break
            global overflow
            if time.clock() - t0 > self.overflow:
                self.timeout = True
                break
        return round(x_n.real, self.precision) + round(x_n.imag, self.precision)*1j
    
    
    def solve(self,x_n=0):
        ret_arr = []
        second_arr = self.coarray[:]
        while True:
            if len(second_arr) == 1 or len(second_arr) < 1:
                break
            result = self.newton_c(x_n, second_arr)
            if self.timeout:
                print("Overflow time exceeded.")
                break
            if result.imag == 0:
                result = result.real
            ret_arr.append(result)
            second_arr = self.divide_arr(second_arr, [1, -1*result])[:-1]        
        return ret_arr