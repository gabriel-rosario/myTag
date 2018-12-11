# MyTag
**About**
---
MyTag is a Programming Language with the purpose of facilitating the creating and editing process of manipulating 
the meta-data of certain file formats.  These formats include: MP4, MP3, and PDF files.  Using the MyTag language a user can easily
edit metadata about the files, add coverart to music and video files, watermark PDF files, and much more.  Also, this language
permits the user manipulate whole directories so that for example, edit all the data about an album with just one execution instead 
of doing it one by one.

**Setup**
---
First of all, clone this repository to your computer.

Now, to begin the setup to use this language, it is assumed that you already have Python 3 installed.  The external libraries need to be installed using PIP (if you have Python 3 installed, then this is also installed)

You also need to install the PLY parsing tool.

After this is installed, you need to install the external libraries located in the requirements.txt file by running ```pip install –r requirements.txt```

Alternatively, you can install them seperately from the terminal.  Navigate to the cloned repository and run the following commands:
1. ```pip install pypdf2```
2. ```pip install pymupdf```
3. ```pip install ffmpy```
4. ```pip install send2trash```
5. ```pip install mutagen```

Now that you have all the libraries installed, you can begin to edit MP4, MP3, and PDF files using MyTag!

To start using MyTag, just run ```python3 myTag.py``` and you are now writing in the MyTag language!
To see what you can do with this languages, read the documentation in the following section of this file.

**Features**
---
1. MP4 Files

    a. set and get tags - manage file about file's creator, author, genre, etc.

    b. set costume artwork - pass a path to an image and set it as the video's coverart

    c. add chapters - divide the video into chapters to easily navigate to specific parts

    d. add subtitles - add subtitles in multiple languages

    e. writing multiple files - pass a directory as the path and manipulate multiple audio files at once

2. MP3 Files

    a. set and get ID3 tags - manage file about file's creator, author, genre, etc.

    b. set costume artwork - pass a path to an image and set it as the audio's coverart

    c. writing multiple file - pass a directory as the path and manipulate multiple audio files at once

3. PDF Files

    a. merge - merge two PDF Files.  It can be merged at the end of a file or in the middle.

    b. watermark - add a watermark to each page of the original PDF
    
    c. create Table of Content - create a ToC to bookmark certain pages and sections to be able to skip to specific pages easily

    d. modify tags - edit author, creator, date, etc.

**Documentation**
---

For all files you work with, the first step would be to create a variable for the path of the file you wish to work with.

Example: 

```vid myvid = /Users/usr/Demo/GameOfThrones```

Now, this will change depending on the format of the file so for MP4 is ```vid myvar = /PATH/```, for MP3 is ```aud myvar = /PATH/```, and for PDF is ```doc myvar = /PATH/```

After you make all the changes you wished to do, save them by running ```save myvar```.

1. MP4 Files

    **Commands**
    
    Once you have the variable set, ```vid myvar = /PATH/```, you can use the following commands to edit the file:
    
    a. SET
    ```set myvar<TAG> = VALUE```
    
    where TAG is the metadata tag you wish to edit, and VALUE is the new value it will have.  Possible tags include:
    ```title```, ```artist```, ```album```, ```track```, ```genre```, ```date```, ```description```, ```comment```, ```grouping```
    
    b. GET
    ```get myvar<TAG>```
    
    where TAG is the metadata tag, shown previously, you with to view the value of.
    
    c. COVER
    
    To set the cover image, it uses the SET function but with the ```cover``` as the TAG, and a PATH name to the image, instead of string.
    
    ```set myvar<cover> = /PATH/```

    d. ADD
    ```add myvar<TAG> = VALUE```

    This is used to add either ```chapter``` or ```sub``` to add either chapters or subtitles to the video.

    Example: ```add myvar<chapter> = "10"```  adds 10 chapters to the video

    ```add myvar<sub> = "PATH/To/SUBS"```     adds subtitles located in the file specified

    e. CLEAR
    ```clear myvar```

    This clears the file's metadata

2. MP3 Files

    **Commands**
    
    Once you have the variable set, ```aud myvar = /PATH/```, you can use the following commands to edit the file:
    
    a. SET
    ```set myvar<TAG> = VALUE```
    
    where TAG is the metadata tag you wish to edit, and VALUE is the new value it will have.  Possible tags include: 
    ```title```, ```artist```, ```album```, ```albumartist```, ```composer```, ```genre```, ```date```, ```tracknumber```, ```discnumber```, ```bpm```
    
    b. GET
    ```get myvar<TAG>```
    
    where TAG is the metadata tag, shown previously, you with to view the value of.
    
    c. COVER
    
    To set the cover image, it uses the SET function but with the ```cover``` as the TAG, and a PATH name to the image, instead of string.
    
    ```set myvar<cover> = /PATH/```

    d. CLEAR
    ```clear myvar```

    This clears the file's metadata

3. PDF Files

    **Commands**
    
    Once you have the variable set, ```doc myvar = /PATH/```, you can use the following commands to edit the file:
    
    a. SET
    ```set myvar<TAG> = VALUE```
    
    where TAG is the metadata tag you wish to edit, and VALUE is the new value it will have.  Possible tags include: 
    ```format```, ```title```, ```author```,```subject```,```keywords```,```creator```,```producer```,```creationDate```,```modDate```,```encryption```
    
    b. GET
    ```get myvar<TAG>```
    
    where TAG is the metadata tag, shown previously, you with to view the value of.
    
    c. WATERMARK
    
    Watermark uses the SET function but receives a path to the watermark PDF instead of a string, like:
    
    ```set myvar<watermark> = /PATH/```
    
    d. TABLE OF CONTENTS
    
    This uses the SET function too, but receives a string in the following format: ```1 string 3```, where ```1``` is the heirarchy of the bookmark
    (if it's a main section, or a subsection of the main section would be a ```2```, and so on), ```string``` is the title of the chapter/section,
    and ```3``` would be the page to link to.
    
    EXAMPLE:
    
    ```
    set myvar<toc> = "1 chapter1 2"
    set myvar<toc> = "2 subsection1 4"
    set myvar<toc> = "2 subsection2 5"
    set myvar<toc> = "1 chapter2 7"
    save myvar
    ```

    e. CLEAR
    ```clear myvar```

    This clears the file's metadata
    
**Example**
---
This is an example to add metadata and coverart for a MP4 video file

```
vid myvid = /Users/usr/Demo/GameOfThrones             //creates variable with video path name
set myvid<artist> = “George Martin”                   //add artist name metadata
set myvid<genre> = “Fantasy”                          //add genre metadata
set myvid<date> = “2017”                              //add date metadata
set myvid<cover> = /Users/usr/Demo/cover.jpg          //add cover image to video
save myvid                                            //save changes
```

**Video Example**
---

Here is a visual example of the code running.

You you can click [this link to see it on youtube](https://www.youtube.com/watch?v=kcqrEt1Ks7A) or go to [https://www.youtube.com/watch?v=kcqrEt1Ks7A](https://www.youtube.com/watch?v=kcqrEt1Ks7A).



**Final Report**
---
The final report can be seen by viewing the github page and opening the file called FinalReport.pdf or by clicking [here](https://github.com/gabriel-rosario/myTag/blob/master/FinalReport.pdf).


**Credit**
---
This project was created by: Josue Castro, Jean Merced, Gabriel Rosario and Ariel Silva.  
All students from the University of Puerto Rico at Mayaguez for the Programming Languages course 
during the Fall 2018 Semester with direction of Dr. Wilson Rivera.