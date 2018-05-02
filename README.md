# Image Processor Final Project (Spring 2018)

**Final Project DUE:** Wednesday, May 02, 2018 05:00PM EST 

## Overview
The final project in this class will require our team to leverage the
industry-standard skills learned over this semester to design and
implement a software system to upload an image to a
web-server, perform image-processing tasks on the web-server, and then display
/ download your processed image. 

This final project was  open-ended to allow our group to tailor this to
their areas of interest.

The following proper professional software
development and design conventions taught in this class were used in the 
creation of the web-app:
* git feature-branch workflow
* continuous integration
* unit testing
* PEP8
* docstrings / Sphinx documentation

## Functional Specifications
### Front End
* Provides a front-end that will allow a user to select an image that will be 
  uploaded to the web-server,
  perform necessary preprocessing steps (convert image to base64 string), and 
  then issue a RESTful API request
  to your cloud service for further processing.
* Front-end has a choice of processing steps to perform on each
  uploaded image, including:
  + Histogram Equalization [default] (Pre- Processing: Grayscale Conversion)
  + Contrast Stretching
  + Log Compression
  + Reverse Video
  + Edge Detection (Pre- Processing: Grayscale Conversion)
* Front-end contains a text field for user to write their email to access their saved images
* Front-end has a gallery of all final processed images store for the user
* A table to provide usefull metadata for the user:
  + Upload Time
  + User Email
  + Process Requested
  + Image Size
  + Process Duration
  + Grayscale Conversion (Required in Histogram Equalization and Edge Detection)
* Front-end also provides:
  + A viewer window to compare the original and processed images.
  + A viewer window to compare the original and processed image histograms.
  + A button to download the image in the following format:
    - JPEG

### Back End
* A cloud-based web service that exposes a well-crafted RESTful API that will
  implement the image processing methods specified above.
  + Post-Request: Upload an image and determine what image processing function
  to run. As well as to handle user data allocation. 
  + Get-Request: Return a jason file with all metadata along with images (processed and original).
* A database is implemented to do the following:
  + Store previous user actions / metrics (metadata sepcified above). 
  + Store uploaded images and timestamps for a user
  + Store processed images (along with what processing was applied) and timestamps for a user

## Deliverables
# [checkbox:checked] A `README` describing the final performance and state of your
  project.
# [checkbox:checked] Recorded video demo of image processor in action:
  + demo.mp4
# [checkbox:checked] All project code (in the form of a tagged GitHub repository named
  `ImageProcessorS18`)
# [checkbox:checked] Link to deployed web service
  + http://imageprocessor.surge.sh/
* Final RFC link and PDF
  + 

## Install App
* Installation instructions
  + Clone the repository
  `git clone https://github.com/martinli8/image_processor.git`
  + Move into repository folder (image_processor)
  `cd image_processor`
  + Move into React App folder (image_processor_viewer)
  `cd image_processor_viewer`
  + Install app dependencies 
  `npm install`
  + Run app
  `npm start`

## Grading

* RFC Document
* Git Repository
  + Issues/Milestones
  + Commits are discrete, logical changesets
  + Feature-branch workflow
* Software best practices
  + Modularity of software code
  + Handling and raising exceptions
  + Language convention and style (PEP8)
  + Sphinx documentation for all modules/functions
* Testing and CI
  + Unit test coverage of all functions (except Flask handler)
  + Travis CI passing build
* Cloud-based Web Service
  + RESTful API Design 
  + Validation Logic 
  + Returning proper error codes
  + Robust deployment on virtual machine 
  + Image processing functionality
* Proper use of a Database 
* Client software functionality
* Demo of the final working project
* Robust README