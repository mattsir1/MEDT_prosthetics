"JointINO" contains the compiled files, used during implementation.





MEDT_Joint contains the visual studio package and files related
JointINO contains the .INO file and any Joint classes

Rather than having the .INO in the folder with the rest of the clutter for the Visual Studio files, it was moved into it's own folder. During execution there are minor problems when referencing anything below the .INO file. 
  
  Example: 
  File: Joint.INO 
    include ".\SampleFolder\Joint.cpp"
   
With the above include directory during execution the .INO file has some issues reading the joint structure and can't find the file. To simplify organizing the files Joint.INO requires, the folder exclusively holds any and all relevant files.
