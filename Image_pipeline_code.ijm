//Thin section processing and segmentation code

// lets you choose your folder
inputDir = getDirectory("Choose your input folder");
path = getDirectory("Choose your output folder");

// Import file (assuming image already cropped)
open();
sample_name = File.nameWithoutExtension;
raw_img = getImageID();
print("raw image imported");

// Non-local means denoising
selectImage(raw_img);
run("Non-local Means Denoising", "sigma=15 smoothing_factor=1 auto"); // typically finds the best parameters automatically
denoised_img = getImageID();
print("raw image desnoised");

// Unsharp mask
selectImage(denoised_img);
run("Unsharp Mask...", "radius=1 mask=0.60"); // test which values work beforehand to choose the best parameters
sharp_img = getImageID();
print("denoised image sharpened");

// Segmentation by color thresholding in the HSB space
selectImage(sharp_img);
run("Color Threshold...");
waitForUser
hsb_binary = getImageID();

// Segmentation by thresholding in the LAB space
selectImage(sharp_img);
run("RGB to CIELAB");
run("Stack to Images");
selectWindow("a");
close();
selectWindow("L");
close();
selectWindow("b");
lab_binary = getImageID();

//HSB processing
////Removing the PPR
selectImage(hsb_binary);
run("Gray Scale Attribute Filtering", "operation=Opening attribute=Area minimum=30 connectivity=4");
hsb_pores_removed_title = sample_name + "_" + "30px.removed_HSB";
saveAs("Tiff", path + hsb_pores_removed_title);

////Cleaning the pores out
selectWindow(hsb_pores_removed_title + ".tif");
run("Gray Scale Attribute Filtering", "operation=Closing attribute=Area minimum=1000 connectivity=4");
hsb_pores_cleaned_title = sample_name + "_" + "1000px.cleaned_HSB";
saveAs("Tiff", path + hsb_pores_cleaned_title);
selectWindow(hsb_pores_cleaned_title + ".tif");
hsb_processed = getImageID();

//LAB processing
////Removing the PPR
selectImage(lab_binary);
run("Gray Scale Attribute Filtering", "operation=Opening attribute=Area minimum=30 connectivity=4");
lab_pores_removed_title = sample_name + "_" + "30px.removed_LAB";
saveAs("Tiff", path + lab_pores_removed_title);

////Cleaning the pores out
selectWindow(lab_pores_removed_title + ".tif");
run("Gray Scale Attribute Filtering", "operation=Closing attribute=Area minimum=1000 connectivity=4");
lab_pores_cleaned_title = sample_name + "_" + "1000px.cleaned_LAB";
saveAs("Tiff", path + lab_pores_cleaned_title);
selectWindow(lab_pores_cleaned_title + ".tif");
lab_processed = getImageID();

//Adding the processed binary images
imageCalculator("Add",hsb_processed,lab_processed);
final_img_id = getImageID();
addition_title = sample_name + "_" + "HSB+LAB.binary";
saveAs("Tiff", path + addition_title);

run("Close All");
