### Example Python Panda3d Scene with 3rd-Person Camera
- Use keyboard or XBox controller


### Installing Panda3d source for Windows or Ubuntu:
- Navigate to the <code>panda3d_room/</code> directory and then
create and activate a virtualenv. Install the requirements:

<pre><code>pip install -r requirements.txt</code></pre>

- If on Ubuntu, these libraries may be required:
<pre><code>sudo apt-get install build-essential pkg-config \
    fakeroot python3-dev libpng-dev libjpeg-dev libtiff-dev \
    zlib1g-dev libssl-dev libx11-dev libgl1-mesa-dev \
    libxrandr-dev libxxf86dga-dev libxcursor-dev bison flex \
    libfreetype6-dev libvorbis-dev libeigen3-dev libopenal-dev \
    libode-dev libbullet-dev nvidia-cg-toolkit libgtk2.0-dev \
    libassimp-dev libopenexr-dev</code></pre>


### Run development:

<pre><code>python main.py</code></pre>


### Build Windows binaries for distribution:

<pre><code>python setup.py build_apps</code></pre>

- A build/ folder will get created after running the
above command. Double-click the build/panda3d_room.exe
to open the app.


### 3d-models:
- The <code>.glb</code> files in <code>assets/</code> were converted
to <code>.bam</code> by activating the venv and running <code>gltf2bam</code>:

<pre><code>gltf2bam assets/ninja.glb assets/ninja.bam
gltf2bam assets/Home2_Night.glb assets/Home2_Night.bam</code></pre>


### Keyboard controls:
<pre><code>s       -> punch
d       -> strafe right
a       -> strafe left
w + up  -> run
up      -> walk
left    -> rotate ninja/cam left
right   -> rotate ninja/cam right
down    -> walk backwards</code></pre>


### XBox controls:
<pre><code>X                         -> punch
RB                        -> strafe right
LB                        -> strafe left
A + directional-arrow-up  -> run
directional-arrow-up      -> walk
directional-arrow-up-left -> rotate ninja/cam left
directional-arrow-right   -> rotate ninja/cam right
directional-arrow-down    -> walk backwards</code></pre>


<br><br>
<img src="https://user-images.githubusercontent.com/30498791/190553885-d95448a6-01eb-46c6-b81a-83b50cb4a2fa.png" alt="ex">
<br><br>
