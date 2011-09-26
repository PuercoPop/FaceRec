# -*- coding: utf-8 -*-

import cv
import numpy
import PIL.Image
#import pdb
import IPython
#import matplotlib.pyplot

class Profile:
  def __init__(self, id, column ):
    """
    id: nombre (str)
    column: vector de la foto
    sample_count: número de muestras (flato)
    Agregar un flag processed?
    """
    self.name = id
    self.matrix = numpy.array( column).reshape(-1,1)
    self.sample_count = 1.0
  
  def add_sample(self,column):
    self.matrix = numpy.hstack( [self.matrix, column ])
    self.sample_count += 1
  
  def calc_mean_stddev(self):
    self.matrix_mean = self.matrix.mean( axis = 1 ).reshape(-1,1)
    (row_count, col_count) = self.matrix.shape
    accum = 0
    for col in range(col_count):
      accum += ( self.matrix_mean - self.matrix[:,col].reshape(-1,1) ) ** 2
    self.std_dev = accum / float( self.sample_count)
  
  def max_distance(self):
    return self.std_dev * 3
  
  def fits_profile(self, candidate):
    """
    candidate: vector columna de la nueva muestra
    returns: la distancia que los separa y el signo + significa que si pertenece y el negativo que no.
    """
    
    tmp_vec = self.matrix_mean - candidate
    distance = numpy.dot( tmp_vec.T , tmp_vec ) #scalar
    
    if distance < max_distance():
      return distance
    else:
      return -1 * distance



class PhotoDatabase:
  """
  array: es el arreglo de fotos convertirdas en vectores ( columnas )
  avg_Matrix: es la vector de todas las imagenes
  diff_Matrix: los imagenes expresadas en vectores con respecto a la media
  """
  def __init__(self):
    self.db_Matrix = None
    self.names = []
    self.diff_Matrix = None
    self.eigv_Matrix = None
  
  def sort_eigvectors(self, eig_val, eig_vec):
    """
    Definitivamente no la solución más optima.
    Aqui es dónde puedo poner un tope o descartar PCs
    """
    eigen_val_list = []
    eigen_vec_list = []
    (row, col) = eig_vec.shape
    for p_col in range(col):
      #eigenvectors = numpy.hstack(  (eigenvectors ,numpy.dot(  self.diff_Matrix , eigenvectors_i[:, p_col] ) ) ) #ordenados como uan matrix.
      eigen_val_list.append( eig_val[p_col])
      eigen_vec_list.append( eig_vec[:, p_col] )
    
    #ordena los autovectores en función del autovaluor más grande
    eigen_tuple = zip( eigen_val_list,  eigen_vec_list)
    sorted(eigen_tuple)
    eig_val_s = [ item[0] for item in eigen_tuple ]
    eig_vec_s = [ item[1] for item in eigen_tuple ]
    
    first_pass = True
    for col in eig_vec_s:
      if first_pass is True:
        eig_vec_ss = col[:]
        first_pass = False
      else:
        eig_vec_ss = numpy.hstack ( [eig_vec_ss, col[:]] )
    
    return ( numpy.array( eig_val_s) , eig_vec_ss )
  
  def project_into_subspace(self, subspace, img_ma):
    (row_num,col_num) = img_ma.shape
    fPass = True
    for row in range(row_num):
      x,res_sum,rank,s = numpy.linalg.lstsq( subspace, img_ma[row].T)
      if fPass is True:
        eig_faces = x
        fPass = False
      else:
        eig_faces = numpy.hstack( [ eig_faces,x] )
    return eig_faces

  def generate_profiles(self,eigenfaces, id_list):
    """
    -Identificar las columnas que pertenecen  a la misma identificacion
    -Calcular la media y la desviación estandar.
    """
    d_profiles = {}
    faces = []
    for  index,item in zip( range( len(id_list )), id_list):
      if item in faces:
        d_profiles[item].add_sample( eigenfaces[:,index].reshape(-1,1) )
      else:
        d_profiles[item] = Profile(item,eigenfaces[:,index].reshape(-1,1) )
        faces.append(item)
      
    return d_profiles

  def evaluate_new_face(self, column):
      """
      Primero se proyecta el retrato
      """
      new_face, res_sum,rank,s = numpy.linalg.lstsq( self.eigenvectors, column)
      
      candidates = []
      candidates_rank = []
      for key in self.d_profiles.keys():
        result = d_profiles[key].fits_profile(column)
        if result > 0:
          candidates_rank.append( result )
          candidates.append( d_profiles[key] )
      
      #Si hay más de un match se elige el que tiene menos distancia
      if len(candidates) == 1:
        print "Match:", candidates[0].name
        matched_profile = candidates[0]
      else:
        print "Match:", candidates[ candidates_rank.index( min(candidates_rank) ) ].name
        matched_profile = candidates[ candidates_rank.index( min(candidates_rank) ) ].name
      #If no match
      print "No Match"
  
  def add_portrait( self, portrait  ):
    #add column to database
    if self.db_Matrix is None:
      self.db_Matrix = numpy.copy( portrait.vector ) #Si es el primer vector
    else:
      self.db_Matrix = numpy.vstack(  (self.db_Matrix , portrait.vector) ) #Se añaden como filaes las nuevas imagenes
    
    #se alinea la columna con los nombres de la lista
    self.names.append( portrait.name )

  def save_eigenfaces( self,  matrix ):
    target_dir= './EigenFaces/'
    (row , col) = matrix.shape
    for col in range(col):
      vector_img = matrix
      img = PIL.Image.fromarray(  vector_img.reshape(256, -1),  "L" )
      img.save(target_dir + 'IMG_' + str(col) + '.png' )
      #matplotlib.pyplot.imshow( vector_img.reshape(256, -1) )
      #matplotlib.pyplot.savefig( target_dir + 'IMG_' + str(col) + '.png' )
   
  def process_db(self):
    """
    Pasos a seguir:
    1. Expresar las imagenes como diferencias con respecto a la media.
    2. Obtener los PC (ver como descartar)
    3. Expresar las imagenes como una combinación de los de los PC
       -Calcular el error incurrido
    4. Calcular la media y distancia promedio/ desviación estandar de cada grupo de muestras. A partir de esto sacar la distancia máxima de la media para considerar a una nueva muestra parte del grupo
    
    """
    #Paso 1
    #Se obtiene la imagen promedio, Se expresan las imagenes como diferencia a la media aritmética
    self.avg_Matrix = self.db_Matrix.mean( axis = 0 )
    self.diff_Matrix = self.avg_Matrix - self.db_Matrix
    #Paso 2
    #Exraer los autovalores de la matriz de covarianza( Truco A.T * A ) Pero como estan como filas por defecto en numpy
    covar_Matrix_i = numpy.dot( self.diff_Matrix , self.diff_Matrix.T)
    #covar_Matrix_i = numpy.dot( self.diff_Matrix , self.diff_Matrix.T)
    eigenvalues_i, eigenvectors_i = numpy.linalg.eig( covar_Matrix_i )
    #Ordenando los autovectors de acuerdo a los autovalores, de mayor a menor.
    eig_val, eig_vec = self.sort_eigvectors( eigenvalues_i[:], eigenvectors_i[:])
    #ahora transformarlos a los autovalroes de a la matrix de Covarianza al través de A*v
    self.eigenvectors = numpy.dot( self.diff_Matrix.T , eig_vec)
    #Paso 3 
    #x vector proyectado al subspacio
    #x,res_sum,rank,s = numpy.linalg.lstsq( self.eigenvectors, self.diff_Matrix[0].T)
    self.eigen_faces = self.project_into_subspace( self.eigenvectors, self.diff_Matrix )
    #Falta agrupar las ids iguales, calcular el punto medio y la desviación estandar.
    self.d_profiles = self.generate_profiles(self.eigen_faces[:],self.names[:])
    
    for key in d_profiles.keys()[]
      d_profiles[key].calc_mean_stddev()
    
    IPython.embed()
    
    #Paso 5
    

class Photo:
  """
  Processing_Finished,
  Una vez que se ha puesto un id a cada portrait o se ha rechazado como portrait
  """
  def __init__(self,path):
    self.portraits = []
    self.processing_finished = False

  def remove_portrait():
    pass
  
  def find_portraits( self,  path):
    cascade = cv.Load( 'haarcascade_frontalface_alt.xml' )
    img = cv.LoadImage( path )
    img_gray = cv.CreateImage( cv.GetSize(img), img.depth, 1)
    cv.CvtColor( img, img_gray, cv.CV_BGR2GRAY )
    faces = cv.HaarDetectObjects( img , cascade , cv.CreateMemStorage(),)
    
    if len(faces)>0:
      pass
    else:
      return False
    
    for counter , ((x, y, w, h), n) in enumerate(faces):
      cv.SetImageROI( img, (x,y,w,h ) )#Fija la region de interes
      img_face = cv.CreateImage( cv.GetSize(img) , img.depth , img.nChannels )
      cv.Copy( img , img_face )
      cv.SaveImage("Temp_Faces/face_" +str(img)+"_"+str(counter)+".png", img_face )
      img_portrait = cv.CreateImage( (128,128), img.depth , img.nChannels )
      cv.Resize( img_face , img_portrait , interpolation=cv.CV_INTER_CUBIC )
      cv.SaveImage( "Potrait_" + str(counter), img_portrait)
      self.potraits.append( Portrait( "Portrait" + str(counter) ))
      cv.ResetImageROI(img)
  

class Portrait:
  """
  Supuestos: Se le entrega una imagen frontal ya identificada como un rostro y remuestrada a una magnitud uniforme (256x256)
  vec_portait: vector
  """
  def __init__(self, img_path, name, size=None):
    self.name = name
    self.img_path = img_path
        
    self.img = cv.LoadImage( self.img_path )
    
    if size == None:
      (self.width , self.height) = cv.GetSize( self.img )
    else:
      self.width, self. height = size
    
    self.vector = self.vectorize()
  
  def set_name( self,  name ):
    self.name = name  
  
  def vectorize(self):
    #volver la imagen pasada en path en un vector de 1 columna x N filas
    return numpy.asmatrix( PIL.Image.open( self.img_path ).convert("L") ).reshape( 1,-1 ) 
  

if __name__ == "__main__":
  db = PhotoDatabase()
  db.add_portrait( Portrait('Temp_Faces/face_Positivo_0.png','Gabylonia') )
  db.add_portrait( Portrait('Temp_Faces/face_Positivo_1.png', 'Javier') )
  db.add_portrait( Portrait('Temp_Faces/face_MatukOllantaDixit_0.png',  'Matuk') )
  db.process_db()
  db.evaluate_new_face('')
  pdb.set_trace()
