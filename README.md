
#### Installing source:
- Navigate to the <code>panda3d_room/</code> directory and then
create and activate a virtualenv. Install the requirements.

<pre><code>python -m venv ./venv
source venv/Scripts/activate
pip install -r requirements.txt</code></pre>

#### Run development:

<pre><code>python main.py</code></pre>

#### Build Windows binaries for distribution:

<pre><code>python setup.py build_apps</code></pre>

- A build/ folder will get created after running the
above command. Double-click the build/panda3d_room.exe
to open the app.

#### 3d-models
- The glb/gltf files in assets/ were converted
to bam by activating the venv and running:

<pre><code>gltf2bam assets/ninja.glb assets/ninja.bam</code></pre>

#### Keyboard controls:
<pre><code>up      -> walk
left    -> rotate ninja/cam left
right   -> rotate ninja/cam right
down    -> walk backwards
w + up  -> run
s       -> punch
d       -> strafe right
a       -> strafe left</code></pre>

#### Xbox controls:
<pre><code>dpad-up         -> walk
dpad-left       -> rotate ninja/cam left
dpad-right      -> rotate ninja/cam right
dpad-down       -> walk backwards
a + dpad-up     -> run
x               -> punch
left-trigger    -> strafe left
right-trigger   -> strafe right</code></pre>


<br><br>
<img src="https://user-images.githubusercontent.com/30498791/190553885-d95448a6-01eb-46c6-b81a-83b50cb4a2fa.png" alt="ex">

