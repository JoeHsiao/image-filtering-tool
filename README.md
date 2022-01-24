# Matting Human Datasets Labling 
This is a GUI tool for manually filtering images from the [Matting Human Datasets](https://www.kaggle.com/laurentmih/aisegmentcom-matting-human-datasets) dataset on Kaggle. This dataset provides a large number of images (34427), yet the quality of most mattings is not very good, e.g. mislabeled background pixels and random alpha values, which suffocate the performance of a neural network. This tool helps label the good ones and ignore the bad ones.

# How it works
The programs sorts all the images in terms of file names, and displays one image at a time on the screen, with the alpha matting superimposed on the image. Users check the matting quality, and decide whether the matting is good enough to be kept in the dataset.

Note that if labeling is interrupted, the program remembers which image it was stopped at and will resume from that image next time. Labeling results will be stored in a .csv file. 

# Program interface:
<p>
<img src="/screenshots/good_matting.png" width="30%" height="30%" />
<img src="/screenshots/bad_matting.png" width="30%" height="30%" />
</p>


# Usage
- Right arrow: Mark current image as 'bad', and move on to the next image.
- Left arrow: Go back to the previous image.
- Up arrow: Mark current image as 'good'.
- Down arrow: Mark current image as 'bad'.
- Esc: save and exit.
