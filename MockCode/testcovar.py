import numpy
import pdb

a = numpy.matrix([[1,2,2],[3,21,1],[3,2,11],[23,2,1]],numpy.dtype('int8') )
#a = numpy.matrix( [[1,2],[3,5]] )
b = a.T
print a
print "Byte Size:",a.dtype.itemsize
print "Byte Size:",b.dtype.itemsize

#ein_val, ein_vec, shape = numpy.linalg.svd(numpy.dot(a,b))
ein_val, ein_vec = numpy.linalg.eig(numpy.dot(a,b))
ein_val_i, ein_vec_i = numpy.linalg.eig(numpy.dot(b,a))

#ein_vec, ein_val, shape = numpy.linalg.svd(numpy.dot(a,b))
#ein_vec_i, ein_val_i, shape_i = numpy.linalg.svd(numpy.dot(b,a))

(row,col) = ein_vec_i.shape

for p_col in range(col):
  t = numpy.dot(a,ein_vec_i[:,p_col])
  print "A:",t
  print "B:",ein_vec[:,p_col]
  print "Ratio:",(t/ein_vec[:,p_col])[0]
  print "\n"

pdb.set_trace()

