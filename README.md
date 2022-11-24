# Unet-denoising-tool-for-textbook-images
This tool (named UDM) will use a pre-trained Unet model to remove grids, grey background and noise from text and equations in textbook type papers (with diffent types of grids)
the dataset used is a png converted verion of the CROHME competitions (summ of all) + IAM dataset that both have been modified by adding random noise, random backrounds and random grids.







![image](https://user-images.githubusercontent.com/97101162/191034246-077eae24-c636-4745-9602-7255ae1301d4.png)

Real world input (this image is a picture taken from a student's textbook; image not present in the dataset)

![image](https://user-images.githubusercontent.com/97101162/191034550-a189268a-20e1-45a4-8bce-9b94649d2306.png)

Output


Above is an example where the model worked perfectly.



![image](https://user-images.githubusercontent.com/97101162/191035633-0fad00fe-c999-4226-addc-06bf3fdb91d8.png)

![image](https://user-images.githubusercontent.com/97101162/191035677-32b13257-1ea9-4754-bb7d-d0495c7a9007.png)

Above is an example where the model not only removed the noise and grids but also recuntructed the writing; the little blank in the red boxe was filled by the model in the output image, the prediction is however not perfect due to the bars just above the Fs.

-----------------------------------------Critic-----------------------------------------------------

![image](https://user-images.githubusercontent.com/97101162/191036610-4ce09dd6-1c50-4df8-8db8-6f2bbebec96a.png)

![image](https://user-images.githubusercontent.com/97101162/191036627-e943337e-f824-496c-b1f4-a65912ac2d1f.png)

Above is a disadventage of our model, it learned to only proccess the data correctly when the symbols in the image are of a similar size of the one from the training set (single or doble line of text or equations), this issue however can be overcomed with ease by slicing the images


![image](https://user-images.githubusercontent.com/97101162/191037546-aca68e53-5885-49ed-b963-c0259e821bf4.png)

Above is the application of the model on the first line of the last image.




Other real world application :

![image](https://user-images.githubusercontent.com/97101162/191038155-25edd039-fbdf-41dc-91cc-37616c11ca76.png)

![image](https://user-images.githubusercontent.com/97101162/191038182-b9eb92f2-a3f4-4b42-8f2f-d94568049d18.png)





--------------------------------------------------------------------------------------------------------------------



How to use ?
I have compiled the code into one .exe (900Mo)

Download link for the file: https://drive.google.com/file/d/1TcpXVGqKW6b50U_zTpaoXQff8gaVXcNg/view?usp=share_link

![image](https://user-images.githubusercontent.com/97101162/199512480-790e9aa5-3f86-446d-9bd2-6795537c8893.png)

execute the file and wait for its initialization (2 minutes depending or your hardware) (make sure to have
at least 2 Go free disk space for it to load as temporary file)

![image](https://user-images.githubusercontent.com/97101162/199513299-fa451721-78e4-4ebc-8064-86b67a422c74.png)

insert the full path of the image file (with the name with extenction .png or jpg)

![image](https://user-images.githubusercontent.com/97101162/199514204-0d4e1a0f-6f04-4538-8da1-9ab95c172515.png)

the output image will also be saved in the main dir as "out.png"

![image](https://user-images.githubusercontent.com/97101162/199514563-463547a0-5c28-4fed-9ec0-ade2b8cd12a1.png)





