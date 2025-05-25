# HIT137-Group_SYD_17
This is the assessment repository for Software Now subject where Group 17 members will collaborate to complete all assignments. 

## Assessment 2
### To run the file

1. Open the terminal in the "Assessment2" folder.
2. Run the code using the following command:

### 1. For encryption and decryption 
```bash 
python enc_dec/enc_dec.py
 ```
The encrypted text is saved in enc_dec/result_files/encrypted_text.txt file. 

### 2. For Australian Temperature analysis 

 ```bash
 python temp_aus/temp_analysis.py
 ```
The analysis results of the temperature are saved inside temp_aus/analysis folder. 

### 3. To Draw Tree Pattern 

 ```bash
 python tree_pattern/tree_pattern_turtle.py
 ```
This is the tree pattern generated using following values: <br>
Left branch angle: 25   </br>
Right branch angle: 20  </br>
Starting branch length: 100 </br>
Recursion depth: 5 </br>
Branch length reduction factor(1-100): 70
</br></br>
 ![alt text](/images/tree_pattern.png)


 ## Assessment 3

### 1. Image Processing GUI (Question 1)

This desktop application shows GUI for image processing. It includes the following features:

1. **Image Loading**
   - Select and load images from your local device
   - Supports common image formats (jpg, jpeg, png, bmp, gif)
   - Displays the loaded image in the application window

2. **Image Cropping**
   - Draw a selection rectangle using mouse interaction
   - View the cropped result alongside the original image

3. **Image Resizing**
   - Adjust the size of the cropped image using a slider control
   - Real-time preview as you adjust the size

4. **Save Functionality**
   - Save the modified image in PNG or JPEG format
   - Preserves the current crop and resize settings


#### To Run the Application

1. Open the terminal in the "Assessment3" folder.
2. Install the required packages
    ```bash
    pip install -r requirements.txt
    ```
3. Run the command:
   ```bash
   python image_processing_gui.py
   ```

