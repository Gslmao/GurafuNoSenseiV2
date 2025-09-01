import matplotlib.pyplot as plt
import sympy as sy
import numpy

from F_FuncLib import derivative

class MathTools:
    """
    Provides mathematical tools for equation processing, plotting, and integration.
    """
    def __init__(self, c):
        x = sy.symbols('x')
        self.Derv = False

        if c == 2:
            self.Derv = True

    @staticmethod
    def spc_func(uInput, dFlag):
        try:
            x = sy.symbols('x')
            eqn = uInput.replace("^", "**")

            expr = sy.sympify(uInput)
            f = sy.lambdify(x, expr)

            if 'log' in uInput:
                x_val = numpy.linspace(0, 100, 10000)
            else:
                x_val = numpy.linspace(-100, 100, 10000)

            y_val = [f(val) for val in x_val]

            if dFlag:
                yDeriv = derivative(x_val, y_val)
                return {'x': x_val, 'y': y_val, 'deriv': yDeriv}
            else:
                return {'x': x_val, 'y': y_val}

        except Exception as e:
            print(f"Error in spc_func: {e}")

    @staticmethod
    def polynomial(uInput, dFlag):
        try:

            eqn = uInput.replace("^", "**")
            x = sy.symbols('x')
            expr = sy.sympify(eqn)  # Convert string to sympy expression
            f = sy.lambdify(x, expr)  # Pass the symbol 'x' and the expression
            x_val = numpy.linspace(-100, 100, 4000)

            y_val = [f(x) for x in x_val]
            if dFlag:
                yDeriv = derivative(x_val, y_val)
                return {'x': x_val, 'y': y_val, 'deriv': yDeriv}
            else:
                return {'x': x_val, 'y': y_val}

        except Exception as ex:
            print(f"Error in polynomial: {ex}")

    @staticmethod
    def simp_trig(uInput, dFlag):
        x = sy.symbols('x')
        MathFunc = {
            'sin': numpy.sin, 'cos': numpy.cos, 'tan': numpy.tan,
            'cosec': lambda x: 1 / numpy.sin(x), 'sec': lambda x: 1 / numpy.cos(x), 'cot': lambda x: 1 / numpy.tan(x),
            'log': numpy.log
        }

        func = ["sin", "cos", "tan", "cosec", "sec", "cot", "log"]

        def MathFuncFind(uInput, func):
            for subStr in func:
                if subStr in uInput:
                    return subStr

        MathF = MathFuncFind(uInput, func)

        if MathF is not None:
            pass
        else:
            pass
        function = MathFunc[MathF]

        if MathF == "log":
            x_val = numpy.linspace(1e-15, 100, 10000)
        else:
            x_val = numpy.linspace(-100, 100, 10000)

        y_val = []
        for i in x_val:
            val = function(i)
            if val != numpy.inf:
                y_val.append(val)
            else:
                y_val.append(numpy.inf)

        fig, ax = plt.subplots(figsize=(6.5, 5.5))

        if dFlag:
            yDeriv = derivative(x_val, y_val)
            return {'x': x_val, 'y': y_val, 'deriv': yDeriv}
        else:
            return {'x': x_val, 'y': y_val}

    @staticmethod
    def integrate(uInput, **kwargs):
        import sympy as sy
        import numpy as np

        def CustomFuncs():
            from scipy import special
            import numpy as np

            def hyper(a_p, b_p, z):
                if len(a_p) == 2 and len(b_p) == 1:
                    return special.hyp2f1(a_p[0], a_p[1], b_p[0], z)
                else:
                    return special.hyp1f1(a_p[0], b_p[0], z)

            def fresnels(x): return special.fresnel(x)[1]
            def fresnelc(x): return special.fresnel(x)[0]
            def sec(x): return 1 / np.cos(x)
            def cosec(x): return 1 / np.sin(x)
            def cot(x): return 1 / np.tan(x)

            cust_funcs = {
                'fresnels': fresnels, 'fresnelc': fresnelc,
                'gamma': special.gamma, 'hyper': hyper,
                'sec': sec, 'cosec': cosec, 'cot': cot
            }
            return cust_funcs

        try:
            limits = kwargs.get('limits', (None, None))
            lim_u, lim_l = limits if isinstance(limits, (tuple, list)) and len(limits) >= 2 else (None, None)

            flag = kwargs.get('flag', 'y')

            x = sy.symbols('x')
            eqn = uInput.replace("^", "**")
            expr = sy.sympify(eqn)

            custom_functions = CustomFuncs()

            modules = ['numpy', custom_functions]
            f = sy.lambdify(x, expr, modules=modules)

            if flag != 'y':
                x_coord = np.linspace(-100, 100, 10000)
                integral = sy.integrate(expr, x)
                EqnInt = str(integral).replace("**", "^")

            elif flag == 'y' and lim_l is not None and lim_u is not None:
                if lim_l > lim_u:
                    raise ValueError("Lower limit must be less than upper limit")
                integral = sy.integrate(expr, x)
                x_coord = np.linspace(-max(abs(lim_l), abs(lim_u)) * 1.1, max(abs(lim_l), abs(lim_u)) * 1.1, 100000)
                ar_x = np.linspace(lim_l, lim_u)
                ar_y = f(ar_x)
            else:
                raise ValueError("Invalid flag or limits")

            y_coord = f(x_coord)
            g = sy.lambdify(x, integral, modules=modules)
            int_y = g(x_coord)

            if flag != 'y':
                return {'x': x_coord, 'y': y_coord, 'sh_x': None, 'sh_y': None, 'int_inf': int_y, 'integral': EqnInt}
            else:
                return {'x': x_coord, 'y': y_coord, 'sh_x': ar_x, 'sh_y': ar_y, 'int_inf': int_y,
                        'integral': str(integral).replace("**", "^")}

        except Exception as e:
            print(f"Error in integrate function: {e}")
            return None

class MainApp:
    """
    MainApp handles equation parsing, flag detection, and plotting/integration operations.

    Attributes:
        operator (str): Operation flag ('d' for derivative, 'i' for integral, etc.).
        Equation (str): The right-hand side of the equation to process.
        raw_eqn (str): The full equation string as provided.
        limits (tuple): Integration limits, if applicable.
        flags (dict): Dictionary of flags indicating equation type and operation.

    Methods:
        checker(): Detects equation type and sets flags.
        plot_eqn(equation): Processes and returns results for plotting or integration.
    """
    def __init__(self, Eqn, **kwargs):
        self.operator = kwargs.get('operator', None)
        self.Equation = Eqn.split("=")[1]
        self.raw_eqn = Eqn
        self.limits = kwargs.get('limits', None)
        self.flags = self.checker()

    def checker(self):
        flags = {}
        mFunc = ["sin", "cos", "tan", "cosec", "sec", "cot", "log"]
        m1Func = ["sin(x)", "cos(x)", "tan(x)", "cosec(x)", "sec(x)", "cot(x)", "log(x)"]

        chck = self.Equation

        flags['sp_func'] = False
        flags['simp_trig'] = False
        flags['polynomial'] = False

        flags['op'] = self.operator

        for i in mFunc:
            if i in chck:
                flags['sp_func'] = True

            else:
                flags['polynomial'] = True

        for i in m1Func:
            if i == chck:
                flags['simp_trig'] = True
                flags['sp_func'] = False

        return flags

    def plot_eqn(self, equation):
        tools = MathTools(0)
        equation = equation.split("=")[1]
        try:
            if self.flags['op'] != 'i':
                if self.flags['simp_trig']:
                    output = tools.simp_trig(equation, self.flags['op'] if self.flags['op'] == 'd' else False)
                    return output, equation

                elif self.flags['polynomial']:
                    output = tools.polynomial(equation, self.flags['op'] if self.flags['op'] == 'd' else False)
                    return output, equation

                elif self.flags['sp_func']:
                    output = tools.spc_func(equation, self.flags['op'] if self.flags['op'] == 'd' else False)
                    return output, equation

            elif self.flags['op'] == 'i':
                if self.limits[0] == 0 and self.limits[1] == 0:
                    output = tools.integrate(equation, limits=self.limits, flag='n')
                else:
                    if self.limits[0] < self.limits[1]:
                        raise ValueError
                    else:
                        output = tools.integrate(equation, limits=self.limits)
                return output, equation

            else:
                print("Error: Invalid function type.")
                return None

        except Exception as e:
            print('processing error', e)
