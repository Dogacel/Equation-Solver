# Equation-Solver
### Python 3.4

##A basic demonstration of solving polynomial equations with python using Newton's Method.
 Run test.py to see how it works !

# Overview
------------------

-->Polyroots.py : 

```python

class polyroots:
    
    def __init__(self, coarray=[], overflow=1, precision=4):
        self.overflow = overflow #Time limit for calculation process. 
        self.coarray = coarray #array : constants of a polynomial ex: 3x^4 + 2x^2 - 5x = [ 3 , 0 , 2 , -5 , 0]
        self.precision = precision #Number of fractional digits
        self.timeout=False #Set true if timelimit exceeded
```
#####This function is not the best way to get derivative. But its fast and usable in this project.

```python
def derivative(self, array):
        arr_size = len(array)
        new_arr = [] #create a temporary array
        for id,element in enumerate(array[:-1]):
            new_arr.append(element*(arr_size-id-1))
            # This is an easy method to find derivative of a polynomial.
            #f(x) = ax^n --> f'(x) = anx^(n-1)
            
        return new_arr #return
```

#####This method basically replaces the indeterminate in the polynomial with the variable "x"


```python
 def _solve(self,x, array, debug=False):
        arr_size = len(array)
        result = 0
        for id,element in enumerate(array):
            if debug:
                print(result, element)
            result += element*x**(arr_size-id-1) # ax^n
        return result

```

####Polynomial division

```python
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

```


### Newton's Method
It keeps dividing polynomial into its derivative.
for more info [click here](https://en.wikipedia.org/wiki/Newton%27s_method).

```python

    def newton_c(self,x_0, array, debug=False):
        x_n = x_0
        der_arr = self.derivative(array)
        t0 = time.clock()
        while True:
            try:
                x_n = x_n - self._solve(x_n, array)/self._solve(x_n, der_arr)
            except:
                x_n += 0.1 #if x_n is 0 it would throw an error.
                continue
            if debug:
                print(round(x_n, 4))
            if round(self._solve(x_n, array).real, self.precision*2) + round(self._solve(x_n, array).imag, self.precision*2)*1j == 0j:
                break
            global overflow 
            if time.clock() - t0 > self.overflow: #Did we exceed the time limit ?
                self.timeout = True
                break
        return round(x_n.real, self.precision) + round(x_n.imag, self.precision)*1j
```


###Secure way to solve:

```python

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

```
