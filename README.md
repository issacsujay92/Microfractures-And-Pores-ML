# Microfractures-And-Pores-ML

## Overview of the codes in the repository
This study was performed in three programming languages: ImageJ macro language (based on Javascript), Python, and R
### ImageJ
ImageJ was used for image processing and segmentation. The macro used for this pipeline is image_pipeline.ijm
The macro can be run as is in Fiji (or ImageJ), and will prompt the user for the image path. For each processing and segmentation step, it prompts the user for manual tuning, so it can be applied to any image type.

### Python
Python was used for connected components analysis (labelling), feature extraction, visualization of the random sampling, and visualization of the predicted classes. In addition, the ellipses and maximum and minimum axes visualized in Fig. 8 of the study was made using this language. The codes are named according to their task.

### R
The machine learning code is written in RMarkdown with each of the steps of the supervised ML pipeline documented within the document. The code developed in this study has no restrictions on its usage. We only ask that you cite the study if it was useful in any capacity. The instructions on using the code are provided in the following section.

#### Libraries Used

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


