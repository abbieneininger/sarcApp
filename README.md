# README.md
![logo](https://user-images.githubusercontent.com/91763838/211939296-4be28219-7ae4-4290-a22e-0a0a412d2df6.png)

# sarcApp: an automated tool for sarcomere quantification
### Abigail Neininger-Castro 2023
### Vanderbilt University
### github/abbieneininger/sarcApp
### abbieneininger@gmail.com


possible stains for sarcomere quantification: actinin2, myomesin, titin

possible stains for edge detection: actin, NMII(A or B)

auxilliary stains for analysis: paxillin, dapi


### installation:

sarcApp and yoU-Net are python-based apps. It is recommended to use Visual Studio Code, especially for beginners. The GUI handler (PySimpleGUI) works in both VS Code and PyCharm. It is also recomended to use Anaconda to create a virtual environment for the required sarcApp packages (below). An advanced programmer can use sarcApp however they'd like.
    
### The requirements for sarcApp and yoU-Net are different. Included below are three requirements lists: one for sarcApp, one for yoU-Net, and one list for both. 

    sarcApp only: os PIL numpy PySimpleGUI csv math skimage io alpha-shapes natsort scipy pickle
    yoU-Net only: torch tensorboard PIL matplotlib numpy os imgaug random natsort torchvision math
    both: os PIL numpy PySimpleGUI csv math skimage io alpha-shapes natsort torch tensorboard matplotlib imgaug random torchvision scipy pickle

## How to run:

If you want to run sarcApp, run sarcApp.py
If you want to train a model from scratch, run trainModel_yoUNetgui.py
If you want to run a pre-trained model, run runModel_yoUNetgui.py

### file setup:

There are three possible inputs for each channel in sarcApp: image folder, binary folder, and data folder. The "image folder" input expects a folder with 2D tiffs of the selected stain. The "image folder" is not required if the user inputs either the "binary folder" or "data folder". However, if the user wishes to see the sarcomere outputs on top of the image, they can input the "image folder". The "binary folder" input expects a folder with 2D tiffs with a binary of the selected stain. For stains not requiring deep learning binarization, a basic otsu threshold or similar can be created in FIJI and saved. The "binary folder" is not required if A) the image is thresholdable by the software using otsu's method (paxillin, dapi, actin, NMIIA) or B) if the user is inputting a "data folder". Similar to the "image folder", if a "binary folder" is not required, it can still be added to see the sarcomre outputs on top of the binary. A "data folder" input expects a folder with CSV files output from a software like FIJI. It expects each file to contain a list of objects with the X and Y coordinates, length and width of the object, angle, area, aspect ratio, and circularity of the object. 
    
The images, binaries, and data files are expected to be in the same order in each folder. They can have different filenames, but must be numerically in the same order. 

### sarcApp.py: GUI 

This file sets up and runs the GUI wrapper for sarcApp. 

Four simultaneous channels may be chosen depending on how many stains the dataset has. For example, a cell might be stained for actinin, myomesin, DAPI, and actin.

Choose each stain and click "go", or click "clear" to start over. For each stain, a separate upload menu will appear. Select the image folder, binary folder, and/or data folder of interest, and create a folder in the "output folder" menu for all of the data to be saved into. If images or binaries are uploaded, the sarcomere quantification outputs will appear on the screen one-by-one for the user to observe. If only data is uploaded from FIJI or an equivalent, the app will run faster but the images will not be shown. 

### edge data:

There are three stains that can be used to detect the edge: actinin2, NMII(A-B), and F-actin (phalloidin). An edge stain is not strictly necessary for any marker, but it is prefered for myomesin and titin. Without an edge marker, many of the metrics can still be calculated, but metrics including "distance from the edge", "relative orientation", etc. will not be calculated. Because actinin2 localizes close to the edge, actinin2 does not require a separate edge marker and can be used itself. If actin or NMII(A-B) are uploaded alone, no metrics will be calculated but a shapely Geometry of the edge will be produced and saved as a pickle in the output folder. 

### dataset handler:
    
Each dataset is opened and saved under the class Dataset in Dataset.py

## yoUNet: a tool to train a deep learning model to predict binaries of 2D microscopy images (or used pre-trained datasets to binarize images of sarcomeric proteins)

Generating deep learning models to predict binaries: There are two steps to generating a deep-learning model using yoU-Net: generate annotated ground truth binaries, and train a model using them. Users can use whichever app they prefer to generate binaries; we used LabKit in FIJI. Generate binaries such that the background grey level is 0 and the foreground is 255. Set up four folders: a folder for your training images, a folder for the matched ground truth binaries, a folder for validation images, and a folder for the matched ground truth binaries for the validation dataset. It is recommended to put 10-20% of your images/matched binaries as validation images. The validation images must not overlap with the training images. There are decisions to be made to train a deep learning model: number of epochs (steps, start at 100) and number of features (16 or 32). During training, the loss function values and the validation metric values are printed on the screen. When the function is complete and the user is happy with the binaries generated, they can move on to the next step. What makes a user happy with binaries? Depends on the user and the stain. It is generally preferred to stop the model when the loss function stops decreasing and the validation metric stops increasing. keeping the model running for much longer could be allowing the model to "memorize" your data, in which case its functionality for new, unseen images might not be as expected.

Using deep learning model to generate binaries: We generated three deep learning-based models: one for actinin2, one for myomesin, and one for titin. If the user wishes to generate binaries based on one of these stains, or based on a new stain that a model has been already generated for (using the previous step), the user can use "runModel_yoUNetgui.py" (see below). There should be a folder of images and an empty output folder as inputs. The output will be a prediction map (Not a binary!) for each image. A pixel grey value of 0 represents that the model is certain that pixel is background, and a pixel grey value of 255 represents that the model is certain that pixel is foreground. It is up to the user to open these prediction maps (probably in FIJI) and threshold them in a way that captures the features of interest. It is important that the same threshold is used for every image. Once the prediction maps have been converted into binaries by the user and saved in a separate folder, the user can either A) go ahead with sarcApp quantification or B) use FIJI/Image J to analyze particles in the binary to generate a folder full of data files (csv) to input into sarcApp

Using yoU-Net-generated binaries in sarcApp: If you generated binaries for any of the supported markers in sarcApp, now you can quantify them! Use the sarcApp GUI to input the binaries and/or data files (and images if you'd like) and run it as above.



## STAINS: 

#### actinin:
If only the images are uploaded, a binary is created (see makeBinary.py) and quantified (see binaryMeasure.py) before quantification proceeds. If only a binary is uploaded, it is quantified through binaryMeasure.py then sarcomere quantification proceeds. If data is uploaded (with or without any images), the quantification occurs immediately.

All actinin data is handled through actininMain.py once the data is ready (uploaded or calculated via binary). actininMain.py determines what data has been uploaded, calls the code to generate and quantify an image/binary, and calls actininFixed2D: the major quantification code. It is named "Fixed2D" because we anticipate accepting live data and/or 3D data in the future. 

In actininFixed2D, first objects are separated into potential Z-Lines (longer than 1.4 microns) and Z-bodies (between 0.2 and 1.4 microns along the long axis). Next, the edge boundaries are detected (see edgeDetection.py). Next, any identified "H" structure (two Z-Lines with a connecting bridge, see Figure S2) is separated into its two Z-Lines in the function solveH. Then, myofibrils are identified (see myofibrilSearch.py) and MSFs (MSFSearch.py) are identified. Then the identified myofibrils and MSFs are quantified using calcMyofibrils.py and calcMSFs.py, respectively, and the data is combined for the entire folder and saved in the output folder. If images/binaries were uploaded, the quantified myofibrils and MSFs will be drawn on the image itself so the user can observe how sarcApp is quantifying the data in real time. Each myofibril will be a different color and each Z-Body within an MSF will be red. These images will be saved to the output folder as well//. To proceed to the next cell, click 'Next' in the lower righthand corner.

#### actin:

If actin alone is selected, no metrics will be calculated but a shapely Geometry of the edge will be produced and saved as a pickle in the output folder. If actin is selected with myomesin or titin, the edge will be used to calculate extra metrics (distance from edge, relative angle, etc.). 

actinMain.py is the first function used: it identifies if actin was selected alone or with another marker. If alone, the edge is calculated using findActinEdge.py. Briefly, a threshold is calculated on the actin image and small objects are removed and holes filled. This function accounts for raw actin images as well as images that have large black sections in it: this is intended in case any image has several cells in it and the user wishes to quantify them separately. One way to do so is to only produce a binary of each cell, and/or to produce one image per cell in which all the other cells are deleted. Just be aware to keep all raw data and never publish the modified images: they are only for edge detection! 

If actin was chosen with myomesin or titin, the edge is determined within myomesinMain.py or titinMain.py using the same technique.

#### myomesin:

If only the images are uploaded, a binary is created (see makeBinary.py) and quantified (see binaryMeasure.py) before quantification proceeds. If only a binary is uploaded, it is quantified through binaryMeasure.py then sarcomere quantification proceeds. If data is uploaded (with or without any images), the quantification occurs immediately.

If myomesin is included with F-actin, NMII (A or B), or actinin, the edge will be quantified using findActinEdge.py, findNMIIEdge.py, or edgeDetection.py, respectively. if myomesin is uploaded without one of these three markers, quantification proceeds without an edge. These determinations are made in myomesinMain.py. Once the edge is detected (or not) and the data path is read, the next function is myomesinFixed2D.py. This function is extremely similar to actininFixed2D.py, in which potential M-Lines are first separated from smaller objects, and myofibrilSearch.py assigns these M-Lines to myofibrils. The major change is that there are no Z-Bodies (or any type or precursor) with myomesin, and that there only needs to be 3 M-Lines in a row to be considered a myofibril. This is directly related to the 4 Z-Lines in a row for actinin: if a myofibril has 4 Z-Lines, it would have 3 M-Lines directly in the center of the Z-Lines. 

If an image/binary is uploaded with the data alongside, the quantified myofibrils will be drawn on the image itself so the user can observe how sarcApp is quantifying the data in real time. Each myofibril will be a different color. These images will be saved to the output folder as well//. To proceed to the next cell, click 'Next' in the lower righthand corner.

The myomesin outputs for each cell are Total Number of Myofibrils, Total Number of M-Lines, Average Myofibril Persistence Length, Average M-Line Length, Average M-Line Spacing, Average Size of All Puncta, and Total Number of Puncta. For each myofibril, the basic outputs are Number of M-Lines, Average Spacing, Persistence Length, Angle of Myofibril Long Axis, and Average M-Line Length. If an edge is added, three extra outputs are included: Distance from the Edge, Edge Angle, and Normalized Myofibril Angle Compared to Edge.

#### NMII(A-B):

The edge detection for NMII is similar to actin, but different based on the differing localizations of each protein. Actin localizes through the entire cell, whereas NMII(A-B) localizes to the cell edge only. If NMII alone is selected, no metrics will be calculated but a shapely Geometry of the edge will be produced and saved as a pickle in the output folder. If NMII is selected with myomesin or titin, the edge will be used to calculate extra metrics (distance from edge, relative angle, etc.). 

NMIIMain.py is the first function used: If alone, findNMIIEdge.py is called to find the cell edge. In brief, a threshold is calculated on the NMII image followed by watershed segmentation and binary dilation, then small obejcts are removed and holes filled. Finally, the image goes through a sobel filter to produce the final edge coordinates. 

This function accounts for raw NMII images as well as images that have large black sections in it: this is intended in case any image has several cells in it and the user wishes to quantify them separately. One way to do so is to only produce a binary of each cell, and/or to produce one image per cell in which all the other cells are deleted. Just be aware to keep all raw data and never publish the modified images: they are only for edge detection! 

If NMII was chosen with myomesin or titin, the edge is determined within myomesinMain.py or titinMain.py using the same technique.

#### DAPI:

DAPI is a nuclear stain. Cardiac myocytes are freuqently binucleated (having two nuclei) so nuclei count and area is of interest to many cardiac biologists. Thus, DAPI can be quantified in sarcApp. The images uploaded are binarized using makeBinary.py and measured in binaryMeasure.py. If data/a binary is given, the outputs for each cell are Number of Nuclei and Area. If an image is given, another output is added: Average Grey Level of the nucleus. All data is saved in the output folder as csv files. 

#### paxillin:

Paxillin stains focal adhesions. Cardiac myocytes have focal adhesions in culture and many researchers co-stain sarcomere markers with adhesion markers, so adhesion quantification is added to sarcApp as an auxilliary stain. The uploaded images are binariezed using makeBinary.py and measured with binaryMeasure.py, similar to DAPI. If data/a binary is given, the outputs for each cell are Number of Adhesions and Area. If an image is given, another output is added: Average Grey Level of each adhesion. All data is saved in the output folder as csv files. 

#### titin: 

It is not recommended to only upload titin images, as a basic Otsu threshold will almost certainly not work well. It is recommended to use the provided yoU-Net-generated model to generate binaries first, then use those binaries for quantification. If only a binary is uploaded, it is quantified through binaryMeasure.py then sarcomere quantification proceeds. If data is uploaded (with or without any images), the quantification occurs immediately.

if titin is included with F-actin, NMII (A or B), or actinin, the edge will be quantified using findActinEdge.py, findNMIIEdge.py, or edgeDetection.py, respectively. if titin is uploaded without one of these three markers, quantification proceeds without an edge. These determinations are made in titinMain.py. Once the edge is detected (or not) and the data path is read, the next function is titinFixed2D.py. This function provides similar functionality to actininFixed2D.py and myomesinFixed2D.py. In brief, potential doublets and single lines that might be part of a doublet are partitioned from the dataset. Potential single lines are then paired together into doublets then all doublets are passed to myofibrilSearch.py and calcMyofibrils.py, where doublets are assigned to myofibrils and stats are calculated on a per-cell and per-myofibril level. Next, the remaining titin structures are classified into precursor rings based on size and aspect ratio. The list of rings is passed to calculateRings which calculates stats for rings on a per-cell level.

If an image/binary is uploaded with the data alongside, the quantified myofibrils will be drawn on the image itself so the user can observe how sarcApp is quantifying the data in real time. Each myofibril will be a different color. These images will be saved to the output folder as well//. To proceed to the next cell, click 'Next' in the lower righthand corner.

The titin outputs for each cell are Total Number of Myofibrils, Total Number of Doublets, Average Myofibril Persistence Length, Average Doublet Length, Average Douiblet Spacing, Average Size of All Puncta, Total Number of Puncta, Number of Rings, Average Ring Diameter, and Average Ring Aspect Ratio. If an edge is detected, four extra outputs are included: Average Doublet Distance from Edge (the average distance of all doublets from the edge), Closest Doublet Distance to Edge (the average distance from the edge of the five doublets closest to the edge), Average Ring Distance from Edge (the average distance of all rings from the edge), and Closest Ring Distance to Edge (the average distance from the edge of the five rings closes to the edge). The titin outputs for each myofibril are Number of Doublets, Average Spacing between Doublets, Persistence Length, Angle of Myofibril Long Axis (using the image edges as the axes), and Average Doublet Length. If an edge is detected, three extra outputs are included: Distance from the Edge, Edge Angle, and Normalized Myofibril Angle Compared to Edge. The titin outputs for each ring are Diameter and Aspect Ratio. If an edge is detected, an extra output is included: Distance from the Edge


## FUNCTIONS/FILES:

##### binaryMeasure.py
    This function measures features from a given binary (either one generated in yoU-Net, given by the user, or generated in makeBinary.py). The measurements are Centroid, Major Axis Length, Minor Axis Length, Orientation, Aspect Ratio, Area, and Angle. 

##### makeBinary.py
    This function generates an otsu-based binary of an image given by the user. This code is used if the user provides an image of one of the stains but no binary or data files. A threshold is calculated using otsu's method and a binary is generated using the threshold value. Features are then measured (Centroid, Major Axis Length, Minor Axis Length, Orientation, Aspect Ratio, Area, and Angle).

##### edgeDetection.py
    This function calculates the edge coordinates of an image/binary/data file with actinin2 data. Because Z-Bodies localize near the edge of cardiac myocytes, the exterior Z-Bodies are used as initial edge coordinates. In brief, the alpha shape of the Z-Bodies is calculated. The alpha shape is similar to but distinct from the convex hull and accounts for complex cell shapes. There is a small space between outer Z-Bodies and the actual cell edge (the lamella) which is accounted for after the alpha shape is calculated (the edge is dilated by a factor of 1.1 from the centroid). 

##### myofibrilSearch.py
    This code is used for finding myofibrils given a list of potential Z-Lines, M-Lines, or titin doublets (we will call them lines here). The functionality is largely the same for each marker. First, the distance between each possible pair of lines is calculated and the difference in orientation between the pair of lines is calculated. If the lines are close enough with similar angles (depends on user inputs, but is set as within 3 uM and less than 30 degrees of angle difference), they are considered to be in the same myofibril. Once every line has been compared with every other line, unique myofibrils are identified and their indices are returned to the function that called myofibrilSearch.py. 

##### MSFSearch.py
    This code is used for finding MSFs given a list of potential Z-Bodies. First, the maximum distance between potential neighboring Z-Bodies is set and the maximum Angle difference betwen the MSF and its nearest edge is set (pre-set at 3 and 15). Then, the distance between each possible pair of Z-Bodies is calculated and the difference in orientation between the nearest edge and the line connecting the two Z-Bodies is calculated. If the Z-Bodies are close enough with an angle between them that is relatively parallel to the edge, they are considered to be in the same MSF. Once every Z-Body has been assigned or not, unique MSfs are identified and their indices are returned to the function that called MSFSearch.py. 

##### calcMyofibrils.py
    This code is used to calculate statistics on myofibrils (generated by myofibrilSearch.py, for either Z-Lines, M-Lies, or titin doublets. we will call them lines here). The functionality is largely the same for each marker. First, the lines are sorted in order (from left to right, for example). Using this list, the center point of the myofibril is calculated and the absolute angle (compared to the image border axes) is calculated. If the cell has a detected edge, ehe closest edge segment to the center of the myofibril, perpendicularly (using the absolute angle) is found. This edge segment's angle is calculated and compared to the myofibril angle (Figure 2M-O) to generate the relative myofibril orientation angle. Then, the distances between each line in the myofibril and the myofibril's persistence length are calaculated. These values are all put into an array and returned to whichever function called calcMyofibrils.py.

##### calcMSFs.py
    This code is used to calculate statistics on MSFs. First, the Z-Bodies are sorted in order (from left to right, for example). Using this list, the center point of the MSF is calculated and the distance of this center point to the closest edge segment is calculated. Then, the distances between each neighboring Z-Body in the MSF is calculated and the MSF's persistence length is calculated. These values are put into an array and returned to whichever function called calcMSFs.py

##### conv2png.py
    This function converts images to PNGs for usage in the GUI

##### getMetadata.py
    This function grabs the image resolution for use in calculations

##### findActinEdge.py
    This function uses an image of an F-actin stain to find the cell edge and save the coordinates for use in calculations. The cell edge is found using thresholding followed by the removal of small objects and hole filling. This function includes case-specific code to assist in determining the best threshold in various cases (for example, if an image had two cells in it and the user removed one to ony calculate the edge of the other, leaving a black hole in the image that would affect automatic thresholding). The X and Y coordinates for the edge are returned to whichever function called findActinEdge.py

##### findNMIIEdge.py
    This function uses an image of an NMII (A or B) stain to find the cell edge and save the coordinates for use in calculations. The cell edge is found using thresholding followed by binary dilation, the removal of small objects, and hole filling. This function includes case-specific code to assist in determining the best threshold in various cases (for example, if an image had two cells in it and the user removed one to ony calculate the edge of the other, leaving a black hole in the image that would affect automatic thresholding). The X and Y coordinates for the edge are returned to whichever function called findNMIIEdge.py

##### prepareData.py
    This function imports data files (uploaded using the sarcApp gui) and extracts the relevant information needed for calculations. The information required for each data file (can be easily generated in FIJI using the image binary) is the X coordinate, Y coordinate, major axis length, minor axis length, angle, aspect ratoi, area, and circularity. If a data file folder is not uploaded, the binaries will be segmented using binaryMeasure.py which generates these same variables for each object. These variables are put into an array (numData) and returned with a dictionary of header keys to whichver function called prepareData.py

##### channelAssignments.py
    This code contains a suite of wrapper functions to analyze which file types were submitted into the GUI and call the appropriate programs for each.
    
##### runModel_yoUNetgui.py
	This is the GUI wrapper for using a pre-made deep learning model to generate prediction maps which can be converted into binaries by the user. The inputs are the path to the image data, the path to the model, and the path to an empty output folder. Whether the model was generated using 16 or 32 feature maps must also be defined.
	
##### runModel2factor.py
    This function runs a pre-made deep  learning model to generate prediction maps which can be converted into binaries by the user. The inputs are the path to the image data, the path to the model, and the path to an empty output folder. Whether the model was generated using 16 or 32 feature maps must also be defined.

##### trainModel_yoUNetgui.py
    This is the GUI wrapper for generating deep learning models to predict binaries. The GUI requires four folders: a folder for your training images, a folder for the matched ground truth binaries, a folder for validation images, and a folder for the matched ground truth binaries for the validation dataset. It also asks for the number of epochs and number of features (16 or 32)

##### trainDataset2factor.py
    This function contains a class to open and store the datasets used for generated a deep learning model. In brief, for every iteration in each epoch (see trainAndVal2factor.py), 10 images are randomly seleted from the training image folder and transformed randomly (augmentation) using elastic and affine transformations. The images are then converted to tensors and returned to trainAndVal2factor.py for model training. For validation images, the raw images are opened and no augmentation is done, then the images are returned to trainAndVal2factor.py where the model is set to evaluate mode.

##### trainAndVal2factor.py
    This code contains the functions necessary to train and validate a U-Net deep learning model to generate image binaries. Briefly, there is a training loop for each iteration in each epoch (our models were generated with 100 epochs with 10 iterations each and a batch size of 10 images per iteration). The model is set to train mode, gradients zeroed, and the model applied and loss calculated. Then the loss is backpropagated and the parameters are adjusted. There is also a validation loop, once per epoch, where the model is set to evaluation mode and gradients disabled. For each of the images in the validation folder, the most recent version of the model is applied and its accurary validation metric is calculated (Dice Coefficient, also in this code). The predictions made from the model are saved in the given output folder so the user can watch as the model becomes more and more accurate. 

##### unet2factor.py
    This code contains the actual U-Net functionality, described in Figure 1 and S1. 

##### implement2factor.py
    This code is what is called by the GUI to actually implement the training of a model. For each epoch, it runs 10 iterations of training and one validation step.

Logo courtesy of Zachary Sanchez, Vanderbilt University. Edited by Abigail Neininger-Castro
