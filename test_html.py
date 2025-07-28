import sympy
from sympy.printing.mathml import mathml

x2, y, z = sympy.symbols('x2 y z')
y = x2*z+x2**3
f = open('sympy_test.html', 'w')
f.write('<html>\n')
f.write('<head>\n')
f.write('<title>SymPy MathML Test</title>\n')
f.write('</head>\n')
f.write('<body>\n')
f.write('<math xmlns="http://www.w3.org/1998/Math/MathML">\n')
f.write(sympy.mathml(y, printer='presentation')+'\n')
f.write('</math>\n')
f.write('</body>\n')
f.write('</html>\n')
f.close()