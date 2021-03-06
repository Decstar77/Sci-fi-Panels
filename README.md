# Sci-fi-Panels
A procedural Sci-fi panel generator for blender 2.8

**Please Note** </br>
I'm an no longer working on this, and thus is no longer supported </br>
If you'd like a last packaged version that you can load as an add on in blender 2.8 you can find that here: https://gum.co/TCnk 

**For the programmer** </br>
There are 2 algorithms for generating the panels which I call, Square and Abstract.

| Algorithm     |  Description  |
| ------------- | ------------- |
| Square  | This algorithm works by taking the least and max vertex in the mesh, then generating a series of planes to cut the mesh. The resulting intersections are the cuts. The cuts are then bevelled, and extruded. All the above has random values that are tweakable. Example: number of planes generated |
| Abstract | This algorithm works by picking 2 edges. These 2 edges will then be sub-divided resulting in an extra vertex on each edge. These extra vertices are then connected to form a new edge. This new edge is then bevelled, and extruded. Again, the above uses random values are tweakable. Example: how much the edge is bevelled |

**Installation**
<ul>
  <li> Unzip the file. </li>
  <li> Place the unzipped file into your Blender addon directory. </li>
  <li> Start Blender then navigate to "user preferences"then "addons" and activate it. </li>
</ul>

**Usage**
<ul>
  <li> Once installed you can find all the settings and algorithms under the "N panel". </li>
  <li> Select the model you wish to use, then click the algorithm you'd like to use. </li>
  <li> There are two algorithms, Square and Abstract, each one comes with their own settings below the button. </li>  
</ul>

**Tips**
<ul>
  <li> Vertex count plays a vital role. Keeping the vertex count low and the distance between vertices high will generate the best  results. This is because if vertices are too close to one another the generator avoid cutting there. </li>
  <li> If the results are not to your liking you can always undo the change and try again. This is a common occurrence as there is a great deal of randomness when generating. </li>
  <li> Hovering over each setting available will give you a short description on what it does. </li>
  <li> The addon works best with planes. The planes can any shape and size as well as be curved. </li>
</ul>

