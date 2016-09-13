# Clothes Extraction Web API

Clothes extraction with torando, Google drive API and openCV
 
This is a simple web API to receive the requests from client and process the images on Google drive to extract clothes. Most of images have simple background and faces could be detected with good accuracy, a straightforward solution is proposed. Firstly, use openCV Harr Cascades face detection. Secondly, use edges to determine the object location. Thirdly, calculate naive background model and skin model to obtain the clothes and remove the background and human body. Use torando interface to support a POST /cut operation. Use PyDrive to download all images from Google drive. In current codes, download function is commented for test purpose. It could be used at the first time to access the image folder. 

##Environment

Python3.5.2 with OpenCV 3.0.0 on OSX 2.6 GHz Intel Core i7 and 16GB DDR3

Virtualenv install tornado, pydrive packages etc. 

There are 97 images on shared folder.

Pydrive doesn't support python3 if installed through pip and auth.py needs to updated. 

Some functions from OpenCV encountered problems with Threadpool multithread execution. Use substitution functions or lock. 
   
##How to run it? 

At server, run "python3 server.py"
At client, send command curl -X POST -d '{"number_thread":4,"path":"https://drive.google.com/drive/folders/0B96ROFsiJB0pVjBrNFdsUHlXenc"}' -v http://localhost:8888/cut

response will send back to client to denote number of processed images, total processing time, average processing time and output directory. 

The extracted images are found at /out. Downloaded images are at /images. myapp.log saves execution information 

##Performance analyze:

Implement multithread solution to assign tasks to multiple threads. Compare the average processing time at different threads 2, 4, 6, 8, 10 and 20.     

Thread  Average processing time (ms)

2       1300.6   

4       1227.13

6       1234.58 

8       1224.96

10      1224.46

20      1240.02

##Comments:

It didn't achieve satisfying results on most of images. Dresses are detected on example_7_1.jpg, Copy of image27_test.jpg, Copy of image52_test_cut.jpg etc. /boundarea is the result of the bound image excluding some background and head. It achieved very good location of object, but the following extraction could not work with this simple solution. Graphcut method from OpenCV is tried but it is worse than current implementation. Creating models from clothes with color and texture may be a possible alternative.   
      
