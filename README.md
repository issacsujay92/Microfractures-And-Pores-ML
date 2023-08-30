# Microfractures-And-Pores-ML

## Overview of the repository
**Code**
The code developed in this study is provided in this repository with no restrictions on its usage. We only ask that you cite the study if it was useful in any capacity. The instructions on using the code are provided in the following section.

**Dataset**
The dataset of 18 petrographic thin section scans is provided in this repository and also contains no restrictions on its usage. The folder for each of the scans contains the following images;
1. The raw scan
2. The cropped raw scan
3. The processed scan
4. The HSB colorspace thresholded image
5. The HSB colorspace thresholded image with a 30 px closing operation
6. The HSB colorspace thresholded image with a 1000 px opening operation
7. The LAB colorspace thresholded image
8. The LAB colorspace thresholded image with a 30 px closing operation
9. The LAB colorspace thresholded image with a 1000 px opening operation
10. The combined HSB and LAB image (binary)
11. The combined HSB and LAB image (as a color composite)

The processing of the images was performed in Fiji (Schindelin et al., 2012) using the following plugins;
MorphoLibJ (Legland et al., 2016)

## Code
### Libraries Used

1. tidyverse
2. dplyr
3. caret
4. magrittr
5. ggplot2
6. ggthemes
7. gridExtra
8. MASS
9. reshape2
10. ggcorrplot
11. ggfortify
12. stats
13. GGally
14. class
15. ranger
16. svglite
17. MLeval
18. fastshap
19. shapviz
20. viridisLite

(Note: It's advisable to check the specific versions of these libraries when replicating or running the provided code.)

---

## How to Use

1. **Setup**: Ensure you have R and RStudio (or your preferred R environment) installed.
2. **Library Installation**: Before running the code, install all the libraries listed above using `install.packages("library_name")` in your R console.
3. **Download and Open**: Download the `.rmd` file and open it in RStudio.
4. **Run**: Execute the code chunks step-by-step, ensuring you understand the purpose of each section. Some chunks may have dependencies on previous chunks, so it's important to execute them in order.
5. **Output**: The expected output format is an `html_document`. Once you knit the document, you should see the results in an HTML format. You can alternately change the output to your preferred types such as MS Word, pdf, etc.
6. **Troubleshooting**: If you face any issues or errors, ensure that:
   - All libraries are correctly installed.
   - You're running the code chunks in the correct order.
   - Your R environment is up to date.

---


## References
Legland, David, Ignacio Arganda-Carreras, and Philippe Andrey. "MorphoLibJ: integrated library and plugins for mathematical morphology with ImageJ." Bioinformatics 32, no. 22 (2016): 3532-3534.
Schindelin, Johannes, Ignacio Arganda-Carreras, Erwin Frise, Verena Kaynig, Mark Longair, Tobias Pietzsch, Stephan Preibisch et al. "Fiji: an open-source platform for biological-image analysis." Nature methods 9, no. 7 (2012): 676-682.
