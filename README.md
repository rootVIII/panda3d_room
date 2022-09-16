<br>
###### Installing source:
Navigate to the panda3d_room/ directory and then create
and activate a virtualenv. Install the requirements.
<br>
python -m venv ./venv
source venv/Scripts/activate
<code>pip install -r requirements.txt</code>
<br>
###### Run development:
<br>
<code>python main.py</code>
<br>
###### Build Windows binaries for distribution:
<br>
<code>python setup.py build_apps</code>
<br>
- A build/ folder will get created after running the
above command. Double-click the build/panda3d_room.exe
to open the app.
<br>
- The glb/gltf files in assets/ were converted
to bam by activating the venv and running:
<br>
<code>gltf2bam assets/ninja.glb assets/ninja.bam</code>
<br><br>